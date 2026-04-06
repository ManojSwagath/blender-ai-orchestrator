from __future__ import annotations

import argparse
import csv
import json
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9876

ERROR_CONNECTION_REFUSED = "CONNECTION_REFUSED"
ERROR_TIMEOUT = "TIMEOUT"
ERROR_NO_BLENDER = "NO_BLENDER"


def _timestamp_iso8601() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_port_open(host: str, port: int, timeout: float) -> tuple[bool, str | None, int]:
    """
    Try to open a TCP connection and measure response time.
    Returns: (is_open, error_code, response_time_ms)
    """
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return True, None, elapsed_ms
    except socket.timeout:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return False, ERROR_TIMEOUT, elapsed_ms
    except ConnectionRefusedError:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return False, ERROR_CONNECTION_REFUSED, elapsed_ms
    except OSError as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        if getattr(exc, "errno", None) in {111, 61, 10061}:
            return False, ERROR_CONNECTION_REFUSED, elapsed_ms
        return False, ERROR_TIMEOUT, elapsed_ms


def get_blender_processes() -> list[str]:
    """
    Detect Blender processes via platform-specific process listing.
    Returns a list of process descriptions.
    """
    system_name = platform.system().lower()
    processes: list[str] = []

    try:
        if system_name == "windows":
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return []

            reader = csv.reader(result.stdout.splitlines())
            for row in reader:
                if not row:
                    continue
                image_name = row[0].strip().lower()
                if "blender" in image_name:
                    processes.append(" | ".join(item.strip() for item in row if item.strip()))
        else:
            result = subprocess.run(
                ["ps", "-ax", "-o", "pid=,comm=,args="],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return []

            for line in result.stdout.splitlines():
                lowered = line.lower()
                if "blender" in lowered:
                    processes.append(line.strip())
    except (OSError, subprocess.SubprocessError):
        return []

    return processes


def generate_health_report(
    server_available: bool,
    host: str,
    port: int,
    response_time_ms: int,
    blender_processes: list[str],
    error: str | None,
) -> dict[str, Any]:
    if server_available:
        recovery = "MCP server is reachable. No recovery action required."
    elif error == ERROR_NO_BLENDER:
        recovery = (
            "No Blender process detected. Start Blender with the MCP server enabled, "
            f"then verify it listens on {host}:{port}."
        )
    elif error == ERROR_CONNECTION_REFUSED:
        recovery = (
            f"Connection refused on {host}:{port}. Ensure Blender MCP is started and "
            "bound to the expected port."
        )
    elif error == ERROR_TIMEOUT:
        recovery = (
            f"Connection timed out to {host}:{port}. Verify local firewall/network rules "
            "and Blender MCP server startup status."
        )
    else:
        recovery = "Unknown error. Verify Blender and MCP server configuration."

    return {
        "server_available": server_available,
        "host": host,
        "port": port,
        "response_time_ms": response_time_ms,
        "blender_processes": blender_processes,
        "error": error,
        "recovery_instructions": recovery,
        "timestamp": _timestamp_iso8601(),
    }


def check_mcp_server_health(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = 1.5,
    retries: int = 3,
    initial_backoff: float = 0.25,
    backoff_multiplier: float = 2.0,
    max_backoff: float = 2.0,
) -> dict[str, Any]:
    blender_processes = get_blender_processes()
    attempts = max(1, retries)
    backoff = max(0.0, initial_backoff)

    last_error: str | None = None
    last_response_time_ms = 0

    for attempt in range(attempts):
        is_open, error_code, response_time_ms = check_port_open(host, port, timeout)
        last_error = error_code
        last_response_time_ms = response_time_ms

        if is_open:
            return generate_health_report(
                server_available=True,
                host=host,
                port=port,
                response_time_ms=response_time_ms,
                blender_processes=blender_processes,
                error=None,
            )

        if attempt < attempts - 1 and backoff > 0:
            time.sleep(backoff)
            backoff = min(backoff * backoff_multiplier, max_backoff)

    if not blender_processes:
        last_error = ERROR_NO_BLENDER

    return generate_health_report(
        server_available=False,
        host=host,
        port=port,
        response_time_ms=last_response_time_ms,
        blender_processes=blender_processes,
        error=last_error,
    )


def check_mcp_connectivity(timeout_seconds: float = 1.5) -> dict[str, Any]:
    report = check_mcp_server_health(timeout=timeout_seconds, retries=1)
    return {
        "available": report["server_available"],
        "host": report["host"],
        "port": report["port"],
        "timeout_seconds": timeout_seconds,
        "checked_at_utc": report["timestamp"],
        "error": report["error"],
        "response_time_ms": report["response_time_ms"],
    }


def get_recovery_instructions(connectivity_status: dict[str, Any]) -> list[str]:
    host = connectivity_status.get("host", DEFAULT_HOST)
    port = connectivity_status.get("port", DEFAULT_PORT)
    error = connectivity_status.get("error")

    instructions = [
        "Ensure Blender is running with MCP server enabled.",
        f"Verify MCP endpoint settings (host={host}, port={port}).",
    ]
    if error:
        instructions.append(f"Last connectivity error: {error}.")
    instructions.append("If Blender was just started, wait a few seconds and retry.")
    return instructions


def wait_for_server(
    max_wait: float,
    poll_interval: float,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = 1.5,
    retries: int = 2,
) -> dict[str, Any]:
    deadline = time.monotonic() + max(0.0, max_wait)
    interval = max(0.1, poll_interval)

    while True:
        report = check_mcp_server_health(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
        )
        if report["server_available"]:
            return report

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return report

        time.sleep(min(interval, remaining))


def _format_human_report(report: dict[str, Any]) -> str:
    blender_count = len(report["blender_processes"])
    lines = [
        "Blender MCP Health Check",
        f"  available: {report['server_available']}",
        f"  endpoint: {report['host']}:{report['port']}",
        f"  response_time_ms: {report['response_time_ms']}",
        f"  blender_processes: {blender_count}",
        f"  error: {report['error']}",
        f"  recovery: {report['recovery_instructions']}",
        f"  timestamp: {report['timestamp']}",
    ]
    if blender_count:
        lines.append("  process_list:")
        for item in report["blender_processes"]:
            lines.append(f"    - {item}")
    return "\n".join(lines)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Blender MCP server connectivity on localhost:9876."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Run a single health check (default).")
    mode.add_argument("--wait", action="store_true", help="Wait until server becomes available.")

    parser.add_argument("--json", action="store_true", help="Print compact JSON output.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host to check (default: localhost).")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to check (default: 9876).")
    parser.add_argument("--timeout", type=float, default=1.5, help="Socket timeout in seconds.")
    parser.add_argument("--retries", type=int, default=3, help="Retries for each health check.")
    parser.add_argument("--max-wait", type=float, default=60.0, help="Max wait seconds for --wait mode.")
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Polling interval for --wait mode.")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    if args.wait:
        report = wait_for_server(
            max_wait=args.max_wait,
            poll_interval=args.poll_interval,
            host=args.host,
            port=args.port,
            timeout=args.timeout,
            retries=max(1, args.retries),
        )
    else:
        report = check_mcp_server_health(
            host=args.host,
            port=args.port,
            timeout=args.timeout,
            retries=max(1, args.retries),
        )

    if args.json:
        print(json.dumps(report, separators=(",", ":"), ensure_ascii=False))
    else:
        print(_format_human_report(report))

    return 0 if report["server_available"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
