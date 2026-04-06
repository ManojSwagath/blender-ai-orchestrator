# Blender AI Orchestrator 🎨🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/ManojSwagath/blender-ai-orchestrator)

Fully autonomous Blender scene creation system using GitHub Copilot CLI's multi-agent orchestration.

## ✨ Features

- **🎯 Autonomous Workflow**: Automatically builds complete Blender scenes from text descriptions
- **🤖 7 Specialized Agents**: Each agent handles a specific aspect of scene creation
- **⚡ Parallel Team Mode**: Independent subagent tasks are generated in parallel for higher throughput
- **🧠 Brainstorm Variants**: Prompts asking for variants automatically trigger concept brainstorming and best-option selection
- **📐 Structured Waves**: Geometry → (Prop + Material) → (Rigging + Material Touch-up) → Export → QA
- **🔄 Auto-Retry**: Intelligent error handling with automatic retries
- **✅ Quality Assurance**: Built-in validation and issue fixing

## 🏗️ Architecture

The system uses a **multi-agent orchestration** pattern:

```
User Prompt
     ↓
[Orchestrator Agent]
     ↓
Geometry
    ↓
Parallel Wave 1: Prop + Material
    ↓
Parallel Wave 2: Rigging + Material Touch-up
    ↓
Export
    ↓
QA Loop
    ↓
Complete Scene
```

## 🚀 Quick Start

### Prerequisites

- Blender 3.6+ (in PATH or set `BLENDER_PATH`)
- GitHub Copilot CLI with multi-agent support
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ManojSwagath/blender-ai-orchestrator.git
cd blender-ai-orchestrator
```

2. **Install agents globally:**
```bash
# Windows
Copy-Item .github\agents\*.agent.md $env:USERPROFILE\.copilot\agents\

# macOS/Linux
cp .github/agents/*.agent.md ~/.copilot/agents/
```

3. **Restart your CLI** to load the agents

### Usage

**Method 1: Direct CLI Command**
```bash
copilot --agent=blender-orchestrator --prompt "Create a 2-floor house with windows and doors"
```

**Method 2: Interactive Session**
```bash
copilot
# Then type:
/agent
# Select "blender-orchestrator"
```

**Method 3: Natural Language**
```bash
copilot
# Then type:
"Ask the blender-orchestrator to create a medieval castle"
```

## 🎭 Available Agents

| Agent | Description | Model |
|-------|-------------|-------|
| **blender-orchestrator** | Main coordinator | Gemini 3.1 Pro |
| **geometry** | Creates structures | GPT-5.3 Codex |
| **material** | Applies colors/materials | GPT-5.3 Codex |
| **prop** | Creates doors, windows, objects | GPT-5.3 Codex |
| **rigging** | Adds animation/interaction | GPT-5.3 Codex |
| **export** | Prepares and cleans scene | GPT-5.3 Codex |
| **qa** | Validates and fixes issues | Gemini 3.1 Pro |

## 📝 Example Prompts

- "Create a simple house with 2 floors"
- "Build a modern office space with desks and chairs"
- "Make a medieval tower with spiral stairs"
- "Create a cozy living room with furniture"
- "Build a sci-fi corridor with doors"
- "Create a house like granny has. Brainstorm and make another house model in Blender."

## 🔧 How It Works

1. **ORCHESTRATE** → Parses prompt, optionally brainstorms variants, selects one concept
2. **GEOMETRY** → Builds base structure (walls, floors, roof volumes)
3. **PARALLEL BUILD WAVE** → Calls **PROP** and **MATERIAL** in parallel, then executes in safe order
4. **PARALLEL POLISH WAVE** → Calls **RIGGING** and **MATERIAL TOUCH-UP** in parallel, then executes in safe order
5. **EXPORT** → Cleans and prepares scene
6. **QA LOOP** → Validates, fixes issues, and repeats until clean or pass limit reached

Each step:
- Gets Python (bpy) code from specialized agent
- Executes in Blender
- Validates result
- Auto-retries on failure (max 3 attempts per worker script)

## 🛠️ Tools

### run_blender.py

Simple utility for executing Blender scripts:

```python
import subprocess
import tempfile

def run_blender_script(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode("utf-8"))
        script_path = f.name
    
    result = subprocess.run(
        ["blender", "--background", "--python", script_path],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
```

## 📚 Documentation

- [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide
- [.github/agents/](.github/agents/) - Agent definitions

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blender Foundation** - Amazing open-source 3D software
- **GitHub Copilot Team** - Multi-agent support
- **OpenAI & Anthropic** - AI models powering the agents

## 📞 Support

- [GitHub Issues](https://github.com/ManojSwagath/blender-ai-orchestrator/issues)
- [Documentation](.github/agents/)

---

**Made with ❤️ by [Manoj Swagath](https://github.com/ManojSwagath)**
