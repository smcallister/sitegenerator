from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        if self.props is None:
            props_str = ""
        else:
            props_str = " " + self.props_to_html()

        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'