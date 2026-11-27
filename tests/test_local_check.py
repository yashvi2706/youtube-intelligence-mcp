"""Unit tests for scripts/local_check.py (SK-4). No subprocess, pip or network is used."""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest

_SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "local_check.py"
_SPEC = importlib.util.spec_from_file_location("local_check", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
local_check = importlib.util.module_from_spec(_SPEC)
sys.modules["local_check"] = local_check
_SPEC.loader.exec_module(local_check)

StepResult = local_check.StepResult


def _ok(number: int) -> StepResult:
    return StepResult(number, f"step {number}", local_check.PASS, "ok")


def test_overall_pass_when_all_pass() -> None:
    assert local_check.overall([_ok(1), _ok(2)]) == local_check.PASS


def test_overall_incomplete_when_a_step_is_skipped() -> None:
    skipped = StepResult(3, "server", local_check.SKIP, "not yet")
    assert local_check.overall([_ok(1), skipped]) == "INCOMPLETE"


def test_overall_fail_beats_skip() -> None:
    failed = StepResult(2, "tests", local_check.FAIL, "boom")
    skipped = StepResult(3, "server", local_check.SKIP, "not yet")
    assert local_check.overall([_ok(1), failed, skipped]) == local_check.FAIL


def test_render_table_lists_every_step_and_overall() -> None:
    table = local_check.render_table([_ok(1), _ok(2)])
    assert "step 1" in table and "step 2" in table
    assert "Step 5 - Overall: PASS" in table


def test_server_step_skips_when_entry_point_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(local_check, "_server_module_exists", lambda: False)
    result = local_check.step_server()
    assert result.status == local_check.SKIP
    assert result.number == 3


def test_fetch_step_is_never_reported_as_pass() -> None:
    assert local_check.step_fetch().status == local_check.SKIP


def test_main_returns_nonzero_when_a_step_fails(capsys: pytest.CaptureFixture[str]) -> None:
    def failing() -> StepResult:
        return StepResult(1, "build", local_check.FAIL, "pip error")

    assert local_check.main([], steps=[failing]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_main_returns_zero_when_only_skips(capsys: pytest.CaptureFixture[str]) -> None:
    def passing() -> StepResult:
        return _ok(1)

    def skipped() -> StepResult:
        return StepResult(3, "server", local_check.SKIP, "not yet")

    assert local_check.main([], steps=[passing, skipped]) == 0
    assert "INCOMPLETE" in capsys.readouterr().out


def test_main_reports_a_crashing_step_as_fail(capsys: pytest.CaptureFixture[str]) -> None:
    def crash() -> StepResult:
        raise RuntimeError("unexpected")

    assert local_check.main([], steps=[crash]) == 1
    assert "RuntimeError" in capsys.readouterr().out
