import re
import os
import argparse

def extract_info_from_file(file_path):
    pattern = r'(?P<path>.*?)\((?P<lineno>\d+)\):\s(?P<code>.*)'

    result = {}

    with open(file_path, 'r') as file:
        for line in file:
            matches = re.finditer(pattern, line)
            for match in matches:
                path = match.group('path')
                lineno = match.group('lineno')
                code = match.group('code')

                if path not in result:
                    result[path] = []

                result[path].append((lineno, code))

    for key in result:
        result[key] = sorted(set(result[key]), key=lambda x: int(x[0]))

    return result

def create_files_and_write_info(result_map, relative_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for path, info_list in result_map.items():
        print(f"process {path}, prefix {relative_path}")
        if relative_path not in path:
            continue
        
        path = path.replace(relative_path, "")
        if path.startswith('/'):
            path = path[1:]
        
        print(f"handling {path}")
        target_file_path = os.path.join(current_dir, path)

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, 'w') as target_file:
            for lineno, code in info_list:
                target_file.write(f"{lineno} : {code}\n")

def main():
    parser = argparse.ArgumentParser(description='Process file content and create files.')
    parser.add_argument('file_path', type=str, help='Path to the file containing the content')
    parser.add_argument('relative_path', type=str, help='Relative path for file generation')

    args = parser.parse_args()

    file_path = args.file_path
    relative_path = args.relative_path

    result_map = extract_info_from_file(file_path)
    create_files_and_write_info(result_map, relative_path)

if __name__ == "__main__":
    main()
