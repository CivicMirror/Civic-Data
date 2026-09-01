# Batch Curl Website Collector

`batch_curl.sh` reads a list of website URLs, downloads each response with
`curl`, and creates a CSV summary. It can process multiple websites at the same
time and is suitable for lists such as the 87-site batch.

## Requirements

- Linux, macOS, or another environment with Bash
- `curl`
- `awk`

## 1. Prepare the URL list

Create a text file named `websites.txt` with one complete URL per line:

```text
https://example.com
https://www.agawam.ma.us/190/City-Council
https://another-example.gov/page
```

Blank lines and lines beginning with `#` are ignored:

```text
# Massachusetts municipal pages
https://example.com
```

Include `https://` or `http://` at the beginning of every URL.

## 2. Run the script

Place `batch_curl.sh` and `websites.txt` in the same directory. Open a terminal
in that directory and run:

```bash
chmod +x batch_curl.sh
./batch_curl.sh websites.txt
```

## Optional settings

The full command format is:

```bash
./batch_curl.sh URL_FILE [OUTPUT_DIRECTORY] [CONCURRENCY]
```

For example:

```bash
./batch_curl.sh websites.txt municipal_results 8
```

- `URL_FILE`: file containing one URL per line; required
- `OUTPUT_DIRECTORY`: destination for results; defaults to `curl_results`
- `CONCURRENCY`: number of requests allowed at once; defaults to `8`

Use a lower concurrency, such as `4`, if sites begin rejecting or throttling
requests.

## Output

The default output structure is:

```text
curl_results/
├── responses/       Downloaded response bodies
├── headers/         HTTP response headers
├── status/          Per-request working and error records
└── summary.csv      Combined request summary
```

`summary.csv` contains:

- Input URL
- Curl exit code
- HTTP status code
- Final URL after redirects
- Content type
- Downloaded byte count
- Request time
- Error message, when applicable

The numbered body and header files correspond to the URL order in
`websites.txt`. For example, `001_response.body` belongs to the first URL.

## Request behavior

The script:

- Follows redirects
- Accepts compressed responses
- Retries failed requests twice
- Uses a 15-second connection timeout
- Uses a 60-second total timeout per attempt
- Identifies itself with a browser-compatible user-agent string

## Troubleshooting

### Python syntax error

If you see a Python error mentioning `awk`, the script was started incorrectly.
Use:

```bash
bash batch_curl.sh websites.txt
```

### Permission denied

Either make the script executable:

```bash
chmod +x batch_curl.sh
```

or run it through Bash:

```bash
bash batch_curl.sh websites.txt
```

### URL file not found

Confirm that `websites.txt` is in the current directory, or provide its full
path:

```bash
bash batch_curl.sh /home/lefort/Downloads/websites.txt
```

### HTTP errors

An HTTP status such as `403`, `404`, or `500` is recorded in `summary.csv`.
Check the matching header, body, and error files for more details. Some sites
block automated requests even when the URL works in a browser.

