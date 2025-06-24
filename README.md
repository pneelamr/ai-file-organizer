# ai-file-organizer
AI Agent to organize files using a local LLM
# Local AI File Organizer for macOS

An autonomous AI agent that automatically organizes your Mac's files using a local Large Language Model (LLM). This privacy-first tool watches a folder (like your Downloads) and intelligently sorts new files into categories you define.

![Demo GIF (Placeholder - you can create a GIF showing it in action)](https://user-images.githubusercontent.com/12345/your-demo-gif-url.gif)

---

## Key Features

-   **🤖 Autonomous Agent:** Runs in the background to watch for and process new files automatically.
-   **🧠 Intelligent Categorization:** Uses a local LLM (via Ollama) to analyze file content—not just filenames—to determine the best category.
-   **📄 Content-Aware:** Extracts text from PDFs and uses Optical Character Recognition (OCR) to read text from images, enabling deep content analysis.
-   **🔒 100% Private:** Your files and their content are never sent to the cloud. The entire process runs locally on your machine.
-   **🔧 Fully Customizable:** Easily define your own categories, keywords, and folder to watch.
-   **🚀 Lightweight Setup:** Leverages the power of Ollama to make running powerful local LLMs incredibly simple.

## How It Works

The agent follows a simple, powerful workflow:

1.  **Detect:** The `watchdog` library detects when a new file is added to the specified `WATCH_FOLDER`.
2.  **Extract:** The script checks the file type and extracts text content.
    -   For PDFs, it uses `PyPDF2`.
    -   For images (PNG, JPG, etc.), it uses `pytesseract` for OCR.
3.  **Analyze:** The filename and extracted text are sent to a locally running LLM (e.g., Llama 3, Mistral) via Ollama. A carefully crafted prompt asks the model to classify the file based on your custom categories.
4.  **Organize:** The script receives the category from the LLM, creates a corresponding subfolder if it doesn't exist, and moves the file into it.

## Prerequisites

Before you begin, ensure you have the following installed on your macOS system:

-   [Homebrew](https://brew.sh/): The missing package manager for macOS.
-   [Python 3.8+](https://www.python.org/downloads/): Your Mac likely has it, but it's good to check.
-   [Ollama](https://ollama.com/): The easiest way to run local LLMs on a Mac.

## Installation & Setup

Follow these steps to get your AI agent up and running.

**1. Clone the Repository**
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
