import argparse
import sys
import xml.dom.minidom

def parse_xml_file(file_path: str) -> xml.dom.minidom.Document:
    return xml.dom.minidom.parse(file_path)

def print_xml(doc: xml.dom.minidom.Document, output_file: str | None) -> None:
    pretty_xml = doc.toprettyxml(indent=" "  * 4)
    lines = [line for line in pretty_xml.splitlines() if line.strip()]
    pretty_xml = '\n'.join(lines)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(pretty_xml)
    else:
        print(pretty_xml)

def main() -> None:
    parser = argparse.ArgumentParser(description='Pretty-print an XML file')
    parser.add_argument('file_path', help='Path to the XML file')
    parser.add_argument('-o', '--output', help='Output file path')
    args = parser.parse_args()

    if not args.file_path:
        print("Error: XML file path is required.", file=sys.stderr)
        sys.exit(1)

    doc = parse_xml_file(args.file_path)
    print_xml(doc, args.output)

    return

if __name__ == '__main__':
    raise SystemExit(main())
