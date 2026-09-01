from __future__ import annotations

import re
import shutil
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

from .charter import _clean_text
from .errors import ECodeError
from .models import CharterResult, SectionResult
from playwright.sync_api import Browser, BrowserContext, Playwright, sync_playwright

SECTION_RE = re.compile(r"^(?:Sec\.|SECTION)\s*([0-9]+(?:[-.][0-9A-Za-z]+)*)\s*[:.]?\s*(.*)$", re.I | re.S)
ARTICLE_RE = re.compile(r"^ARTICLE\s+([IVXLCDM]+)\b", re.I)
CHAPTER_RE = re.compile(r"^CHAPTER\s+([IVXLCDM]+)\b", re.I)


def select_charter_url(overview_url: str, links: object) -> str:
    overview = urlparse(overview_url)
    overview_parts = overview.path.strip("/").split("/")
    code_prefix = "/" + "/".join(overview_parts[:3]) + "/"
    if isinstance(links, list):
        for link in links:
            if not isinstance(link, dict):
                continue
            text = link.get("text")
            href = link.get("href")
            if isinstance(text, str) and "charter" in text.casefold() and isinstance(href, str) and href.strip():
                candidate = urlparse(urljoin(overview_url, href))
                if candidate.hostname == overview.hostname and candidate.path.startswith(code_prefix):
                    return candidate.geturl()
    raise ECodeError("amlegal_charter_not_found", "AM Legal overview did not expose a Charter document", 5)


def navigation_urls(page_result: dict[str, object], current_url: str, charter_url: str) -> tuple[str, ...]:
    def same_book(candidate: object) -> bool:
        return isinstance(candidate, str) and is_same_amlegal_book(candidate, charter_url)

    candidates = page_result.get("children")
    child_urls = list(candidates) if isinstance(candidates, (list, tuple)) else []
    child_urls.append(page_result.get("next"))
    result: list[str] = []
    for candidate in child_urls:
        if same_book(candidate) and candidate != current_url and candidate not in result:
            result.append(candidate)
    return tuple(result)


def is_same_amlegal_book(candidate_url: str, charter_url: str) -> bool:
    charter = urlparse(charter_url)
    book_parts = charter.path.strip("/").split("/")[:4]
    parsed = urlparse(candidate_url)
    return (
        parsed.scheme == charter.scheme
        and parsed.hostname == charter.hostname
        and parsed.path.strip("/").split("/")[:4] == book_parts
    )


def scoped_article_labels(article_documents: object, charter_url: str) -> tuple[str, ...]:
    result: list[str] = []
    if not isinstance(article_documents, (list, tuple)):
        return ()
    for document in article_documents:
        if not isinstance(document, (list, tuple)) or len(document) != 2:
            continue
        label, url = document
        if isinstance(label, str) and isinstance(url, str) and is_same_amlegal_book(url, charter_url):
            cleaned = _clean_text(label)
            if cleaned and cleaned not in result:
                result.append(cleaned)
    return tuple(result)


def article_labels_for_page(
    page_result: dict[str, object],
    current_url: str,
    charter_url: str,
    linear_navigation: bool,
) -> tuple[str, ...]:
    if current_url != charter_url and not linear_navigation:
        return ()
    return scoped_article_labels(page_result.get("article_documents"), charter_url)


@dataclass
class _Block:
    identifier: str
    classes: str
    text: str
    anchor: str = ""


class _BlockParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[str] = []
        self._active: tuple[int, _Block] | None = None
        self.blocks: list[_Block] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        self._stack.append(tag)
        classes = attrs_map.get("class") or ""
        if tag == "div" and "rbox" in classes.split() and self._active is None:
            self._active = (len(self._stack), _Block(attrs_map.get("id") or "", classes, ""))
        if tag == "a" and self._active is not None:
            identifier = attrs_map.get("id") or attrs_map.get("name") or ""
            if ".Sec." in identifier or identifier.startswith("JD_Section"):
                self._active[1].anchor = identifier

    def handle_data(self, data: str) -> None:
        if self._active is not None:
            self._active[1].text += data

    def handle_endtag(self, tag: str) -> None:
        if self._active is not None and len(self._stack) == self._active[0] and tag == "div":
            block = self._active[1]
            block.text = _clean_text(block.text)
            if block.text or block.anchor:
                self.blocks.append(block)
            self._active = None
        if self._stack:
            self._stack.pop()


