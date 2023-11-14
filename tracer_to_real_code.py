import re
import os
import argparse
import html
import sys
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def convert_to_html(input_file, output_file, highlighted_lines):
    with open(input_file, 'r') as file:
        code_lines = file.readlines()

        # 获取最大行号的位数，用于生成行号的对齐格式
        max_line_num_width = len(str(len(code_lines)))

        formatter = HtmlFormatter(full=True, style="friendly", linenos='table', lineanchors='line')

        html_code = f'''
        <html>
        <head>
            <style>
                {formatter.get_style_defs()}
                pre {{ white-space: pre; }}
            </style>
        </head>
        <body>
        <table class="highlighttable">
        '''
        
        for i, line in enumerate(code_lines, start=1):
            # 生成行号HTML
            line_number_html = f'<td class="linenos" style="width: 60px; padding-left: 1px;" data-value="{i}">'
            if str(i) in highlighted_lines:
                line_number_html = f'<td class="linenos" style="width: 60px; padding-left: 1px;color: blue;" data-value="{i}">'

            line_number_html += str(i).rjust(max_line_num_width)
            line_number_html += '</td>'

            # 检查是否需要将该行高亮
            # line = line.replace(' ', ' &nbsp;')
            if str(i) in highlighted_lines:
                line = f'<td class="highlight" style="white-space: pre;color: blue;">{html.escape(line)}</td>'
            else:
                line = f'<td style="white-space: pre;">{html.escape(line)}</td>'

            html_code += f'<tr><td>{line_number_html}</td>{line}</tr>'

        html_code += '</table></body></html>'

        with open(output_file, 'w') as html_file:
            html_file.write(html_code)
    
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
        
        fpath = path.replace(relative_path, "")
        if fpath.startswith('/'):
            fpath = path[1:]
        
        print(f"handling {fpath}")
        target_file_path = os.path.join(current_dir, fpath)
        # target_file_path = target_file_path.replace(".py", ".html")
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        yellow_lines = []
        for linenos in info_list:
            yellow_lines.append(linenos[0])
        print("yellow_lines: ", yellow_lines)
        
        convert_to_html(path, fpath + ".html", yellow_lines )
        # with open(target_file_path, 'w') as target_file:
        #     for lineno, code in info_list:
        #         target_file.write(f"{lineno} : {code}\n")

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
