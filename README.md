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
git clone [https://github.com/pneelamr/ai-file-organizer.git](https://github.com/pneelamr/ai-file-organizer.git)
cd ai-file-organizer
````

2. Set Up the Python Environment

It's highly recommended to use a virtual environment.

Bash

```
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

_(Note: This assumes you have a `requirements.txt` file. If not, you can install the packages directly: `pip install ollama watchdog pypdf2 pillow pytesseract`)_

3. Install Tesseract OCR Engine

The Python OCR library needs the underlying Tesseract engine.

Bash

```
brew install tesseract
```

**4. Set Up Ollama and Download a Model**

- Download and run the [Ollama macOS app](https://ollama.com/).
    
- Pull a model via your terminal. `llama3` is powerful, while `mistral` is smaller and faster.
    

Bash

```
ollama pull llama3
```

## Usage

**1. Running Manually (for Testing)**

First, make sure the Ollama application is running. Then, execute the script from your terminal:

Bash

```
python organizer.py
```

You'll see a message that it's watching your folder. Add a file to the folder to test it. Press `Ctrl+C` to stop the script.

**2. Running as a Background Service**

To make the agent truly autonomous, run it as a background service using macOS's `launchd`.

- Edit the .plist file: Open com.user.aifileorganizer.plist and replace all instances of /path/to/your/ai-organizer with the absolute path to this project's directory.
    
    (Tip: Navigate to the folder in Terminal and run pwd to get the full path.)
    
- **Install and load the agent:**
    
    Bash
    
    ```
    # Copy the agent file to the correct directory
    cp com.user.aifileorganizer.plist ~/Library/LaunchAgents/
    
    # Load the agent to start it
    launchctl load ~/Library/LaunchAgents/com.user.aifileorganizer.plist
    ```
    

Your agent is now running in the background! You can check the `organizer.log` and `organizer.err` files to see its activity.

- **To stop the agent:**
    
    Bash
    
    ```
    launchctl unload ~/Library/LaunchAgents/com.user.aifileorganizer.plist
    ```
    

## Customization

You can easily tailor the agent to your needs by editing `organizer.py`:

- Change the watched folder:
    
    Modify the WATCH_FOLDER variable to any folder you want.
    
    Python
    
    ```
    WATCH_FOLDER = os.path.expanduser("~/Desktop") # To watch the Desktop
    ```
    
- Define your own categories:
    
    Edit the CATEGORIES dictionary. The key is the folder name, and the value is a string of keywords that helps the LLM make better decisions.
    
    Python
    
    ```
    CATEGORIES = {
        "Invoices": "invoice, receipt, bill, payment",
        "Images": "image, picture, screenshot, photo",
        "Documents": "document, report, resume, letter, form",
        "Code": "python, javascript, html, css, script",
        "Personal": "personal, travel, health, finance",
        "Work": "work, project, meeting, presentation"
    }
    ```
    
- Use a different LLM:
    
    If you've pulled a different model in Ollama (e.g., mistral), change the model parameter in the get_category_from_llm function:
    
    Python
    
    ```
    response = ollama.chat(
        model='mistral', # Changed from llama3
        messages=[{'role': 'user', 'content': prompt}]
    )
    ```
    
## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

This project is made possible by these incredible open-source tools:
- [Ollama](https://ollama.com/)
- [Watchdog](https://github.com/gorakhargosh/watchdog)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
