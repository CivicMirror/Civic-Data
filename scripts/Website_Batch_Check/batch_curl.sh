#!/usr/bin/env bash
set -uo pipefail

usage() {
  cat <<'EOF'
Usage: ./batch_curl.sh URL_FILE [OUTPUT_DIR] [CONCURRENCY]

Reads one URL per line and saves:
  OUTPUT_DIR/responses/NNN_response.body
  OUTPUT_DIR/headers/NNN_headers.txt
  OUTPUT_DIR/summary.csv

Blank lines and lines beginning with # are ignored.

Example:
  chmod +x batch_curl.sh
  ./batch_curl.sh websites.txt curl_results 8
EOF
}

if [[ $# -lt 1 || $# -gt 3 ]]; then
  usage >&2
  exit 2
fi

url_file=$1
output_dir=${2:-curl_results}
concurrency=${3:-8}

if [[ ! -f "$url_file" ]]; then
  echo "Error: URL file not found: $url_file" >&2
  exit 2
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is not installed." >&2
  exit 2
fi

if [[ ! "$concurrency" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: concurrency must be a positive integer." >&2
  exit 2
fi

mkdir -p "$output_dir/responses" "$output_dir/headers" "$output_dir/status"
urls_tmp="$output_dir/.urls"

awk '
  { sub(/\r$/, "") }
  /^[[:space:]]*($|#)/ { next }
  { sub(/^[[:space:]]+/, ""); sub(/[[:space:]]+$/, ""); print }
' "$url_file" > "$urls_tmp"

total=$(wc -l < "$urls_tmp" | tr -d ' ')
if [[ "$total" -eq 0 ]]; then
  echo "Error: no URLs found in $url_file" >&2
  rm -f "$urls_tmp"
  exit 2
fi

width=${#total}
(( width < 3 )) && width=3

fetch_one() {
  local number=$1 url=$2 id body headers metrics curl_exit error_text
  printf -v id "%0${width}d" "$number"
  body="$output_dir/responses/${id}_response.body"
  headers="$output_dir/headers/${id}_headers.txt"

  echo "[$id/$total] $url" >&2

  set +e
  metrics=$(curl \
    --location \
    --compressed \
    --silent \
    --show-error \
    --retry 2 \
    --retry-delay 1 \
    --connect-timeout 15 \
    --max-time 60 \
    --user-agent 'Mozilla/5.0 (compatible; BatchCurl/1.0)' \
    --dump-header "$headers" \
    --output "$body" \
    --write-out '%{http_code}\t%{url_effective}\t%{content_type}\t%{size_download}\t%{time_total}' \
    "$url" 2>"$output_dir/status/${id}.error")
  curl_exit=$?
  set -e

  error_text=$(tr '\r\n\t' '   ' < "$output_dir/status/${id}.error")
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$url" "$curl_exit" "$metrics" "$error_text" \
    > "$output_dir/status/${id}.tsv"
}

export -f fetch_one
export output_dir total width

set -e
number=0
while IFS= read -r url; do
  number=$((number + 1))
  fetch_one "$number" "$url" &
  while (( $(jobs -rp | wc -l) >= concurrency )); do
    wait -n || true
  done
done < "$urls_tmp"
wait || true

printf 'number,input_url,curl_exit,http_status,final_url,content_type,bytes,time_seconds,error\n' \
  > "$output_dir/summary.csv"

for status_file in "$output_dir"/status/*.tsv; do
  awk -F '\t' 'BEGIN { OFS="," }
    {
      for (i=1; i<=9; i++) {
        gsub(/"/, "\"\"", $i)
        $i="\"" $i "\""
      }
      print $1,$2,$3,$4,$5,$6,$7,$8,$9
    }
  ' "$status_file" >> "$output_dir/summary.csv"
done

rm -f "$urls_tmp"
echo "Complete: $total URLs processed. Summary: $output_dir/summary.csv"
