# The list of tools and required arguments, to assist the LLM.
tool_schemas = [
    {
        "type": "function",
        "function": {
            "name": "int_add_new_skill",
            "description": "Add a new skill for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A short, filesystem-safe identifier for the skill, used directly as the filename. Use snake_case, capped at 2 words, unless the user explicitly specifies a different name."
                    },
                    "description": {
                        "type": "string",
                        "description": "A one-line summary of what the skill does and when to use it, shown in the skills index."
                    },
                    "content": {
                        "type": "string",
                        "description": "The full skill instructions in Markdown — the body the agent follows when the skill is invoked."
                    },
                },
                "required": ["name", "description", "content"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_get_skill_content",
            "description": "Load the full instructions for one of your available skills by name, so you can follow them.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Exact skill name from your available skills list."}
                },
                "required": ["name"],
                "additionalProperties": False,
            },  
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_add_new_workflow",
            "description": "Add a new workflow for the user. A workflow is a step-by-step process that chains together tools, skills, and/or MCP tools in order — write its content as an ordered list of steps, not free-form instructions. You still use your own judgment on how to carry out each individual step.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A short, filesystem-safe identifier for the workflow, used directly as the filename. Use snake_case, capped at 2 words, unless the user explicitly specifies a different name."
                    },
                    "description": {
                        "type": "string",
                        "description": "A one-line summary of what the workflow does and when to use it, shown in the workflows index."
                    },
                    "content": {
                        "type": "string",
                        "description": "The workflow's ordered steps in Markdown — a numbered list the agent follows in order when the workflow is invoked."
                    },
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Names of any skills this workflow's steps rely on. Documents the workflow's dependencies; never needs approval since loading a skill is already always allowed. Pass an empty list if none are used."
                    },
                    "workflows": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Names of any other already-existing workflows this workflow's steps rely on. Their steps are loaded alongside this workflow's whenever it's invoked, so list every one the steps mention. Pass an empty list if none are used."
                    },
                    "tools": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Names of any internal tools (besides the always-available ones) this workflow's steps are likely to need, e.g. int_fetch_content_from_url. Each one not already auto-run gets confirmed with the user right now, once, so this workflow can later be invoked without re-asking. Pass an empty list if none are needed."
                    },
                    "mcp_tools": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Names of any MCP-provided tools this workflow's steps are likely to need. MCP tools always need confirmation, so each one gets confirmed with the user right now, once. Pass an empty list if none are needed."
                    },
                },
                "required": ["name", "description", "content", "skills", "workflows", "tools", "mcp_tools"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_web_search_tool",
            "description": "Search the web for a query and get back page titles, URLs, and short snippets. Use this to find sources before fetching their full content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_fetch_content_from_url",
            "description": "Fetch and read the content of a specific URL, typically one found via the web search tool. Returns the page's main content as clean text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch."} 
                },
                "required": ["url"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_add_mcp_server",
            "description": "Connect a new MCP server so its tools become available to use. Validates the server and discovers its tools before saving. Provide either a url (HTTP server) or a command + args (stdio server) — never both.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A short identifier for the server, used as its config filename and to prefix its tool names. Use a single lowercase word, letters and digits only — no underscores, hyphens, or spaces (any will be stripped out), unless the user explicitly specifies a different name."
                    },
                    "url": {
                        "type": ["string", "null"],
                        "description": "The MCP server's HTTP endpoint URL. Set this for an HTTP server; leave null for a stdio server."
                    },
                    "command": {
                        "type": ["string", "null"],
                        "description": "The command to run for a stdio server (e.g. \"npx\"). Leave null for an HTTP server."
                    },
                    "args": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Arguments to pass to the command, for a stdio server (e.g. [\"-y\", \"@modelcontextprotocol/server-filesystem\", \"/some/dir\"]). Leave null for an HTTP server."
                    },
                },
                "required": ["name", "url", "command", "args"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_update_mcp_server",
            "description": "Refresh an already-connected MCP server's tools, in case they changed on the server side (added, removed, or edited). Re-discovers using the server's already-known URL, so it doesn't need to be supplied again.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The exact name of an already-connected MCP server."
                    },
                },
                "required": ["name"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
]