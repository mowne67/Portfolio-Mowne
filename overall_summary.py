import os
from pathlib import Path

# ✅ Your working GPT-4o call function
def call_gpt4o(prompt: str) -> str:
    # Replace with actual Azure OpenAI GPT-4o call
    return "Mock response: summary + flowchart + folder structure"

# ✅ Collect summaries from .summary.md files
def collect_all_summaries(summary_dir: str) -> str:
    all_summaries = ""
    for file in Path(summary_dir).glob("*.summary.md"):
        try:
            content = file.read_text(encoding="utf-8")
            all_summaries += f"\n\n# {file.name}\n{content.strip()}\n"
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
    return all_summaries

# ✅ Generate folder structure as a text-based tree
def get_folder_tree(base_path: str) -> str:
    tree = ""

    def walk(dir_path: Path, prefix: str = ""):
        entries = sorted([e for e in dir_path.iterdir() if not e.name.startswith(".")])
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            tree_line = f"{prefix}{connector}{entry.name}"
            tree_list.append(tree_line)
            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                walk(entry, prefix + extension)

    tree_list = [f"{Path(base_path).resolve().name}/"]
    walk(Path(base_path))
    return "\n".join(tree_list)

# ✅ Create final prompt with summaries + structure
def generate_codebase_summary_and_flowchart(summary_text: str, folder_structure: str) -> str:
    prompt = f"""
You are a software documentation assistant.

Below is the folder structure and summaries of individual files from a codebase.

Your tasks:

1. Provide a high-level summary of the entire codebase: what it does, its main components, and how it fits together.
2. Generate a simple flowchart (in Markdown or ASCII text) that shows how the key modules relate.
3. Highlight the structure of the codebase using the folder layout.

FOLDER STRUCTURE:
{folder_structure}

FILE SUMMARIES:
{summary_text}
"""
    return call_gpt4o(prompt)

# ✅ Save the result to markdown
def save_overall_summary(output: str, output_path: str = "codebase_overview.md"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📦 Overall Codebase Summary and Flowchart\n\n")
        f.write(output.strip())
    print(f"✅ Saved: {output_path}")

# ✅ Run it all
if __name__ == "__main__":
    summary_dir = "summaries"            # Your summary folder
    source_dir = "your/codebase/path"    # Your code folder (replace this)

    summaries = collect_all_summaries(summary_dir)
    if not summaries.strip():
        print("⚠️ No summaries found in:", summary_dir)
    else:
        folder_tree = get_folder_tree(source_dir)
        final_output = generate_codebase_summary_and_flowchart(summaries, folder_tree)
        save_overall_summary(final_output)
