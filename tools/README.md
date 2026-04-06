# Blender MCP Server Setup & Troubleshooting

## 1) Overview

This project expects a **running Blender MCP server** so tools can reliably connect to Blender before executing scene code.  
By default, connectivity checks target **`localhost:9876`**.

---

## 2) Requirements

- **Blender 3.6+**
- **Blender MCP addon** installed and enabled in Blender
- MCP server listening on **port `9876`** (or a custom port you pass explicitly)

---

## 3) Quick Start

1. Install and open **Blender 3.6+**.
2. Install/enable the **MCP addon** in Blender (`Edit → Preferences → Add-ons`).
3. In the addon panel, start the MCP server.
4. Confirm endpoint is `localhost:9876` (or note your custom host/port).
5. In this repo, run:

```bash
python tools/mcp_health.py --check
```

If successful, you should see `available: True` (human output) or `"server_available":true` (JSON mode).

---

## 4) Verifying Connectivity

Use the health checker:

```bash
python tools/mcp_health.py --check
```

For machine-readable output:

```bash
python tools/mcp_health.py --check --json
```

Exit codes:
- `0` = MCP server reachable
- `1` = MCP server not reachable

---

## 5) Usage Examples

### Single check
```bash
python tools/mcp_health.py --check
```

### Wait for server (startup race-safe)
```bash
python tools/mcp_health.py --wait --max-wait 60 --poll-interval 2
```

### JSON output (for scripts/CI)
```bash
python tools/mcp_health.py --check --json
```

### Custom endpoint
```bash
python tools/mcp_health.py --check --host 127.0.0.1 --port 9876
```

---

## 6) Troubleshooting

Below are common failure patterns, the error signals you may see, and how to recover.

### A) Port 9876 already in use

**Symptoms**
- Blender MCP fails to start, or starts on a different port.
- Health check may fail or connect to the wrong process.

**Check**
```powershell
Get-NetTCPConnection -LocalPort 9876 -ErrorAction SilentlyContinue
```

**Recovery**
1. Stop the conflicting process (or change its port).
2. Restart Blender MCP on `9876`, or pick a new port.
3. Re-run:
   ```bash
   python tools/mcp_health.py --check --port <your-port>
   ```

---

### B) Blender not found / not running

**Symptoms**
- Health output includes error code: `NO_BLENDER`
- Recovery text: *"No Blender process detected..."*
- `tools/run_blender.py` may return:
  - `"MCP server is unavailable."`
  - `"MCP server is unavailable. Start or fix the MCP server before running Blender code."`

**Recovery**
1. Launch Blender manually.
2. Enable MCP addon and start server.
3. Retry connectivity check.

---

### C) Addon not installed or not enabled

**Symptoms**
- Blender is open, but health check reports:
  - `CONNECTION_REFUSED` or `TIMEOUT`
- No MCP server endpoint appears in Blender UI.

**Recovery**
1. In Blender, open `Edit → Preferences → Add-ons`.
2. Install the MCP addon (if missing), then enable it.
3. Open addon panel and start MCP server.
4. Re-test with:
   ```bash
   python tools/mcp_health.py --check
   ```

---

### D) Firewall blocking localhost connection

**Symptoms**
- Health check error: `TIMEOUT`
- Blender appears running and addon enabled, but connection still fails.

**Recovery**
1. Allow Blender/Python local network access in firewall rules.
2. Ensure loopback/localhost traffic is not blocked.
3. Re-run health check.

---

### E) WSL / Docker networking mismatch

**Symptoms**
- Works on host OS, fails inside container/WSL.
- Connection attempts to `localhost:9876` time out/refuse.

**Recovery**
1. Use the host-reachable address instead of container-local localhost.
   - Docker (macOS/Windows): often `host.docker.internal`
   - WSL: use Windows host IP or configure mirrored/forwarded networking
2. Pass host/port explicitly:
   ```bash
   python tools/mcp_health.py --check --host <host-address> --port 9876
   ```
3. Confirm firewall permits cross-boundary connection.

---

## 7) Configuration

Recommended environment variables:

- `BLENDER_MCP_HOST` (default idea: `localhost`)
- `BLENDER_MCP_PORT` (default idea: `9876`)

Example:

```powershell
$env:BLENDER_MCP_HOST="localhost"
$env:BLENDER_MCP_PORT="9876"
python tools/mcp_health.py --check --host $env:BLENDER_MCP_HOST --port $env:BLENDER_MCP_PORT
```

```bash
export BLENDER_MCP_HOST=localhost
export BLENDER_MCP_PORT=9876
python tools/mcp_health.py --check --host "$BLENDER_MCP_HOST" --port "$BLENDER_MCP_PORT"
```

---

## 8) Integration with the Orchestrator

`tools/run_blender.py` performs a connectivity pre-check using `check_mcp_connectivity()` before running Blender code.

- If MCP is unavailable and `--require-mcp` is active (default), execution is blocked with explicit errors.
- If `--no-require-mcp` is used, execution continues with warnings.
- Responses include structured fields (`success`, `errors`, `warnings`, `connectivity`, `recovery_instructions`) for automation and debugging.

This ensures predictable behavior for both beginners (clear guidance) and advanced workflows (scriptable JSON + exit codes).
