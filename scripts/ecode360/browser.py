from __future__ import annotations

from pathlib import Path
import time
from typing import Callable
from urllib.parse import urlparse

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from .charter import ExtractionResults, PageTarget, RawSection, normalize_page_sections, validate_toc
from .errors import ECodeError
from .models import DirectoryEntry

NAVIGATION_TIMEOUT_MS = 30_000
CONTENT_INTERVAL_SECONDS = 2.0


def is_toc_response(url: str, ecode_id: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme == "https"
        and (parsed.hostname or "").lower() in {"ecode360.com", "www.ecode360.com"}
        and parsed.path == f"/toc/{ecode_id}"
    )


def retry_sync(
    operation: Callable[[], object],
    max_retries: int = 3,
    sleep: Callable[[float], None] = time.sleep,
) -> object:
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
            if attempt < max_retries:
                sleep(float(2**attempt))
    assert last_error is not None
    raise last_error


DOM_EXTRACT_SCRIPT = """
() => Array.from(document.querySelectorAll('.section_content.content')).map((element) => {
  const historySelectors = '.history, .legislative-history, .history-note, .historyNote';
  const history = Array.from(element.querySelectorAll(historySelectors))
    .map((item) => item.innerText || '').join('\\n').trim();
  const copy = element.cloneNode(true);
  copy.querySelectorAll(historySelectors).forEach((item) => item.remove());
  return {
    guid: (element.id || '').replace(/_content$/, ''),
    text: (copy.innerText || '').trim(),
    history,
  };
})
"""


class ECodeBrowser:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._last_content_navigation = 0.0

    def __enter__(self) -> "ECodeBrowser":
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context(
            locale="en-US",
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
            ),
        )
        self._context.set_default_timeout(NAVIGATION_TIMEOUT_MS)
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if self._context is not None:
            self._context.close()
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._context = None
        self._browser = None
        self._playwright = None

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            raise RuntimeError("ECodeBrowser must be used as a context manager")
        return self._context

    def _new_page(self) -> Page:
        page = self.context.new_page()
        page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
        return page

    def fetch_toc(self, source: DirectoryEntry) -> dict:
        def attempt() -> dict:
            page = self._new_page()
            try:
                with page.expect_response(
                    lambda response: is_toc_response(response.url, source.ecode_id),
                    timeout=NAVIGATION_TIMEOUT_MS,
                ) as response_info:
                    page.goto(source.code_url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
                response = response_info.value
                if response.status >= 400:
                    raise ECodeError("ecode_navigation_failed", f"TOC request returned HTTP {response.status}", 4)
                try:
                    payload = response.json()
                except Exception as exc:
                    raise ECodeError("toc_invalid", "TOC response was not JSON", 4) from exc
                return validate_toc(payload, source.ecode_id)
            except ECodeError:
                raise
            except Exception as exc:
                raise ECodeError("ecode_navigation_failed", f"Unable to retrieve eCode360 TOC: {exc}", 4) from exc
            finally:
                page.close()

        return retry_sync(attempt)  # type: ignore[return-value]

    def _wait_between_content_pages(self) -> None:
        elapsed = time.monotonic() - self._last_content_navigation
        if elapsed < CONTENT_INTERVAL_SECONDS:
            time.sleep(CONTENT_INTERVAL_SECONDS - elapsed)

    def _extract_once(self, target: PageTarget) -> tuple[tuple[RawSection, ...], tuple[RawSection, ...]]:
        page = self._new_page()
        try:
            self._wait_between_content_pages()
            page.goto(f"https://ecode360.com/{target.guid}", wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
            self._last_content_navigation = time.monotonic()
            primary = normalize_page_sections(page.evaluate(DOM_EXTRACT_SCRIPT))
            missing = set(target.section_guids) - {section.guid for section in primary}
            fallback: list[RawSection] = []
            for guid in target.section_guids:
                if guid not in missing:
                    continue
                self._wait_between_content_pages()
                page.goto(f"https://ecode360.com/{guid}", wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
                self._last_content_navigation = time.monotonic()
                fallback.extend(normalize_page_sections(page.evaluate(DOM_EXTRACT_SCRIPT)))
            return primary, tuple(fallback)
        except ECodeError:
            raise
        except Exception as exc:
            raise ECodeError("ecode_navigation_failed", f"Unable to extract eCode360 content: {exc}", 4) from exc
        finally:
            page.close()

    def extract_sections(self, targets: tuple[PageTarget, ...]) -> ExtractionResults:
        primary: list[RawSection] = []
        fallback: list[RawSection] = []
        for target in targets:
            try:
                target_primary, target_fallback = retry_sync(lambda: self._extract_once(target))  # type: ignore[misc]
            except ECodeError:
                raise
            except Exception as exc:
                raise ECodeError("ecode_navigation_failed", str(exc), 4) from exc
            primary.extend(target_primary)
            fallback.extend(target_fallback)
        return ExtractionResults(tuple(primary), tuple(fallback))
