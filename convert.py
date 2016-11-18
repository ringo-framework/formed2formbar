#!/usr/bin/env python
import os
import sys
import argparse
import xml.etree.ElementTree as ET

__doc__ = """A simple python script to convert a XML form definition
written in formed into a formbar form definiton."""


OENTITY = u'<entity id="{id}" name="{name}" label="{label}" type="{type}" {desired}>'
CENTITY = u'</entity>'

def get_values(e, t="string"):
    values = {}
    values["name"] = e.attrib.get("name")
    values["id"] = e.attrib.get("name")
    values["type"] = t
    values["label"] = e.attrib.get("description")
    flags = e.attrib.get("flags")
    values["desired"] = ""
    if flags and flags.startswith("required"):
        values["desired"] = 'desired="true"'
    return values

def convert_element(e, t=None):
    x = []
    options = []
    values = get_values(e, t)
    x.append(OENTITY.format(**values))
    for c in e.findall("bool"):
        value = c.attrib["value"]
        if value == "-1":
            value = ""
        options.append(" "*8 + u'<option value="{}">{}</option>'.format(value, c.attrib["description"]))

    if options:
        y = []
        y.append("\n" + " "*4 + "<options>")
        for o in options:
            y.append(o)
        y.append(" "*4 + "</options>\n")
        x.append("\n".join(y))


    x.append(CENTITY+"\n")
    return (values["name"], "".join(x))

def convert_text(e):
    return convert_element(e, "string")

def convert_int(e):
    return convert_element(e, "integer")

def convert_date(e):
    return convert_element(e, "date")

def convert_choice(e):
    return convert_element(e, "integer")

def find_elements(et):
    # Find all text fields
    elements = []
    for e in et.findall(".//text"):
        elements.append(convert_text(e))
    for e in et.findall(".//int"):
        elements.append(convert_int(e))
    for e in et.findall(".//date"):
        elements.append(convert_date(e))
    for e in et.findall(".//choice"):
        elements.append(convert_choice(e))
    return elements

def parse_infile(xml, rg=None):
    """TODO: Docstring for parse_infile.
    :returns: TODO

    """
    ignored_elements = []
    et = ET.fromstring(xml.read())

    # Find all repeat groups:
    for e in et.findall(".//repeat"):
        if rg and e.attrib["name"] == rg:
            return [x[1] for x in find_elements(e)]
        else:
            ignored_elements.extend()
    all_elements = find_elements(et)
    ignored_names = [x[0] for x in ignored_elements]

    elements = []
    for e in all_elements:
        if e[0] in ignored_names:
            continue
        elements.append(e[1])
    return elements


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('formed.xml', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('-l', '--list-modules',
                        action="store_true",
                        dest="list",
                        help="Will list all modules/repeat groups")
    parser.add_argument('-r', '--repeat-group',
                        dest="rg",
                        help="Parse the given repeat group.")

    args = parser.parse_args(arguments)
    if args.list:
        et = ET.fromstring(args.infile.read())
        # Find all repeat groups:
        for e in et.findall(".//repeat"):
            print(e.attrib["name"])
    else:
        elements = parse_infile(args.infile, args.rg)
        content = "".join(e.encode("utf-8") for e in elements)
        if args.outfile:
            args.outfile.write(content)
            args.outfile.close()
        else:
            print(content)

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)
