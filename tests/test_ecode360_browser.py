from scripts.ecode360.browser import is_toc_response, retry_sync


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
