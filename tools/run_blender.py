import subprocess
import tempfile
import sys

def run_blender_script(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode("utf-8"))
        script_path = f.name

    result = subprocess.run(
        ["blender", "--background", "--python", script_path],
        capture_output=True,
        text=True
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    return result.returncode == 0


if __name__ == "__main__":
    code = sys.stdin.read()
    success = run_blender_script(code)
    print({"success": success})
