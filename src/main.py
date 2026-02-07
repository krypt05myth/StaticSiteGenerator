import sys 
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
##Proj didn't want the following method, lol method, employed:
    # base_dir = input(f"What is the base filepath you wish to access?")
    # src_dir = input(f"What is the source folder in the base path?")
    # tgt_dir = input(f"What is the target folder in the base path?")
    if len(sys.argv) > 1:
        base_url_path = sys.argv[1] ## could be something lik "/StatiicSiteGenerator/"
    else:
        base_url_path = "/"

    ## First, let's nuke the docs folder so it is a fresh canvas, and then copy static -> docs
    ccs.reset_dir() ##nuke, remake clean
    ccs.recursed_copy_path_checker_helper() ##recursive copy static -> docs
    ## Then, let's gen the page from MD source using Site Generation Schema to inject into template.html; write to docs/index.html
    gp.generate_pages_recursive("content","template.html","docs", base_url_path) 
    
## Boilerplate to ensure main() only runs if the script is executed directly
if __name__ == "__main__":
    main()