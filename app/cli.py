import argparse
import time
from app.xml_parser import load_xml, save_xml
from app.extractor import extract_paragraphs
from app.llm_service import proofread_text
from app.injector import inject_errors_xml
from app.style_guide import load_style_guide


# for UI reuse
def process_file(input_path, style_path, lang, output_path):
    tree = load_xml(input_path)
    paragraphs = extract_paragraphs(tree)
    style_text = load_style_guide(style_path)

    for p in paragraphs:
        text = "".join(p.itertext())

        if not text.strip():
            continue

        errors = proofread_text(text, lang, style_text)
        if errors:
            inject_errors_xml(p, errors)

    save_xml(tree, output_path)


# Existing CLI
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--lang", default="en")
    parser.add_argument("--style", required=True)

    args = parser.parse_args()
    start = time.time()

    output = args.input.replace(".xml", ".corrected.xml")

    # reusable function
    process_file(args.input, args.style, args.lang, output)

    print(f"Done in {time.time()-start:.2f}s → {output}")


if __name__ == "__main__":
    main()
