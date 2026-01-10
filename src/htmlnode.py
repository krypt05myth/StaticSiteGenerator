class HTMLNode:
    def __init__(
            self, 
            tag=None, 
            value=None, 
            children=None, 
            props=None,
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        ## Turns whole node into HTML
        raise NotImplementedError("You need to override to_html!")
    
    def props_to_html(self):
        ## Turns the properties dict into str that goes into a Tag
        if self.props is None:
            return ""
        #  Goal is to join the attributes with a space, and add one leading space
        return "".join([f' {k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node with no value, but all must have values.") 
        if self.tag is None:
            return self.value
        return "".join([f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag.")
        if self.children is None:
            raise ValueError("Where the kids at?")
    ## Need to first build the string that recursion will populate
        kids_html = ""
        for kid in self.children:
            kids_html += kid.to_html()
        return f"<{self.tag}{self.props_to_html()}>{kids_html}</{self.tag}>"