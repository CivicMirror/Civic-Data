from scripts.ecode360.browser import (
    is_toc_response,
    launch_options,
    parse_embedded_toc,
    parse_embedded_toc_from_html,
    retry_sync,
)


def test_toc_response_match_is_exact() -> None:
    assert is_toc_response("https://ecode360.com/toc/EX1000", "EX1000")
    assert not is_toc_response("https://ecode360.com/toc/EX10001", "EX1000")
    assert not is_toc_response("https://other.example/toc/EX1000", "EX1000")


def test_retry_sync_retries_with_exponential_delays() -> None:
    calls = 0
    delays: list[float] = []

    def operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("temporary")
        return "ok"

    assert retry_sync(operation, max_retries=3, sleep=delays.append) == "ok"
    assert calls == 3
    assert delays == [1.0, 2.0]


def test_parse_embedded_toc_widget_payload() -> None:
    payload = '{"guid":"EX1000","type":"code","tocName":"Example","children":[]}'
    assert parse_embedded_toc(payload)["guid"] == "EX1000"


def test_parse_embedded_toc_from_completed_html() -> None:
    html = '<section id="code-toc-widget" data-toc-nodes="{&quot;guid&quot;:&quot;EX1000&quot;,&quot;type&quot;:&quot;code&quot;}"></section>'
    assert parse_embedded_toc_from_html(html)["guid"] == "EX1000"


def test_launch_options_disable_automation_detection() -> None:
    options = launch_options(True, "/usr/bin/chromium-browser")
    assert options["headless"] is True
    assert "--disable-blink-features=AutomationControlled" in options["args"]
    assert options["executable_path"] == "/usr/bin/chromium-browser"
