
import sys
import argparse
import subprocess
import json

OUTPUT_TYPES = dict(zip(['PlantUML', 'PNG'], ['pu', 'png']))

def arg_parser():
    """Argument Parser
    
    Parsing arguments
    
    Returns:
        - arguments of Namespace object
    """
    parser = argparse.ArgumentParser(description='Draw the directory tree',
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--tree_json', dest='tree_json', type=str, default=None, required=False, \
            help='JSON file that is gotten from ``tree -J`` command')
    
    parser.add_argument('--output_type', dest='output_type', type=str, choices=OUTPUT_TYPES.keys(), default='PlantUML', required=False, \
            help='output file type')

    parser.add_argument('--output_file', dest='output_file', type=str, default=None, required=False, \
            help='output file path\n'
                 '  - default: output.[pu, png, ...]')
    
    args = parser.parse_args()

    return args
    
def create_plantuml(dict_dir_tree):
    """Create PlantUML
    
    Create PlantUML script as the component diagram
    
    Args:
        - dict_dir_tree: directory tree of the dictionary object
    
    Returns:
        - plantuml script
    """
    
    plantuml_script = ''
    for item in dict_dir_tree:
        if (item['type'] == 'directory'):
            print(f'directory: {item["name"]}')
            plantuml_script += f'folder "{item["name"]}" {{\n'
            if ('contents' in item.keys()):
                plantuml_script += create_plantuml(item['contents'])
            plantuml_script += '}\n'
        elif (item['type'] == 'file'):
            print(f'file: {item["name"]}')
            plantuml_script += f'[{item["name"]}]\n'
        else:
            pass
    
    return plantuml_script
    
def main():
    """main
    
    Main function
    """
    args = arg_parser()
    print(f'tree_json: {args.tree_json}')
    print(f'output_type: {args.output_type}')
    print(f'output_file: {args.output_file}')
    
    output_file = args.output_file
    if (args.output_file is None):
        output_file = f'output.{OUTPUT_TYPES[args.output_type]}'
    print(f'output_file: {output_file}')
    
    if (args.tree_json is None):
        # --- get the directory tree from ``tree -J`` ---
        result = subprocess.run(['tree', '-J'], stdout=subprocess.PIPE)
        dir_tree = result.stdout.decode('utf-8')
        print(dir_tree)
        dict_dir_tree = json.loads(dir_tree)
    else:
        with open(args.tree_json, 'r') as f:
            dict_dir_tree = json.load(f)
    
    print(dict_dir_tree)
    
    if (args.output_type == 'PlantUML'):
        plantuml_script = '@startuml\n'
        plantuml_script += create_plantuml(dict_dir_tree)
        plantuml_script += '@enduml\n'
        print(plantuml_script)
        with open (output_file, 'w') as f:
            f.writelines(plantuml_script)
    elif (args.output_type == 'PNG'):
        print('T.B.D')
    else:
        print(f'{args.output_type} is not supported')
    
if __name__=='__main__':
    main()

