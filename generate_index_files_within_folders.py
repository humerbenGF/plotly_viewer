import os

# Skip system and hidden directories, especially .github/
def should_skip_directory(dir_path):
    parts = dir_path.split(os.sep)
    return any(part.startswith('.') for part in parts)  # Skip hidden directories

# Function to generate an index.html file inside a given folder
def generate_index_html(folder_path):
    files = sorted(os.listdir(folder_path))
    
    # Filter only HTML files
    html_files = [f for f in files if f.endswith('.html') and f != 'index.html']
    subdirs = [f for f in files if os.path.isdir(os.path.join(folder_path, f))]

    index_path = os.path.join(folder_path, "index.html")
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Index</title>\n</head>\n<body>\n")
        f.write(f"<h1>Index of {folder_path}</h1>\n<ul>\n")
        
        # Add links to subdirectories
        for subdir in subdirs:
            f.write(f'  <li><a href="{subdir}/index.html">{subdir}/</a></li>\n')

        # Add links to HTML files
        for html_file in html_files:
            f.write(f'  <li><a href="{html_file}">{html_file}</a></li>\n')

        f.write("</ul>\n</body>\n</html>")

    print(f"Generated: {index_path}")

# Recursively process all directories in the repository
def generate_indexes_recursively(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if should_skip_directory(root):
            continue  # Skip .github and hidden folders
        generate_index_html(root)

# Run the script from the repository root
if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))  # Script location
    generate_indexes_recursively(repo_root)
    print("✅ All index.html files updated successfully!")
