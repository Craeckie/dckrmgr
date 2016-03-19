import os
import sys
# import docker
# import dckrjsn
import argparse
import importlib
import yaml

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: %s\n' % message)
        self.print_help()
        sys.exit(2)

sub_name = 'dckrsub.yml'
compose_name = 'docker-compose.yml'
# sub_scheme_name = 'dckrsub.schema.yml'

src_path = os.path.dirname(os.path.abspath(__file__))
# conf_scheme_path = os.path.join(src_path, sub_scheme_name)
# sub_scheme_path = os.path.join(src_path, sub_scheme_name)

# conf_scheme = dckrjsn.read_json(conf_scheme_path)
# sub_scheme = dckrjsn.read_json(sub_scheme_path)

command_list = {}
action_list = []

def addCommand(cur_directory):
    relative_dir = os.path.relpath(cur_directory, base_directory)
    action_list.append({
        'directory': cur_directory,
        'relative' : relative_dir
    })

def read_yaml(path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def traverse(cur_directory):
    # print("Traversing in " + cur_directory)
    sub_path = os.path.join(cur_directory, sub_name)
    compose_path = os.path.join(cur_directory, compose_name)

    # print("Checking file at " + sub_path)
    if os.path.isfile(sub_path): # has sub folders
        # print("Has sub folders!")
        # sub_folders = dckrjsn.read_json(sub_path, sch = sub_scheme)
        sub_folders = read_yaml(sub_path)
        for sub_folder in sub_folders:
            # print("Checking out " + sub_folder)
            next_directory = os.path.join(cur_directory, sub_folder)
            traverse(next_directory)
    elif os.path.isfile(compose_path): # has a docker-compose file
        addCommand(cur_directory)

def main():
    # global cli
    global base_directory

    # cli = docker.Client('unix://var/run/docker.sock')

    # Include external source files for commands
    # These fill the m_cmd list
    for file in os.listdir(os.path.join(src_path, 'commands')):
        ext_file = os.path.splitext(file)

        if ext_file[1] == '.py' and not ext_file[0] == '__init__':
            importlib.import_module('commands.' + ext_file[0])

    parser = MyParser()
    parser.add_argument('-D',
        dest='base_directory',
        action='store',
        default='',
        help='Set working directory')
    #parser.add_argument('-R',
    #    dest='recursive',
    #    action='store_true',
    #    help='Use dckrsub.json files to recursively apply operations')

    for cmd in command_list.items():
        parser.add_argument('-' + cmd[0],
            dest='a_cmd',
            action='append_const',
            const=cmd[0],
            help=cmd[1]['hlp'])

    args = parser.parse_args()

    base_directory = os.path.join(os.getcwd(), args.base_directory)

    #if args.recursive:
    traverse(base_directory)
    #else:
    #    addCommand(base_directory)

    for cmd in args.a_cmd: # loop over all passed arguments (t, r, c, s)
        cur_cmd = command_list[cmd]
        cmd_function = cur_cmd['fnc']
        cmd_order = cur_cmd['ord'];

        if cmd_order == 'nrm':
            action_list_sorted = action_list
        elif cmd_order == 'rev':
            action_list_sorted = reversed(action_list)
        else:
            exit(1)

        for action in action_list_sorted:
            if cmd_function(action) != 0: # execute the function through reflection
                exit(1)

    exit(0)