def parse_amlegal_sections(html: str, page_url: str) -> CharterResult:
    parser = _BlockParser()
    parser.feed(html)
    parser.close()
    if not parser.blocks:
        raise ECodeError("amlegal_extraction_failed", "AM Legal Charter page contained no code blocks", 4)

    title = next((block.text for block in parser.blocks if "Title" in block.classes and block.text), "Charter")
    payload = parse_amlegal_payload(
        {
            "title": title,
            "blocks": [
                {"anchor": block.anchor, "text": block.text, "classes": block.classes}
                for block in parser.blocks
            ],
            "articles": [
                block.text for block in parser.blocks
                if ARTICLE_RE.match(block.text) or CHAPTER_RE.match(block.text)
            ],
            "children": [],
            "next": "",
        },
        page_url,
    )
    section_results = tuple(payload["sections"].values())
    if not section_results:
        raise ECodeError("amlegal_extraction_failed", "AM Legal Charter page contained no sections", 4)
    return CharterResult(
        guid=urldefrag(page_url)[0].rstrip("/").split("/")[-1],
        title=title,
        url=page_url,
        article_count=len(payload["articles"]),
        sections=section_results,
    )


AMLEGAL_EXTRACT_SCRIPT = """
(charterUrl) => {
  const blocks = Array.from(document.querySelectorAll('div.rbox')).map(block => {
    const anchor = block.querySelector('a[id^="JD_"], a[name^="JD_"]');
    return {anchor: anchor ? (anchor.id || anchor.name) : '', text: block.innerText || '', classes: block.className || ''};
  });
  const next = Array.from(document.querySelectorAll('a')).find(link => link.innerText.trim() === 'Next Doc');
  const codeLinks = Array.from(document.querySelectorAll('a[data-orig-doc-id], a[data-docid]'));
  const charterPath = new URL(charterUrl).pathname;
  const charterLink = codeLinks.find(link => new URL(link.href).pathname === charterPath);
  const charterTree = charterLink ? charterLink.closest('.toc-entry') : null;
  const scopedCodeLinks = charterTree
    ? Array.from(charterTree.querySelectorAll('a[data-orig-doc-id], a[data-docid]'))
    : [];
  const children = scopedCodeLinks
    .map(link => link.href).filter(Boolean);
  const articles = scopedCodeLinks.filter(link => /^(CHAPTER|ARTICLE)/i.test(link.innerText.trim()))
    .map(link => ({label: link.innerText.trim(), url: link.href}));
  if (/^(CHAPTER|ARTICLE)/i.test(document.title.trim())) {
    articles.push({label: document.title.trim(), url: window.location.href});
  }
  return {title: document.title, blocks, next: next ? next.href : '', children, articles};
}
"""


