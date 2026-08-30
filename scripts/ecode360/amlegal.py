from __future__ import annotations

import re
import shutil
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urldefrag

from .charter import RawSection, _clean_text
from .errors import ECodeError
from .models import CharterResult, SectionResult
from playwright.sync_api import Browser, BrowserContext, Playwright, sync_playwright

SECTION_RE = re.compile(r"^Sec\.\s*([0-9]+(?:\.[0-9]+)*)\s*(.*)$", re.I | re.S)
ARTICLE_RE = re.compile(r"^ARTICLE\s+([IVXLCDM]+)\b", re.I)


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
            if ".Sec." in identifier:
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
    section_results: list[SectionResult] = []
    article = ""
    article_count = 0
    for index, block in enumerate(parser.blocks):
        if not block.anchor:
            match = ARTICLE_RE.match(block.text)
            if match:
                article = block.text
                article_count += 1
            continue
        match = SECTION_RE.match(block.text)
        if not match:
            continue
        number, section_title = match.groups()
        content = next((candidate.text for candidate in parser.blocks[index + 1 :] if candidate.text), "")
        if not content:
            continue
        guid = block.anchor
        section_results.append(
            SectionResult(
                guid=guid,
                number=number,
                title=_clean_text(section_title),
                hierarchy=tuple(value for value in ("Charter", article) if value),
                url=f"{urldefrag(page_url)[0]}#{guid}",
                text=content,
                history="",
            )
        )
    if not section_results:
        raise ECodeError("amlegal_extraction_failed", "AM Legal Charter page contained no sections", 4)
    return CharterResult(
        guid=urldefrag(page_url)[0].rstrip("/").split("/")[-1],
        title=title,
        url=page_url,
        article_count=article_count,
        sections=tuple(section_results),
    )


AMLEGAL_EXTRACT_SCRIPT = """
() => {
  const sections = Array.from(document.querySelectorAll('a[id^="JD_"][id*=".Sec."]')).map(anchor => {
    const heading = anchor.closest('.rbox');
    let content = heading && heading.nextElementSibling;
    while (content && !content.classList.contains('rbox')) content = content.nextElementSibling;
    return {guid: anchor.id, heading: heading ? heading.innerText : '', text: content ? content.innerText : ''};
  });
  const next = Array.from(document.querySelectorAll('a')).find(link => link.innerText.trim() === 'Next Doc');
  const children = Array.from(document.querySelectorAll('a[data-orig-doc-id]'))
    .map(link => link.href).filter(Boolean);
  return {title: document.title, sections, next: next ? next.href : '', children};
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
            charter_href = page.locator('a').filter(has_text=re.compile("charter", re.I)).first.get_attribute("href")
            if not charter_href:
                raise ECodeError("amlegal_charter_not_found", "AM Legal overview did not expose a Charter document", 5)
            current = page.url if charter_href.startswith("/") else charter_href
            base = overview_url.split("/codes/", 1)[0]
            if charter_href.startswith("/"):
                current = base + charter_href
            charter_url = current
            sections: dict[str, SectionResult] = {}
            title = "Charter"
            visited: set[str] = set()
            pending = [charter_url]
            article_count = 0
            for _ in range(80):
                if not pending:
                    break
                current = pending.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                page.goto(current, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(3000)
                payload = page.evaluate(AMLEGAL_EXTRACT_SCRIPT)
                if not isinstance(payload, dict):
                    raise ECodeError("amlegal_extraction_failed", "AM Legal returned an invalid page payload", 4)
                page_result = parse_amlegal_payload(payload, current)
                for child in page_result["children"]:
                    if child not in visited and child not in pending:
                        pending.append(child)
                title = page_result["title"] or title
                article_count += page_result["article_count"]
                sections.update(page_result["sections"])
                time.sleep(1.0)
            if not sections:
                raise ECodeError("amlegal_extraction_failed", "AM Legal Charter contained no sections", 4)
            return CharterResult(charter_url.rstrip("/").split("/")[-1], title, charter_url, article_count, tuple(sections.values()))
        finally:
            page.close()


def parse_amlegal_payload(payload: dict, page_url: str) -> dict[str, object]:
    raw_sections = payload.get("sections")
    if not isinstance(raw_sections, list):
        raise ECodeError("amlegal_extraction_failed", "AM Legal page sections were invalid", 4)
    sections: dict[str, SectionResult] = {}
    article_count = 0
    for raw in raw_sections:
        if not isinstance(raw, dict) or not isinstance(raw.get("guid"), str):
            continue
        heading = _clean_text(str(raw.get("heading", "")))
        match = SECTION_RE.match(heading)
        if not match or not str(raw.get("text", "")).strip():
            continue
        number, section_title = match.groups()
        sections[raw["guid"]] = SectionResult(raw["guid"], number, _clean_text(section_title), ("Charter",), f"{page_url}#{raw['guid']}", _clean_text(str(raw["text"])), "")
    children = payload.get("children")
    if not isinstance(children, list):
        children = []
    return {"title": str(payload.get("title") or "Charter"), "sections": sections, "article_count": article_count, "next": str(payload.get("next") or ""), "children": tuple(str(child) for child in children if isinstance(child, str))}
