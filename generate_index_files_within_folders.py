import os

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Plotly Viewer</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ text-decoration: none; color: blue; font-size: 18px; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {back_link}
    <ul>
        {links}
    </ul>
</body>
</html>
"""

def generate_indexes(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if ".git" in root.split(os.sep):  # Skip .git directory
            continue

        rel_path = os.path.relpath(root, base_dir)
        title = "Root" if rel_path == "." else rel_path
        back_link = '<a href="../index.html">⬅ Back</a>' if rel_path != "." else ""

        links = [f'<li><a href="{file}" target="_blank">{file}</a></li>' for file in sorted(files) if file.endswith(".html")]
        links += [f'<li><a href="{folder}/index.html">📁 {folder}/</a></li>' for folder in sorted(dirs)]

        index_html = INDEX_TEMPLATE.format(title=title, back_link=back_link, links="\n".join(links))
        with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

    print("✅ Index files generated recursively!")

if __name__ == "__main__":
    generate_indexes(os.getcwd())
