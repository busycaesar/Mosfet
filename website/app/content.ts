// Single source of all page copy.

export type NavItem = { label: string; href: string };
export type Feature = { title: string; body: string };
export type Screenshot = { src: string; width: number; height: number; caption: string; alt: string };
export type InstallStep = { text?: string; code?: string };
export type InstallMethod = { id: string; label: string; steps: InstallStep[] };
export type FaqItem = { question: string; answer: string };

export const site = {
  name: "Mosfet",
  tagline: "Your own AI agent, on your own machine.",
  description: "Mosfet is an LLM-powered agent you extend with skills, tools, MCP servers and workflows. Drop in more building blocks, and it can do more.",
  status: "Early-stage · work in progress",
  installCommand: "bash <(curl -fsSL https://mosfet.shahtech.info)",
  githubUrl: "https://github.com/busycaesar/Mosfet",
  licenseUrl: "https://github.com/busycaesar/Mosfet/blob/Master/LICENSE",
  licenseName: "MIT",
  authorName: "Dev J. Shah",
  authorUrl: "https://github.com/busycaesar",
};

export const nav: NavItem[] = [
  { label: "Features", href: "#features" },
  { label: "Install", href: "#install" },
  { label: "FAQ", href: "#faq" },
];

// Verbatim copy of BANNER in src/config/constants.py (the six banner lines).
export const banner = `███╗   ███╗ ██████╗ ███████╗███████╗███████╗████████╗
████╗ ████║██╔═══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
██╔████╔██║██║   ██║███████╗█████╗  █████╗     ██║
██║╚██╔╝██║██║   ██║╚════██║██╔══╝  ██╔══╝     ██║
██║ ╚═╝ ██║╚██████╔╝███████║██║     ███████╗   ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝   ╚═╝`;

export const features: Feature[] = [
  { title: "Chat where you are", body: "Talk to the agent from your terminal or other communication channels. Each channel picks up its last conversation right where you left off." },
  { title: "Skills and workflows", body: "The agent can create skills for itself and reuse them whenever they apply. Save multi-step procedures as workflows and run them again whenever you need." },
  { title: "Connects to MCP servers", body: "Connect the agent to MCP servers so it can use their tools." },
  { title: "Works through it, visibly", body: "It works through multiple steps on its own before giving you a final answer, and shows what it's doing as it goes, like loading a skill or calling a tool." },
  { title: "Safe by default", body: "Safe, read-only actions run automatically, and it asks your permission before doing anything else. Messages are checked for sensitive personal information on the way to the LLM and on the way back." },
  { title: "Your model, your machine", body: "Point it at whichever LLM provider and model you want, hosted or local, and change it anytime. Install once and run it from anywhere on your machine." },
];

export const screenshots: Screenshot[] = [
  { src: "https://github.com/user-attachments/assets/c7d9209f-0587-4014-b399-63b220910920", width: 858, height: 655, caption: "CLI", alt: "Mosfet chatting in a terminal: the user's question, the agent's tool activity, and its answer." },
  { src: "https://github.com/user-attachments/assets/8452443c-f662-4bcf-8e72-fe919f6cf7d3", width: 812, height: 925, caption: "Discord", alt: "Mosfet replying to a direct message in Discord." },
];

// Each step: optional text, optional code (a command or file contents). Code matches README.md's "How to run the project?" section.
export const installMethods: InstallMethod[] = [
  { id: "script", label: "Install script", steps: [
      { code: "bash <(curl -fsSL https://mosfet.shahtech.info)" },
      { text: "This clones the latest Mosfet release, sets up an isolated Python environment, and installs a mosfet command on your PATH." },
      { text: "Then set it up and start chatting:", code: "mosfet config\nmosfet" },
  ]},
  { id: "docker", label: "Docker", steps: [
      { text: "Create a docker-compose.yml in the project directory:", code: "services:\n  mosfet-app:\n    image: busycaesar/mosfet:latest\n    volumes:\n      - ./mosfet.config.json:/app/mosfet.config.json\n      - ./.env:/app/.env" },
      { text: "Create mosfet.config.json and .env in the same directory:", code: "echo '{}' > mosfet.config.json\ntouch .env" },
      { text: "Start the container:", code: "docker compose up -d" },
      { text: "Set it up and start chatting:", code: "docker compose exec -it mosfet-app mosfet config\ndocker compose exec -it mosfet-app mosfet" },
  ]},
  { id: "manual", label: "Manual setup", steps: [
      { text: "Clone the repo:", code: "git clone git@github.com:busycaesar/Mosfet.git\ncd Mosfet" },
      { text: "Create a virtual environment and install dependencies:", code: "python3 -m venv .venv\nsource .venv/bin/activate\npip install -r req.txt" },
      { text: "Set it up and start chatting:", code: "python3 src/main.py config\npython3 src/main.py" },
  ]},
];

export const faq: FaqItem[] = [
  { question: "Is it free?", answer: "Yes. Mosfet is open source under the MIT License." },
  { question: "Which LLMs can it use?", answer: "Whichever LLM provider and model you choose, hosted or local. You can change it anytime by running mosfet config." },
  { question: "Where does it run?", answer: "On your own machine. Install it with the install script, run it with Docker, or set it up manually from source." },
  { question: "How do I talk to it?", answer: "Through your terminal or other communication channels. Each channel resumes its last conversation automatically." },
  { question: "How do I extend it?", answer: "Add skills, tools, MCP servers and workflows. Skills describe a capability or knowledge it can draw on, tools let it take action, MCP servers connect it to external systems, and workflows chain these into a saved, repeatable procedure." },
  { question: "Is it ready to use?", answer: "It's early-stage and a work in progress. You can install it and try it today with any of the methods above." },
];
