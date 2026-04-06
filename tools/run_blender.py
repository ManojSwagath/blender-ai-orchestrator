#!/usr/bin/env python3
"""
Blender Runner Utility

This script provides utilities for running Blender with Python scripts
and managing Blender automation workflows.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional, List


def find_blender() -> Optional[str]:
    """
    Attempt to find Blender executable on the system.
    
    Returns:
        Path to Blender executable or None if not found
    """
    common_paths = [
        # Windows
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
        # macOS
        "/Applications/Blender.app/Contents/MacOS/Blender",
        # Linux
        "/usr/bin/blender",
        "/usr/local/bin/blender",
    ]
    
    # Check if BLENDER_PATH environment variable is set
    env_path = os.environ.get("BLENDER_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # Check common installation paths
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Try to find in PATH
    try:
        result = subprocess.run(
            ["which", "blender"] if sys.platform != "win32" else ["where", "blender"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    
    return None


def run_blender_script(
    script_path: str,
    blend_file: Optional[str] = None,
    background: bool = True,
    blender_path: Optional[str] = None,
    additional_args: Optional[List[str]] = None
) -> subprocess.CompletedProcess:
    """
    Run a Python script in Blender.
    
    Args:
        script_path: Path to the Python script to run
        blend_file: Optional .blend file to open
        background: Run Blender in background mode (no UI)
        blender_path: Path to Blender executable (auto-detected if None)
        additional_args: Additional arguments to pass to Blender
        
    Returns:
        CompletedProcess instance with execution results
    """
    if blender_path is None:
        blender_path = find_blender()
        if blender_path is None:
            raise RuntimeError(
                "Could not find Blender executable. "
                "Please set BLENDER_PATH environment variable or specify blender_path argument."
            )
    
    cmd = [blender_path]
    
    # Add blend file if specified
    if blend_file:
        cmd.append(blend_file)
    
    # Add background mode flag
    if background:
        cmd.append("--background")
    
    # Add Python flag
    cmd.extend(["--python", script_path])
    
    # Add additional arguments
    if additional_args:
        cmd.extend(additional_args)
    
    print(f"Running command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return result


def main():
    """CLI entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run Python scripts in Blender"
    )
    parser.add_argument(
        "script",
        help="Path to Python script to execute"
    )
    parser.add_argument(
        "-f", "--file",
        help="Blend file to open"
    )
    parser.add_argument(
        "-b", "--background",
        action="store_true",
        default=True,
        help="Run in background mode (default: True)"
    )
    parser.add_argument(
        "--blender",
        help="Path to Blender executable"
    )
    
    args = parser.parse_args()
    
    try:
        result = run_blender_script(
            script_path=args.script,
            blend_file=args.file,
            background=args.background,
            blender_path=args.blender
        )
        
        print("\n=== STDOUT ===")
        print(result.stdout)
        
        if result.stderr:
            print("\n=== STDERR ===")
            print(result.stderr)
        
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
