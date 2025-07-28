import os
from pathlib import Path

# ✅ Replace with your working GPT-4o function
def call_gpt4o(prompt: str) -> str:
    # This is your actual function that connects to GPT-4o and returns a response
    return "Mock summary for testing"  # Replace with actual GPT response

# ✅ Configuration
SOURCE_DIR = "your/codebase/path"       # <-- Change to your source folder
SUMMARY_DIR = "summaries"               # Output folder
EXTENSIONS = [".py", ".j2", ".yaml", ".yml"]

# ✅ Ensure output directory exists
os.makedirs(SUMMARY_DIR, exist_ok=True)

def read_file(file_path: Path) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""

def summarize_file(file_path: Path) -> None:
    content = read_file(file_path)
    if not content.strip():
        return

    # Truncate to avoid token overflow
    max_chars = 6000
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n# Truncated..."

    prompt = f"""
You are a code summarizer.

Here is a file from a codebase. Provide a concise summary of what this file does, mentioning any key functions, configurations, or roles it plays.

FILE NAME: {file_path.name}

FILE CONTENT: {content}
"""

    print(f"📄 Summarizing {file_path}")
    summary = call_gpt4o(prompt)

    output_file = Path(SUMMARY_DIR) / f"{file_path.name}.summary.md"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"# Summary for {file_path.name}\n\n{summary.strip()}\n")

def summarize_codebase(source_dir: str):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                file_path = Path(root) / file
                summarize_file(file_path)

# ✅ Run it
summarize_codebase(SOURCE_DIR)
