class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")

    def props_to_html(self):
        if self.props == None or len(self.props.items()) == 0:
            return ''
        props = ""
        for [k, v] in self.props.items():
            props += f' {k}="{v}"'

        return props

    def __repr__(self):
        props='None'
        if self.props:
            props=self.props_to_html()
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag=='img':
            return f"<{self.tag}{self.props_to_html()}/>"
        if not self.value:
            raise ValueError("All leaf nodes must have value")
        if self.tag==None:
            return self.value
        html = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return html

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props)

    def to_html(self):
        if self.tag==None:
            raise ValueError('ParentNode must have tag')
        if self.children==None or len(self.children)==0:
            raise ValueError('ParentNode must have children')
        html=f'<{self.tag}{self.props_to_html()}>'

        for child_node in self.children:
            html+=child_node.to_html()

        html+=f'</{self.tag}>'

        return html