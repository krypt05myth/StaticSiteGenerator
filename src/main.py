from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import clean_copy_set as ccs

def main():
    # First, let's nuke the public folder so it is a fresh canvas
    ccs.reset_dir()

    # Create a new TextNode object with dummy values
    node = TextNode(
        "This is some anchor text", 
        TextType.LINK, 
        "https://www.boot.dev"
    )
    
    # Print the object to verify the __repr__ method works as expected
    print(node)

    
# Boilerplate to ensure main() only runs if the script is executed directly
if __name__ == "__main__":
    main()