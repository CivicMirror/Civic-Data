import json

from scripts.ecode360 import __main__ as cli
from scripts.ecode360.charter import ExtractionResults, RawSection
from scripts.ecode360.errors import ECodeError
from scripts.ecode360.models import DirectoryEntry


def _install_success_fakes(monkeypatch, headed_values: list[bool] | None = None) -> None:
    source = DirectoryEntry("Town of Example", "MA", "Sample County", "EX1000", "https://ecode360.com/EX1000")
    toc = {
        "type": "code",
        "guid": "EX1000",
        "tocName": "Example",
        "children": [
            {"type": "chapter", "guid": "c1", "title": "Charter", "children": [
                {"type": "article", "guid": "a1", "title": "Article 1", "children": [
                    {"type": "section", "guid": "s1", "number": "1-1", "title": "Purpose", "children": []}
                ]}
            ]}
        ],
    }

    class FakeBrowser:
        def __init__(self, headless: bool) -> None:
            if headed_values is not None:
                headed_values.append(not headless)

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def fetch_toc(self, _source):
            return toc

        def extract_sections(self, _targets):
            return ExtractionResults((RawSection("s1", "Purpose text.", ""),), ())

    monkeypatch.setattr(cli, "fetch_directory", lambda: "directory")
    monkeypatch.setattr(cli, "parse_directory", lambda _html: (source,))
    monkeypatch.setattr(cli, "ECodeBrowser", FakeBrowser)


def test_main_emits_one_success_document(monkeypatch, capsys) -> None:
    _install_success_fakes(monkeypatch)

    assert cli.main(["--municipality", "Example", "--state", "MA"]) == 0
    captured = capsys.readouterr()
    document = json.loads(captured.out)
    assert document["status"] == "success"
    assert document["charter"]["section_count"] == 1
    assert "Resolving Example, MA" in captured.err


def test_main_emits_known_error_as_json(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_directory", lambda: (_ for _ in ()).throw(ECodeError("directory_fetch_failed", "offline", 3)))

    assert cli.main(["--municipality", "Example", "--state", "MA"]) == 3
    captured = capsys.readouterr()
    assert json.loads(captured.out)["error"]["code"] == "directory_fetch_failed"
    assert "offline" not in captured.err


def test_main_converts_unexpected_error_without_traceback(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_directory", lambda: (_ for _ in ()).throw(RuntimeError("secret traceback")))

    assert cli.main(["--municipality", "Example", "--state", "MA"]) == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out)["error"]["code"] == "internal_error"
    assert "secret traceback" not in captured.out


def test_main_requires_both_request_arguments(capsys) -> None:
    assert cli.main([]) == 2
    document = json.loads(capsys.readouterr().out)
    assert document["error"]["code"] == "invalid_cli_input"


def test_execute_passes_headed_flag_to_browser(monkeypatch) -> None:
    headed_values: list[bool] = []
    _install_success_fakes(monkeypatch, headed_values)
    cli.execute("Example", "MA", headed=True)
    assert headed_values == [True]
