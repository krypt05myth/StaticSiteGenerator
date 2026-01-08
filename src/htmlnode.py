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
        raise NotImplementedError("You need to override to_html!")
    
    def props_to_html(self):
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
