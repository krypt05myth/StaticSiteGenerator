from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import clean_copy_set as ccs
import gen_page as gp
"""
    BUILD ORCHESTRATOR
    Rule Name: "Master Build Protocol", Date Added: 2026-02-02.
    This entry point synchronizes asset management and page generation to 
    transform raw source material into a deployable static site [cite: 2025-11-30].
"""
def main():
    ## First, let's nuke the public folder so it is a fresh canvas, and then copy static -> public
    ccs.reset_dir() ##nuke, remake clean
    ccs.recursed_copy_path_checker_helper() ##recursive copy static -> public
    ## Then, let's gen the page from MD source using Site Generation Schema to inject into template.html; write to public/index.html
    gp.generate_pages_recursive("content","template.html","public") 
    
## Boilerplate to ensure main() only runs if the script is executed directly
if __name__ == "__main__":
    main()