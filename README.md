# Blog to Podcast Agent

An AI agent that converts any blog post into an audio podcast. Built with Agno, Streamlit, Firecrawl, and ElevenLabs.

## Features
- Scrapes any blog URL using Firecrawl
- Summarizes content into a conversational script using an LLM
- Converts the summary to natural-sounding audio via ElevenLabs
- Simple Streamlit UI

## Setup

1. Clone the repo
```bash
   git clone https://github.com/ad1lahamed/blog-to-podcast-agent.git
   cd blog-to-podcast-agent
```

2. Create a virtual environment
```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Run the app
```bash
   streamlit run main.py
```

## API Keys Required
- OpenAI / Gemini / Groq (for the LLM)
- Firecrawl (for scraping)
- ElevenLabs (for audio generation)

## Tech Stack
- **Agno** — agent framework
- **Streamlit** — UI
- **Firecrawl** — web scraping
- **ElevenLabs** — text-to-speech