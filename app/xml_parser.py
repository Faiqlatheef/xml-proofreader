from lxml import etree

def load_xml(path):
    parser = etree.XMLParser(remove_blank_text=False)
    return etree.parse(path, parser)

def save_xml(tree, path):
    tree.write(path, pretty_print=True, encoding="utf-8", xml_declaration=True)
