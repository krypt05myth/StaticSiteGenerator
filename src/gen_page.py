import os
from markdown_html import markdown_to_html_node
from block_markdown import extract_title
"""
    SITE GENERATION SCHEMA: MARKDOWN TO HTML ORCHESTRATOR
    Rule Name: "Site Generation Schema", Date Added: 2025-11-25.
    This module acts as the factory floor, reading raw Markdown and HTML templates, 
    invoking the parsing engine, and committing the final injected product 
    to the public build directory [cite: 2025-11-30].
"""
def generate_page(source_path, template_path, target_path):
    print(f"Generating page from {source_path} to {target_path} using {template_path}")
    with open(file=source_path, mode="r") as source, open(file=template_path, mode="r") as template:
        source = source.read()
        template = template.read()
        # Invoke HTML Conversion Schema to collapse nodes into a string
        html = markdown_to_html_node(source).to_html()
        title = extract_title(source)
        # Systematic placeholder replacement
        templ_fixed = template.replace("{{ Title }}",title).replace("{{ Content }}", html)
        # 1. Isolate the directory from the full file path for pre-write validation
        target_dir = os.path.dirname(target_path)
        # 2. Create all missing levels in one go with safety: 
        # exist_ok=True prevents an error if the path already exists, kinda duh but don't forget!
        os.makedirs(target_dir, exist_ok=True)
        # 3. Commit the generated page (a string) to the file
        with open(file=target_path,mode="w") as target:
            target.write(templ_fixed)


