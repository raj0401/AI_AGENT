# AI-Powered SEO Page Analyzer

This project demonstrates a conversational AI system that performs SEO page analysis. It simulates interaction with a large language model (like Gemini or GPT) and can extract and execute function calls based on the user's query using a structured JSON response.

---

## 🧠 Features

- Simulates a Gemini client to respond to user prompts.
- Extracts JSON-formatted function calls from AI responses.
- Validates and executes SEO-related actions (e.g., checking page response time).
- Uses a conversational loop with system prompt guidance and structured interactions.

---

## 📁 Project Structure

```bash
.
├── .env                   # Contains GEMINI_API_KEY
├── main.py                # Entry point; runs the chat and action loop
├── actions.py             # Implements the actual SEO-related function
├── prompts.py             # Stores the system prompt used for conversation
├── json_helpers.py        # JSON extraction and validation helpers
└── *.pyc                  # Compiled Python files (ignored in version control)
