import os

# Skip system and hidden directories, especially .github/ and .git/
def should_skip_directory(dir_path):
    parts = dir_path.split(os.sep)
    return any(part.startswith('.') or part in {'.git', '.github'} for part in parts)  # Explicitly exclude .git and .github


# Function to generate an index.html file inside a given folder
def generate_index_html(folder_path):
    files = sorted(os.listdir(folder_path))

    # Filter only HTML files (excluding index.html)
    html_files = [f for f in files if f.endswith('.html') and f != 'index.html']
    subdirs = [f for f in files if os.path.isdir(os.path.join(folder_path, f))]

    index_path = os.path.join(folder_path, "index.html")
    relative_path = os.path.relpath(folder_path, repo_root)

    # Determine back button (go up one directory)
    back_link = ".." if relative_path != "." else None

    with open(index_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Index</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; } \n")
        f.write("ul { list-style-type: none; padding: 0; } \n")
        f.write("li { margin: 5px 0; } \n")
        f.write("a { text-decoration: none; color: #007bff; font-size: 18px; } \n")
        f.write("a:hover { text-decoration: underline; } \n")
        f.write("</style>\n</head>\n<body>\n")

        f.write(f"<h1>Index of {relative_path}</h1>\n")

        # Add back button
        if back_link:
            f.write(f'<p><a href="{back_link}/index.html">⬅ Back</a></p>\n')

        f.write("<ul>\n")

        # Ensure something is written even if the folder is empty
        if not html_files and not subdirs:
            f.write("<li><em>No files or subdirectories</em></li>\n")

        for subdir in subdirs:
            f.write(f'  <li>📁 <a href="{subdir}/index.html">{subdir}/</a></li>\n')

        for html_file in html_files:
            f.write(f'  <li>📄 <a href="{html_file}">{html_file}</a></li>\n')

        f.write("</ul>\n</body>\n</html>")

    print(f"✅ Generated: {index_path}")

# Recursively remove old index.html files before regenerating new ones
def remove_old_indexes(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if should_skip_directory(root):
            continue  # Skip hidden folders like .github
        for file in files:
            if file == "index.html":
                os.remove(os.path.join(root, file))
                print(f"🗑 Deleted: {os.path.join(root, file)}")

# Recursively generate index.html files
def generate_indexes_recursively(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if should_skip_directory(root):
            continue  # Skip hidden folders like .github
        generate_index_html(root)

# Run the script
if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))  # Root directory
    print("🔄 Removing old index.html files...")
    remove_old_indexes(repo_root)  # Step 1: Delete old index.html files
    print("🚀 Generating new index.html files...")
    generate_indexes_recursively(repo_root)  # Step 2: Regenerate all index.html files
    print("✅ All index.html files updated successfully!")

