"""local-check driver (SK-4): build, test, start server, fetch, report.

Version 0.1 (Stage 2). Steps 1 and 2 are fully implemented. Step 3 starts the local server
only if the entry point ``youtube_mcp.server`` exists (Stage 3); otherwise it reports SKIP.
Step 4 (read-only fetch through an MCP session) is reported as SKIP until Stage 3.
A SKIP is never reported as PASS, and the overall result is INCOMPLETE while any step is skipped.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass

PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"
SERVER_MODULE = "youtube_mcp.server"
SERVER_START_SECONDS = 3


@dataclass(frozen=True)
class StepResult:
    number: int
    name: str
    status: str
    detail: str


def _tail(text: str, lines: int = 3) -> str:
    parts = [line for line in text.strip().splitlines() if line.strip()]
    return " | ".join(parts[-lines:]) if parts else ""


def _run(cmd: list[str], extra_env: dict[str, str] | None = None) -> tuple[int, str]:
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, env=env, timeout=900, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, f"{type(exc).__name__}: {exc}"
    return proc.returncode, proc.stdout + proc.stderr


def step_build() -> StepResult:
    code, out = _run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
    status = PASS if code == 0 else FAIL
    return StepResult(1, "Build project", status, _tail(out))


def step_tests() -> StepResult:
    code, out = _run(
        [sys.executable, "-m", "pytest", "-q"], {"YOUTUBE_PROVIDER_MODE": "fixture"}
    )
    status = PASS if code == 0 else FAIL
    return StepResult(2, "Run automated tests", status, _tail(out))


def _server_module_exists() -> bool:
    try:
        return importlib.util.find_spec(SERVER_MODULE) is not None
    except ModuleNotFoundError:
        return False


def step_server() -> StepResult:
    name = "Start local MCP server"
    if not _server_module_exists():
        return StepResult(3, name, SKIP, f"{SERVER_MODULE} not implemented yet (Stage 3)")
    env = dict(os.environ, YOUTUBE_PROVIDER_MODE="fixture")
    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", SERVER_MODULE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
    except OSError as exc:
        return StepResult(3, name, FAIL, f"could not start: {exc}")
    try:
        _, err = proc.communicate(timeout=SERVER_START_SECONDS)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return StepResult(3, name, PASS, f"server stayed up for {SERVER_START_SECONDS}s")
    return StepResult(3, name, FAIL, f"exited early with code {proc.returncode}: {_tail(err)}")


def step_fetch() -> StepResult:
    detail = "read-only get_video_details call over MCP not implemented yet (Stage 3)"
    return StepResult(4, "Invoke one read-only fetch tool", SKIP, detail)


def skipped(number: int, name: str, why: str) -> Callable[[], StepResult]:
    return lambda: StepResult(number, name, SKIP, why)


def build_steps(args: argparse.Namespace) -> list[Callable[[], StepResult]]:
    build = step_build
    tests = step_tests
    if args.skip_build:
        build = skipped(1, "Build project", "skipped by --skip-build")
    if args.skip_tests:
        tests = skipped(2, "Run automated tests", "skipped by --skip-tests")
    return [build, tests, step_server, step_fetch]


def overall(results: list[StepResult]) -> str:
    if any(r.status == FAIL for r in results):
        return FAIL
    if any(r.status == SKIP for r in results):
        return "INCOMPLETE"
    return PASS


def render_table(results: list[StepResult]) -> str:
    header = ("#", "Step", "Result", "Detail")
    rows = [(str(r.number), r.name, r.status, r.detail) for r in results]
    widths = [max(len(row[i]) for row in [header, *rows]) for i in range(3)]
    lines = []
    for row in [header, *rows]:
        cells = [row[i].ljust(widths[i]) for i in range(3)]
        lines.append(" | ".join(cells) + " | " + row[3])
    lines.insert(1, "-+-".join("-" * w for w in widths) + "-+-" + "-" * 6)
    lines.append(f"Step 5 - Overall: {overall(results)}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="local-check: verify this machine (SK-4)")
    parser.add_argument("--skip-build", action="store_true", help="skip pip install step")
    parser.add_argument("--skip-tests", action="store_true", help="skip pytest step")
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
    steps: list[Callable[[], StepResult]] | None = None,
) -> int:
    args = parse_args(argv)
    runners = steps if steps is not None else build_steps(args)
    results: list[StepResult] = []
    for index, runner in enumerate(runners, start=1):
        try:
            results.append(runner())
        # A crashing step must be reported as FAIL instead of aborting the whole report.
        except Exception as exc:  # noqa: BLE001
            detail = f"{type(exc).__name__}: {exc}"
            results.append(StepResult(index, f"Step {index}", FAIL, detail))
    print(render_table(results))
    return 1 if overall(results) == FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
