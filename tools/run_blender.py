import argparse
import json
import os
import subprocess
import sys
import tempfile

from mcp_health import check_mcp_connectivity, get_recovery_instructions


def run_blender_script(code, require_mcp=True):
    connectivity = check_mcp_connectivity()
    response = {
        "success": False,
        "require_mcp": require_mcp,
        "connectivity": connectivity,
        "warnings": [],
        "errors": [],
        "stdout": "",
        "stderr": "",
        "returncode": None,
    }

    if not connectivity["available"]:
        recovery = get_recovery_instructions(connectivity)
        if require_mcp:
            response["errors"].append(
                "MCP server is unavailable. Start or fix the MCP server before running Blender code."
            )
            response["recovery_instructions"] = recovery
            return response

        response["warnings"].append(
            "MCP server is unavailable; proceeding because --no-require-mcp was set."
        )
        response["recovery_instructions"] = recovery

    script_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as script_file:
            script_file.write(code.encode("utf-8"))
            script_path = script_file.name

        result = subprocess.run(
            ["blender", "--background", "--python", script_path],
            capture_output=True,
            text=True,
        )

        response["stdout"] = result.stdout
        response["stderr"] = result.stderr
        response["returncode"] = result.returncode
        response["success"] = result.returncode == 0

        if not response["success"] and not response["errors"]:
            response["errors"].append("Blender execution failed.")

        return response
    except Exception as exc:
        response["errors"].append(f"Unexpected error while running Blender: {exc}")
        return response
    finally:
        if script_path and os.path.exists(script_path):
            os.remove(script_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Blender Python code with MCP health checks.")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run MCP connectivity check and exit without executing Blender code.",
    )
    parser.add_argument(
        "--require-mcp",
        dest="require_mcp",
        action="store_true",
        help="Require MCP connectivity before execution (default).",
    )
    parser.add_argument(
        "--no-require-mcp",
        dest="require_mcp",
        action="store_false",
        help="Allow execution when MCP is unavailable.",
    )
    parser.set_defaults(require_mcp=True)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.check_only:
        connectivity = check_mcp_connectivity()
        success = connectivity["available"] or not args.require_mcp
        response = {
            "success": success,
            "check_only": True,
            "require_mcp": args.require_mcp,
            "connectivity": connectivity,
            "warnings": [],
            "errors": [],
            "recovery_instructions": get_recovery_instructions(connectivity),
        }

        if not connectivity["available"]:
            if args.require_mcp:
                response["errors"].append("MCP server is unavailable.")
            else:
                response["warnings"].append(
                    "MCP server is unavailable; this is allowed because --no-require-mcp is set."
                )

        print(json.dumps(response))
        return

    code = sys.stdin.read()
    if not code.strip():
        connectivity = check_mcp_connectivity()
        response = {
            "success": False,
            "check_only": False,
            "require_mcp": args.require_mcp,
            "connectivity": connectivity,
            "warnings": [],
            "errors": ["No Blender Python code provided on stdin."],
            "stdout": "",
            "stderr": "",
            "returncode": None,
            "recovery_instructions": get_recovery_instructions(connectivity),
        }
        print(json.dumps(response))
        return

    response = run_blender_script(code, require_mcp=args.require_mcp)
    response["check_only"] = False
    if "recovery_instructions" not in response:
        response["recovery_instructions"] = get_recovery_instructions(response["connectivity"])
    print(json.dumps(response))


if __name__ == "__main__":
    main()
