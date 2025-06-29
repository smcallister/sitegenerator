from textnode import TextNode, TextType

def main():
    node = TextNode('Local host', TextType.LINK, 'http://localhost')
    print(node)

if __name__ == "__main__":
    main()