from pathlib import Path

SKILLS_DIR = "extensions/skills"
SKILLS_INDEX_FILE = "index.json"
CONFIG_FILE = "mosfet.config.json"
ENV_FILE = ".env"
MCP_SERVERS_DIR = "extensions/mcp/servers"
RUNTIME_DIR = "runtime"
DISCORD_LOG_FILE = "discord.log"
DISCORD_PID_FILE = "discord.pid"
SESSIONS_DIR = "sessions"

SKILLS_PATH = Path(__file__).resolve().parent.parent / SKILLS_DIR
MCP_SERVERS_PATH = Path(__file__).resolve().parent.parent / MCP_SERVERS_DIR
ROOT_PATH = Path(__file__).resolve().parent.parent.parent

SKILLS_INDEX_PATH = SKILLS_PATH / SKILLS_INDEX_FILE
CONFIG_PATH = ROOT_PATH / CONFIG_FILE
ENV_PATH = ROOT_PATH / ENV_FILE
RUNTIME_PATH = ROOT_PATH / RUNTIME_DIR
DISCORD_LOG_PATH = RUNTIME_PATH / DISCORD_LOG_FILE
DISCORD_PID_PATH = RUNTIME_PATH / DISCORD_PID_FILE
SESSIONS_PATH = RUNTIME_PATH / SESSIONS_DIR