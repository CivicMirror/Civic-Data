from __future__ import annotations

from typing import Mapping


class ECodeError(Exception):
    """A user-facing, machine-readable failure."""

    def __init__(
        self,
        code: str,
        message: str,
        exit_status: int,
        candidates: tuple[Mapping[str, object], ...] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_status = exit_status
        self.candidates = candidates
