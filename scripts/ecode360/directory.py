from __future__ import annotations

from difflib import get_close_matches
from html.parser import HTMLParser
import re
import unicodedata
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .errors import ECodeError
from .models import DirectoryEntry
from .output import DIRECTORY_URL

STATE_NAMES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}
STATE_CODES = set(STATE_NAMES.values())
PREFIX_RE = re.compile(r"^(?:town|city|village|borough|municipality)\s+of\s+", re.I)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def _ascii(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def normalize_state(value: str) -> str:
    normalized = _ascii(value).strip().casefold()
    if normalized in STATE_NAMES:
        return STATE_NAMES[normalized]
    code = normalized.upper()
    if code in STATE_CODES:
        return code
    raise ECodeError("invalid_state", f"Unknown state: {value}", 2)


def normalize_municipality(value: str) -> str:
    without_prefix = PREFIX_RE.sub("", _ascii(value).strip())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", without_prefix.casefold())).strip()


class _DirectoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.state = ""
        self.entries: list[DirectoryEntry] = []
        self._stack: list[str] = []
        self._item_depth: int | None = None
        self._link_depth: int | None = None
        self._county_depth: int | None = None
        self._entry_name: list[str] = []
        self._entry_county: list[str] = []
        self._entry_url = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag not in VOID_TAGS:
            self._stack.append(tag)
        classes = set((attrs_map.get("class") or "").split())
        if tag == "a" and "stateAnchor" in classes and attrs_map.get("id"):
            self.state = (attrs_map["id"] or "").upper()
        if tag == "div" and "listItem" in classes:
            self._item_depth = len(self._stack)
            self._entry_name = []
            self._entry_county = []
            self._entry_url = ""
        elif self._item_depth is not None and tag == "a" and "codeLink" in classes:
            self._link_depth = len(self._stack)
            self._entry_url = attrs_map.get("href") or ""
        elif self._item_depth is not None and tag == "div" and "codeCounty" in classes:
            self._county_depth = len(self._stack)

    def handle_data(self, data: str) -> None:
        if self._link_depth is not None:
            self._entry_name.append(data)
        elif self._county_depth is not None:
            self._entry_county.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if tag not in self._stack:
            return
        depth = len(self._stack)
        if self._link_depth == depth and tag == "a":
            self._link_depth = None
        if self._county_depth == depth and tag == "div":
            self._county_depth = None
        if self._item_depth == depth and tag == "div":
            parsed = urlparse(self._entry_url)
            host = (parsed.hostname or "").lower()
            ecode_id = parsed.path.strip("/") if host in {"ecode360.com", "www.ecode360.com"} else ""
            county = " ".join("".join(self._entry_county).split()).strip("() ")
            name = " ".join("".join(self._entry_name).split())
            if self.state and name and self._entry_url:
                self.entries.append(DirectoryEntry(name, self.state, county, ecode_id, self._entry_url))
            self._item_depth = None
        while self._stack and self._stack[-1] != tag:
            self._stack.pop()
        if self._stack:
            self._stack.pop()


def parse_directory(html: str) -> tuple[DirectoryEntry, ...]:
    parser = _DirectoryParser()
    parser.feed(html)
    parser.close()
    return tuple(parser.entries)


def fetch_directory(timeout_seconds: float = 30.0) -> str:
    request = Request(DIRECTORY_URL, headers={"User-Agent": "Civic-Data eCode360 research tool/1.0"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except (OSError, URLError, UnicodeError) as exc:
        raise ECodeError("directory_fetch_failed", f"Unable to fetch ICC directory: {exc}", 3) from exc


def _candidate(entry: DirectoryEntry) -> dict[str, object]:
    return {
        "display_name": entry.display_name,
        "state": entry.state,
        "county": entry.county,
        "url": entry.code_url,
    }


def resolve_municipality(
    entries: tuple[DirectoryEntry, ...], municipality: str, state: str
) -> DirectoryEntry:
    state_code = normalize_state(state)
    target = normalize_municipality(municipality)
    state_entries = [entry for entry in entries if entry.state.upper() == state_code]
    matches = [entry for entry in state_entries if normalize_municipality(entry.display_name) == target]
    if not matches:
        names = {normalize_municipality(entry.display_name): entry for entry in state_entries}
        close = get_close_matches(target, list(names), n=3, cutoff=0.55)
        suggestions = tuple(_candidate(names[name]) for name in close)
        raise ECodeError("municipality_not_found", f"No municipality matched {municipality} in {state_code}", 3, suggestions)
    if len(matches) > 1:
        raise ECodeError("ambiguous_municipality", f"Multiple municipalities matched {municipality} in {state_code}", 3, tuple(_candidate(entry) for entry in matches))
    entry = matches[0]
    if not entry.ecode_id:
        raise ECodeError("unsupported_provider", f"ICC entry is not hosted by eCode360: {entry.code_url}", 3, (_candidate(entry),))
    return entry
