from pprint import pprint
from pyparsing import *
import sys


def main(filename):
    LBRACE, RBRACE = map(Suppress, '{}')
    key = dblQuotedString | Word(printables, excludeChars='{}/')
    value = Forward()
    node = Group(key + value)
    dblQuotedString.setParseAction(removeQuotes)
    section = Group(LBRACE + ZeroOrMore(node) + RBRACE)
    value << (key | section)

    results = OneOrMore(node).parseFile(filename).asList()
    outstr = '"Maphack"\n{\n\t"pre_entities"\n\t{\n'

    for entry in results:
        if entry[0] == 'entity':
            outstr += stringify_entity(entry[1])

    outstr += "\t}\n}"

    with open(f'{filename}_maphack.txt', 'w') as out:
        out.write(outstr)

    print(outstr)


def stringify_entity(entity_data):
    tierent = ''
    tierkv = ''
    tierconn = ''
    classname = ''
    for kv in entity_data:
        if kv[0] == 'classname':
            classname = kv[1]

    if not classname or classname == 'prop_static':
        return ''

    for kv in entity_data:
        if isinstance(kv[1], str):
            if kv[0] != 'classname':
                tierkv += f'\t\t\t\t"{kv[0]}" "{kv[1]}"\n'

        elif kv[0] == 'solid':
            return ''

        elif kv[0] == 'connections':
            for conn in kv[1]:
                tierconn += f'\t\t\t\t"{conn[0]}" "{conn[1]}"\n'

    outstr = f'\t\t"{classname}"\n'
    outstr += '\t\t{\n'

    if len(tierent):
        outstr += tierent

    if len(tierkv):
        outstr += f'\t\t\tkeyvalues\n'
        outstr += '\t\t\t{\n'
        outstr += tierkv
        outstr += '\t\t\t}\n'

    if len(tierconn):
        outstr += f'\t\t\tconnections\n'
        outstr += '\t\t\t{\n'
        outstr += tierconn
        outstr += '\t\t\t}\n'
    outstr += '\t\t}\n'
    return outstr


if __name__ == '__main__':
    main(sys.argv[1])
