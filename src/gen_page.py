import os
from markdown_html import markdown_to_html_node
from block_markdown import extract_title
"""
SITE GENERATION SCHEMA: RECURSIVE ORCHESTRATOR
Orchestrates the conversion of entire directory trees from Markdown to HTML 
while preserving folder hierarchies and injecting template metadata.
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

def generate_pages_recursive(source_dir, template_path, target_dir):
    """
    PATH VALIDATION LAYER
    Ensures source/target mapping adheres to project security boundaries.
    """
    print(f"Recursively generating pages from {source_dir} to {target_dir} using {template_path}")
    base_dir = "/home/knix/Coding/Boot.dev/StaticSiteGenerator/"
    base_path = os.path.abspath(base_dir)
    source_path = os.path.abspath(os.path.join(base_dir, source_dir))
    target_path = os.path.abspath(os.path.join(base_dir, target_dir))
    # Guardrail: Verify both paths are localized and correctly labeled
    if (
        not (source_path.startswith(base_path)
        or target_path.startswith(base_path)) 
        or "content" not in source_path
        or "public" not in target_path
    ):
        return f"ERROR: {source_dir} not 'content' or {target_dir} not 'public', or either not in {base_path}."
    # Handshake: Transition to the recursive worker
    _recursed_copy(source_path, template_path, target_path)

def _recursed_copy(curr_src, template_path, curr_tgt):
    """
    RECURSIVE CONVERTER
    Traverses the content tree, converting .md files to .html mirrors.
    """
    # Ensure the current directory depth exists in the target
    if not os.path.exists(curr_tgt): 
        os.mkdir(curr_tgt)
    # Iterate through current level of 'contents'
    curr_src_contents = os.listdir(curr_src)
    for ea in curr_src_contents:
        new_src = os.path.join(curr_src, ea)
        new_tgt = os.path.join(curr_tgt, ea)
        print(f'Checking for ".md" in <{new_src}>, convert to ".html", copy to <{new_tgt}>.')
        # Maximal efficiency: Path-specific transformation logic.
        if os.path.isfile(new_src) and new_src.endswith(".md"):
            # Extension Swap: .md files must land as .html !!
            tgt_as_html = new_tgt.replace(".md",".html")
            generate_page(new_src, template_path, tgt_as_html)
        elif os.path.isdir(new_src):
            _recursed_copy(new_src, template_path, new_tgt) 
