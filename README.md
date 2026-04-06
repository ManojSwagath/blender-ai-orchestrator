# Blender AI Orchestrator

A multi-agent orchestration system for automating complex Blender workflows using specialized AI agents.

## Overview

This repository contains a collection of specialized AI agents that work together to automate Blender 3D content creation. The system uses an orchestration pattern where a main coordinator agent delegates tasks to specialized agents, each responsible for specific aspects of 3D content creation.

## Architecture

### Agent System

The orchestrator uses a multi-agent architecture with the following specialized agents:

- **🎯 Blender Orchestrator** (`blender-orchestrator.agent.md`) - Main coordination agent
- **📐 Geometry Agent** (`geometry.agent.md`) - 3D modeling and mesh operations
- **🎨 Material Agent** (`material.agent.md`) - Materials, shaders, and textures
- **🎭 Prop Agent** (`prop.agent.md`) - Asset generation and scene props
- **🦴 Rigging Agent** (`rigging.agent.md`) - Character rigging and animation setup
- **📦 Export Agent** (`export.agent.md`) - Scene export and rendering
- **✅ QA Agent** (`qa.agent.md`) - Quality assurance and validation

### Agent Workflow

```
User Request
     ↓
Orchestrator Agent
     ↓
  ┌──┴──┬──────┬────────┬─────────┬────────┐
  ↓     ↓      ↓        ↓         ↓        ↓
Geometry Material Prop Rigging Export    QA
 Agent   Agent  Agent  Agent    Agent  Agent
  ↓     ↓      ↓        ↓         ↓        ↓
  └──┬──┴──────┴────────┴─────────┴────────┘
     ↓
Final Result
```

## Features

- **Task Decomposition**: Automatically breaks down complex requests into manageable subtasks
- **Specialized Execution**: Each agent focuses on its domain of expertise
- **Quality Assurance**: Built-in validation and quality checks
- **Asset Integration**: Support for AI-generated assets (Hyper3D, Hunyuan3D) and asset libraries (Polyhaven, Sketchfab)
- **Multi-format Export**: Export to FBX, GLTF/GLB, OBJ, USD, and more

## Getting Started

### Prerequisites

- Blender 3.6 or higher
- Python 3.10+
- GitHub Copilot with multi-agent support

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/blender-ai-orchestrator.git
cd blender-ai-orchestrator
```

2. Set up Blender path (optional):
```bash
export BLENDER_PATH="/path/to/blender"
```

### Usage

The agents are designed to work with GitHub Copilot's multi-agent system. Simply reference the agents in your Copilot conversations:

```
@blender-orchestrator Create a medieval castle scene with materials and lighting
```

The orchestrator will:
1. Analyze the request
2. Delegate to appropriate specialized agents
3. Coordinate the workflow
4. Validate the final result

## Tools

### run_blender.py

Utility script for running Blender with Python scripts:

```bash
python tools/run_blender.py script.py -f scene.blend --background
```

**Options:**
- `-f, --file`: Blend file to open
- `-b, --background`: Run in background mode
- `--blender`: Path to Blender executable

## Agent Capabilities

### Geometry Agent
- Primitive creation and mesh modeling
- Boolean operations and modifiers
- Mesh cleanup and optimization
- Model importing from asset libraries

### Material Agent
- PBR material setup
- Shader node networks
- Texture mapping and downloading
- HDRI environment configuration

### Prop Agent
- AI-powered 3D generation
- Asset library integration
- Scene composition and placement
- Collection management

### Rigging Agent
- Armature creation
- Weight painting and skinning
- IK/FK setup
- Animation preparation

### Export Agent
- Multi-format export (FBX, GLTF, OBJ, USD, STL)
- Render configuration
- Batch operations
- Format-specific optimization

### QA Agent
- Mesh validation
- Material verification
- Performance analysis
- Visual confirmation

## Configuration

Each agent is configured via its markdown file in `.github/agents/`. These files define:
- Agent role and responsibilities
- Available capabilities
- Tools and APIs
- Workflow procedures
- Best practices

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Blender Foundation for the amazing open-source 3D software
- GitHub Copilot team for multi-agent support
- Asset providers: Polyhaven, Sketchfab
- AI model providers: Hyper3D, Hunyuan3D

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing agent documentation in `.github/agents/`

---

**Note**: This is an orchestration framework for AI agents. It requires GitHub Copilot with multi-agent support to function.
