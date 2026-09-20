# Texas ISD Board Page Search

This tool reads the `ISD` sheet in `TX_Municipalities.xlsx`, takes each website
from column D, searches for `<website> board of trustees page`, and records the
first organic Google result in a new copy of the workbook.

It does **not** modify the original file. The first added column is the actual
URL returned by the search. The output adds these columns in this order:

- Board Page Result URL
- Board Page Result Title
- Board Page Domain Match
- Board Page Search Status
- Board Page Search Error
- Board Page Search Query (audit only)

## 1. Install Python packages

```bash
python3 -m pip install openpyxl
```

## 2. Choose a search provider

### Recommended: Serper

Serper returns Google search results through an API and is the easiest option
for a new setup. Create an API key at <https://serper.dev/>, then set it:

```bash
export SERPER_API_KEY="your-api-key"
```

### Existing Google Custom Search users

If you already have Google Custom Search JSON API access and a Programmable
Search Engine configured to search the web:

```bash
export GOOGLE_CSE_API_KEY="your-google-api-key"
export GOOGLE_CSE_ID="your-search-engine-id"
```

Google no longer accepts new Custom Search JSON API customers and has announced
that existing customers must transition by January 1, 2027.

## 3. Test five rows first

Rename the downloaded attachment to include the `.xlsx` extension if necessary.

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx \
  --limit 5 \
  --output TX_Municipalities_board_pages.xlsx
```

Review the five results. If they look right, continue the same output file:

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx \
  --output TX_Municipalities_board_pages.xlsx
```

Completed rows are skipped, so the second command resumes where the test ended.
The workbook is saved after every request, which also makes interrupted runs
restartable.

## Other useful commands

Preview the queries without using API credits:

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx --dry-run --limit 10
```

Use existing Google Custom Search access:

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx \
  --provider google-cse \
  --output TX_Municipalities_board_pages.xlsx
```

Start at a particular worksheet row:

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx --start-row 500
```

Replace results already written by an earlier run:

```bash
python3 tx_board_page_search.py TX_Municipalities.xlsx --overwrite-results
```

## Reading the output

- `found`: a first organic result was returned.
- `no_result`: the provider returned no organic results.
- `error`: the request failed; details are in the error column.
- `Board Page Domain Match = No`: inspect this result manually. It may be a
  legitimate hosted district page, but it may also be an unrelated result.

The tool intentionally records the first organic result, matching the workflow
described for DC ISD, Idalou ISD, and Meadow ISD. It does not claim that every
first result is correct; the domain-match column helps prioritize review.

The final `Search Query (audit only)` column contains text such as
`http://www.adrianisd.net board of trustees page`. That value is retained only
to show what was sent to the search provider; it is not the result URL.
