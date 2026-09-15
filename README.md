<pre>
███╗   ███╗ ██████╗ ███████╗███████╗███████╗████████╗
████╗ ████║██╔═══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
██╔████╔██║██║   ██║███████╗█████╗  █████╗     ██║
██║╚██╔╝██║██║   ██║╚════██║██╔══╝  ██╔══╝     ██║
██║ ╚═╝ ██║╚██████╔╝███████║██║     ███████╗   ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝   ╚═╝
</pre>

## Index

- [Description](#description)
- [Tech Stack](#tech-stack)
- [AI Stack](#ai-stack)
- [How it looks?](#how-it-looks)
- [Features](#features)
- [Project Structure](#project-structure)
- [Commands](#commands)
- [How to run the project?](#how-to-run-the-project)
- [License](#license)
- [Author](#author)

## Description

Mosfet is an LLM-powered agent that you extend by adding **Skills**, **Tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on, tools let it take action, and MCP servers connect it to external systems. The goal is to empower the LLM by simply dropping in more of these building blocks.

> **Status: early-stage / work in progress.** A model-agnostic chat agent that reasons through multiple tool calls before answering, extending itself with skills and MCP servers along the way, with guardrails checking what goes in and out.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

## AI Stack

- [OpenAI SDK](https://github.com/openai/openai-python)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Ollama](https://github.com/ollama/ollama)

## How it looks?

### CLI

<img width="858" height="655" alt="looks" src="https://github.com/user-attachments/assets/c7d9209f-0587-4014-b399-63b220910920" />

### Discord

<img width="812" height="925" alt="discord" src="https://github.com/user-attachments/assets/8452443c-f662-4bcf-8e72-fe919f6cf7d3" />

## Features

- Chat with the agent through your terminal or other communication channels.
- The agent can create skills for itself and reuse them whenever they apply.
- Connect the agent to MCP servers so it can use their tools.
- The agent can work through multiple steps on its own before giving you a final answer.
- See what the agent is doing as it works, like loading a skill or calling a tool, instead of just watching a spinner.
- Safe, read-only actions run automatically, but the agent asks for your permission before doing anything else.
- Messages are checked for sensitive personal information before they reach the LLM and before a response reaches you.
- Point the agent at whichever LLM provider and model you want, hosted or local, and change it anytime.
- Install once and run the agent from anywhere on your machine.

## Project Structure

```text
.
 src/
 ├── main.py                     # Entry point
 ├── llm.py                      # Guarded LLM entry point used by the agent loop
 ├── config_setup.py             # Guided setup/update for provider config and credentials
 ├── update.py                   # Updates the local install to the latest release
 ├── core/                       # Agent loop and skill/tool orchestration
 ├── adapters/                   # Per-provider LLM and web-search adapters behind common interfaces
 │    ├── llm_providers/
 │    └── web_search_providers/
 ├── config/                     # Provider selection, seed messages, and shared paths
 ├── extensions/                 # Skills, tools, and MCP servers available to the agent
 │    ├── mcp/
 │    ├── skills/
 │    └── tools/
 ├── guardrails/                 # Content checks run on messages going into and out of the LLM
 ├── ui/                         # Front-ends: terminal chat loop and Discord bot
 └── utils/                      # Shared helpers used across the codebase
 scripts/
 ├── install.sh                  # Installs Mosfet into ~/.mosfet and adds `mosfet` to PATH
 ├── publish_docker_beta.sh      # Builds and pushes the beta Docker image
 └── restart_docker.sh           # Restarts the local Mosfet container
```

## Commands

Every option below runs the same commands, just with a different prefix in place of `mosfet`. The commands themselves:

Set up or update your provider, model, and web search provider, prompting for whichever credentials you need. Run it again anytime to change your setup. Rarely-changed settings like Ollama's server URL or Anthropic's response length cap live in `src/config/advanced_providers.py` if you ever need to adjust them.

```bash
mosfet config
```

Start chatting. Defaults to the terminal.

```bash
mosfet
```

Start chatting on Discord. Runs in the background by default so you don't need to keep a terminal open for it.

```bash
mosfet discord              # start in the background
mosfet discord --foreground # attach to this terminal instead
mosfet discord --stop       # stop a background bot
```

Update Mosfet to the latest release. Only works for the install-script setup below (Option 1); Docker installs update via `docker compose pull && docker compose up -d` instead.

```bash
mosfet update
```

## How to run the project?

### Option 1: Install script

```bash
bash <(curl -fsSL https://mosfet.shahtech.info)
```

This clones the latest Mosfet release, sets up an isolated Python environment, and installs a `mosfet` command on your `PATH`. Once it finishes, run the commands in [Commands](#commands) as they are.

### Option 2: Manual setup (for development)

1. Clone the repo:

   ```bash
   git clone git@github.com:busycaesar/Mosfet.git
   cd Mosfet
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r req.txt
   ```

3. Run the commands in [Commands](#commands), replacing `mosfet` with `python3 src/main.py`, e.g.:

   ```bash
   python3 src/main.py config
   python3 src/main.py
   ```

### Option 3: Docker

1. Create a `docker-compose.yml` in the project directory:

   ```yaml
   services:
     mosfet-app:
       image: busycaesar/mosfet:latest
       volumes:
         - ./mosfet.config.json:/app/mosfet.config.json
         - ./.env:/app/.env
   ```

2. Create `mosfet.config.json` and `.env` in the same directory (an empty `.env` and a `mosfet.config.json` containing `{}` are enough to start):

   ```bash
   echo '{}' > mosfet.config.json
   touch .env
   ```

3. Start the container:

   ```bash
   docker compose up -d
   ```

4. Run the commands in [Commands](#commands), prefixing `mosfet` with `docker compose exec -it mosfet-app`, e.g.:

   ```bash
   docker compose exec -it mosfet-app mosfet config
   docker compose exec -it mosfet-app mosfet
   ```

   `mosfet.config.json` and `.env` are bind-mounted, so anything `mosfet config` writes is saved straight back to those files in your project directory.

## License

[MIT](LICENSE)

## Author

[Dev J. Shah](https://github.com/busycaesar)
</pre>