class AMLegalBrowser:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    def __enter__(self) -> "AMLegalBrowser":
        self._playwright = sync_playwright().start()
        executable = next((shutil.which(name) for name in ("chromium-browser", "google-chrome", "chromium") if shutil.which(name)), None)
        options: dict[str, object] = {"headless": self.headless, "args": ["--disable-blink-features=AutomationControlled"]}
        if executable:
            options["executable_path"] = executable
        self._browser = self._playwright.chromium.launch(**options)
        self._context = self._browser.new_context(
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36")
        )
        self._context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def fetch_charter(self, overview_url: str) -> CharterResult:
        assert self._context is not None
        page = self._context.new_page()
        try:
            page.goto(overview_url, wait_until="domcontentloaded", timeout=30_000)
            links = page.evaluate("() => Array.from(document.querySelectorAll('a')).map(link => ({text: link.innerText || '', href: link.href || ''}))")
            charter_url = select_charter_url(overview_url, links)
            sections: dict[str, SectionResult] = {}
            title = "Charter"
            visited: set[str] = set()
            pending = [charter_url]
            articles: set[str] = set()
            linear_navigation = False
            for _ in range(80):
                if not pending:
                    break
                current = pending.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                page.goto(current, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(3000)
                payload = page.evaluate(AMLEGAL_EXTRACT_SCRIPT, charter_url)
                if not isinstance(payload, dict):
                    raise ECodeError("amlegal_extraction_failed", "AM Legal returned an invalid page payload", 4)
                page_result = parse_amlegal_payload(payload, current)
                if current == charter_url:
                    linear_navigation = not page_result["children"] and bool(page_result["next"])
                candidates = navigation_urls(page_result, current, charter_url)
                for candidate in candidates:
                    if candidate not in visited and candidate not in pending:
                        pending.append(candidate)
                if title == "Charter":
                    title = page_result["title"] or title
                articles.update(article_labels_for_page(page_result, current, charter_url, linear_navigation))
                sections.update(page_result["sections"])
                time.sleep(1.0)
            if not sections:
                raise ECodeError("amlegal_extraction_failed", "AM Legal Charter contained no sections", 4)
            return CharterResult(charter_url.rstrip("/").split("/")[-1], title, charter_url, len(articles), tuple(sections.values()))
        finally:
            page.close()


def parse_amlegal_payload(payload: dict, page_url: str) -> dict[str, object]:
    sections: dict[str, SectionResult] = {}

    def add_section(raw: object) -> None:
        if not isinstance(raw, dict) or not isinstance(raw.get("guid"), str):
            return
        heading = _clean_text(str(raw.get("heading", "")))
        match = SECTION_RE.match(heading)
        if not match and raw["guid"].endswith(".Preamble"):
            match = ("Preamble", heading)
        if not match or not str(raw.get("text", "")).strip():
            return
        number, section_title = match.groups() if hasattr(match, "groups") else match
        sections[raw["guid"]] = SectionResult(raw["guid"], number, _clean_text(section_title), ("Charter",), f"{page_url}#{raw['guid']}", _clean_text(str(raw["text"])), "")

    raw_blocks = payload.get("blocks")
    if isinstance(raw_blocks, list):
        current: dict[str, object] | None = None

        def finish_current() -> None:
            if current is None:
                return
            parts = current.get("text_parts")
            add_section({**current, "text": "\n".join(parts if isinstance(parts, list) else [])})

        for block in raw_blocks:
            if not isinstance(block, dict):
                continue
            anchor = block.get("anchor")
            text = _clean_text(str(block.get("text", "")))
            if isinstance(anchor, str) and anchor:
                finish_current()
                if anchor.startswith("JD_Section") or ".Sec." in anchor or anchor.endswith(".Preamble"):
                    current = {"guid": anchor, "heading": text, "text_parts": []}
                else:
                    current = None
            elif current is not None and text:
                current["text_parts"].append(text)  # type: ignore[union-attr]
        if current is not None:
            finish_current()
    else:
        raw_sections = payload.get("sections")
        if not isinstance(raw_sections, list):
            raise ECodeError("amlegal_extraction_failed", "AM Legal page sections were invalid", 4)
        for raw in raw_sections:
            add_section(raw)

    raw_articles = payload.get("articles")
    articles: list[str] = []
    article_documents: list[tuple[str, str]] = []
    if isinstance(raw_articles, list):
        for raw_article in raw_articles:
            if isinstance(raw_article, dict):
                article = _clean_text(str(raw_article.get("label", "")))
                url = str(raw_article.get("url", ""))
                if article and url:
                    article_documents.append((article, url))
            else:
                article = _clean_text(str(raw_article))
            if article and article not in articles:
                articles.append(article)
    children = payload.get("children")
    if not isinstance(children, list):
        children = []
    return {"title": str(payload.get("title") or "Charter"), "sections": sections, "articles": tuple(articles), "article_documents": tuple(article_documents), "next": str(payload.get("next") or ""), "children": tuple(str(child) for child in children if isinstance(child, str))}
