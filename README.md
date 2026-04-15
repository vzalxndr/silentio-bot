---
title: silentio-bot
emoji: 🤫
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# silentio-bot
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-f55036?style=for-the-badge)

A Telegram bot for voice and video message transcription and text processing, powered by the Groq API.

**Link:** [@silentio_tg_bot](https://t.me/silentio_tg_bot)

## Core Models
* **Whisper Large v3 Turbo** (OpenAI): Handles audio/video-to-text transcription and automatic language detection.
* **Llama 3.1 8B Instant** (Meta): Processes the transcribed text for LLM-based generation tasks.

## Functionality
The bot accepts voice messages or video notes and provides the following processing modes:
* **Keep Raw:** Outputs the direct transcription.
* **Summary:** Extracts key points from the transcribed text.
* **Make Note:** Formats the transcription into structured Markdown notes.
* **AI Assistant:** Rewrites rough voice dictations into formatted, ready-to-send messages based on context.

## Tech Stack
* **Language:** Python 3.10
* **Framework:** Aiogram 3.x
* **LLM Provider:** Groq API
* **Deployment:** Docker (via Hugging Face Spaces)
