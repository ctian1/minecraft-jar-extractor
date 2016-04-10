#written in python 3.4
#use `chcp 65001` for utf-8 in windows command prompt
#decompiler used was fernflower.jar from https://the.bytecode.club/showthread.php?tid=5
#decompiler usage: java -jar fernflower.jar minecraft.jar decomp_folder/
#minecraft version tested was 15w41b.jar
#sample output: (right side is this, left is prismarinejs's js extractor) http://www.diff.so/a/35tm2yR5Li

import re
from collections import OrderedDict
import json

# STATES = {
#   "0": "play",
#   "1": "status",
#   "2": "login",
#   "-1": "handshaking"
# }

def main(args):
    if len(args) != 2:
        print("Usage: python protocol_extractor.py <decompiled_files_dir>")
        exit(1)

    decompiled_files_dir = args[1]

    #read el.java, regexify, save to protocol.json
    with open(decompiled_files_dir+'/el.java', 'r', encoding='utf-8') as el:
        lines = el.read().split('\n')
        lines = map(str.strip, lines)
        lines = filter(lambda line: 'import' not in line and 'public' not in line and \
        line not in ('}', '{', '},', '', '};'), lines)
        lines = list(lines)

        # for n in range(0, len(lines)-1):
        #     lines[n] = lines[n].strip()
        #     line = lines[n]
        #     if 'import' not in line and 'public' not in line:
        #         if line not in ('}', '{', '},', ''):
        #             lines.pop(n)
        #             continue
        #     if line == '};':
        #         lines.pop(n)
        #         continue
    # with open('test.txt', 'w', encoding='utf-8') as test:
    #     test.write(str(lines))

    # from pprint import pprint
    # pprint(lines)

    state, client_id, server_id = '', 0, 0
    protocol = OrderedDict()
    for line in lines:
        match = re.search('(HANDSHAKING|PLAY|STATUS|LOGIN)', line)
        if match:
            # print(match.groups())
            # state = states[match.group(1)]
            state = match.group(1).lower()
            client_id = 0
            server_id = 0
            protocol[state] = OrderedDict()
        else:
            match = re.match(r'this\.a\(fg\.(a|b), ([a-z.]+)\.class\);', line)
            if match:
                # print(match.groups())
                # print(client_id)
                direction = 'toClient' if match.group(1) == 'b' else 'toServer'
                the_class = match.group(2)
                id_ = hex(client_id if direction == 'toClient' else server_id)
                if len(id_) == 3:
                    id_ = id_[:-1] + '0' + id_[-1]
                # id_ = id_[:2] + id_[2:].upper()
                if direction not in protocol[state]:
                    protocol[state][direction] = OrderedDict()
                protocol[state][direction][the_class] = OrderedDict({'id': id_}, fields=get_fields(the_class, decompiled_files_dir))
                if direction == 'toClient':
                    client_id += 1
                else:
                    server_id += 1

    list(map(protocol.move_to_end, ['handshaking', 'status', 'login', 'play']))
    with open('protocol.json', 'w') as out:
        out.write(json.dumps(protocol, indent=2))

def get_fields(class_, decompiled_files_dir):
    if '.' in class_:
        return ['error']
    with open(decompiled_files_dir+'/'+class_+'.java', 'r', encoding='utf-8') as data:
        fields = process_packet_definition(data)
    return fields

def process_packet_definition(data):
    fields = data.read().split('\n')
    # fields = map(str.strip, fields)
    # fields = filter(lambda line: 'read' not in line, fields)
    # fields = map(lambda line: re.match(r'read(.+?)\(', line).group(2), fields)
    new_fields = []
    for field in fields:
        field = field.strip()
        if '.read' in field:
            match = re.search(r'read(.+?)\(', field)
            if match:
                # print(match)
                new_fields.append(transform_type(match.group(1)))
    # new_fields = filter(lambda line: line, new_fields)
    # new_fields = list(map(transform_type, new_fields))
    return new_fields

def transform_type(type):
    type = type.lower()
    return type.replace('unsigned', 'u')

if __name__ == "__main__":
    import sys
    main(sys.argv)
