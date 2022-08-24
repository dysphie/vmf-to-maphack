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
    outstr = ''

    for entry in results:
        if entry[0] == 'entity':
            outstr += stringify_entity(entry[1])

    with open(f'{filename}_vscript.nut', 'w') as out:
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

    if not classname:
        return ''

    for kv in entity_data:
        if isinstance(kv[1], str):
            if kv[0] != 'id' and kv[0] != 'classname':
                tierkv += f'e.__KeyValueFromString("{kv[0]}", "{kv[1]}");\n'

        elif kv[0] == 'solid':
            return ''

        elif kv[0] == 'connections':
            for conn in kv[1]:
                tierconn += f'// \t\t\t\t\t"{conn[0]}" "{conn[1]}"\n'

    outstr = f'e = Entities.CreateByClassname("{classname}");\n'

    if len(tierent):
        outstr += tierent

    if len(tierconn):
        tierkv += f'// TODO: has entity I/O!"\n'
        tierkv += tierconn

    if len(tierkv):
        outstr += tierkv

    outstr += 'DispatchSpawn(e);\n\n'
    return outstr


if __name__ == '__main__':
    main(sys.argv[1])
