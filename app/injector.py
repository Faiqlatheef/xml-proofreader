from lxml import etree


def inject_errors_xml(p, errors):
    text = p.text or ""

    if not errors:
        return

    new_nodes = []
    current_index = 0

    for err in sorted(errors, key=lambda x: text.find(x["original"])):
        original = err["original"]
        correction = err["correction"]
        err_type = err.get("type", "unknown")

        idx = text.find(original, current_index)
        if idx == -1:
            continue

        # Add text before error
        if idx > current_index:
            new_nodes.append(text[current_index:idx])

        # Create XML element
        error_elem = etree.Element("error")
        error_elem.set("type", err_type)
        error_elem.set("correction", correction)
        error_elem.text = original

        new_nodes.append(error_elem)

        current_index = idx + len(original)

    # Add remaining text
    if current_index < len(text):
        new_nodes.append(text[current_index:])

    # Clear existing text
    p.text = ""

    # Append nodes properly
    for node in new_nodes:
        if isinstance(node, str):
            if len(p) == 0:
                p.text = (p.text or "") + node
            else:
                p[-1].tail = (p[-1].tail or "") + node
        else:
            p.append(node)