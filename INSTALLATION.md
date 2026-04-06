# Blender AI Orchestrator - Installation Complete! ✅

## 📍 Location

All 7 agents are now installed globally at:
```
C:\Users\amano\.copilot\agents\
```

## 🤖 Available Agents

1. **blender-orchestrator** - Main coordinator (use this one!)
2. **geometry** - Creates structures
3. **material** - Applies colors/materials
4. **prop** - Creates doors, windows, objects
5. **rigging** - Adds animation/interaction
6. **export** - Prepares and cleans scene
7. **qa** - Validates and fixes issues

## 🚀 How to Use

### Method 1: Direct CLI Command
```bash
copilot --agent=blender-orchestrator --prompt "Create a 2-floor house with windows and doors"
```

### Method 2: Slash Command in Session
```bash
copilot
# Then in the session:
/agent
# Select "blender-orchestrator" from the list
```

### Method 3: Natural Language
```bash
copilot
# Then type:
"Ask the blender-orchestrator to create a medieval castle"
```

## 📝 Example Prompts

- "Create a simple house with 2 floors"
- "Build a room with furniture"
- "Make a medieval tower with stairs"
- "Create an office space with desks and chairs"

## ⚙️ Next Steps

1. **Restart your CLI** - Exit and reopen your terminal to load the agents
2. **Test it** - Try: `copilot --agent=blender-orchestrator --prompt "Create a simple cube with red material"`
3. **Check Blender is accessible** - Ensure Blender is in your PATH or set BLENDER_PATH

## 🔧 Workflow

The orchestrator will:
1. **GEOMETRY** → Build structure
2. **MATERIAL** → Apply colors
3. **PROP** → Add objects
4. **RIGGING** → Add interactions
5. **EXPORT** → Clean scene
6. **QA** → Validate everything

## 📂 Repository vs Global

- **Global** (`~/.copilot/agents/`) - ✅ Installed (use anywhere!)
- **Repository** (`blender-ai-orchestrator/.github/agents/`) - Available for team sharing

---

**Ready to use!** Restart your CLI and start creating Blender scenes autonomously! 🎨
