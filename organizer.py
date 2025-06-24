import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ollama
import PyPDF2
from PIL import Image
import pytesseract

# --- Configuration ---
# The folder you want to monitor (e.g., your Downloads folder)
WATCH_FOLDER = os.path.expanduser("~/Downloads")

# The categories you want to sort your files into
# The keys are the folder names, and the values are keywords to help the AI
CATEGORIES = {
    "Invoices": "invoice, receipt, bill, payment",
    "Images": "image, picture, screenshot, photo",
    "Documents": "document, report, resume, letter, form",
    "Code": "python, javascript, html, css, script",
    "Personal": "personal, travel, health, finance",
    "Work": "work, project, meeting, presentation"
}

# --- Helper Functions ---

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def extract_text_from_image(image_path):
    """Extracts text from an image file using OCR."""
    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return ""

def get_category_from_llm(filename, file_content):
    """Uses the local LLM to determine the file's category."""
    prompt = f"""
    Based on the filename and its content, which of the following categories does this file belong to?
    The categories are: {', '.join(CATEGORIES.keys())}.
    The keywords for each category are: {CATEGORIES}
    
    Filename: {filename}
    Content: "{file_content[:500]}..." # Use the first 500 characters of content

    Please respond with only the single category name.
    """
    
    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}]
        )
        category = response['message']['content'].strip()
        if category in CATEGORIES:
            return category
        else:
            print(f"LLM returned an invalid category: {category}")
            return "Other" # A fallback category
    except Exception as e:
        print(f"Error communicating with LLM: {e}")
        return "Other"

# --- The Main File Handler ---

class FileOrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        print(f"New file detected: {filename}")

        # Give the file a moment to finish writing
        time.sleep(1)

        file_content = ""
        if filename.lower().endswith('.pdf'):
            file_content = extract_text_from_pdf(file_path)
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_content = extract_text_from_image(file_path)

        # Get the category from our local LLM
        category = get_category_from_llm(filename, file_content)
        print(f"AI categorized '{filename}' as: {category}")

        # Create the category folder if it doesn't exist
        category_folder = os.path.join(WATCH_FOLDER, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Move the file
        shutil.move(file_path, os.path.join(category_folder, filename))
        print(f"Moved '{filename}' to '{category_folder}'")

# --- Start the Watchdog ---

if __name__ == "__main__":
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)
        print(f"Created watch folder: {WATCH_FOLDER}")

    event_handler = FileOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    
    print(f"Starting AI file organizer. Watching: {WATCH_FOLDER}")
    observer.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
