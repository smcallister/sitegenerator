class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        html = ""
        for (key, value) in self.props.items():
            if len(html) > 0:
                html += " "
            
            html += f'{key}="{value}"'
        
        return html
    
    def __repr__(self):
        return f'HTMLNode({tag}, {value}, {children}, {props})'