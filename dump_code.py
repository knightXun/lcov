from bs4 import BeautifulSoup
import html
import os

def extract_code_from_html(file_path, target_file_path):
    print("process", file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    code_lines = []
    line_nums = soup.find_all('span', class_='lineNum')
    #line_nocovs = soup.find_all('span', class_='lineNoCov')

    for line_num in line_nums:
        line_code = line_num.next_sibling

        #line_num_text = line_num.get_text(strip=True)
        #line_nocov_text = line_nocov.next_sibling

        # 提取代码行
        code_line = get_code_line(line_code)
        #print(code_line)
        #if code_line is not None:
        #    code_line = f"{line_num_text}:{code_line}"
        code_lines.append(code_line)
    with open(target_file_path, 'w', encoding='utf-8') as f:
        for line in code_lines:
            f.write(line + '\n')
        #f.write(soup.prettify())

    return code_lines

def get_code_line(element):
    if element is None:
        return element

    code_line = ''
    if element.name == 'span':
        code_line = element.get_text(strip=True).split(':', 1 )[1][1:]
    elif element.name == 'br':
        next_sibling = element.next_sibling
        while next_sibling is not None and next_sibling.name != 'span':
            code_line += str(next_sibling)
            next_sibling = next_sibling.next_sibling
        code_line = code_line.strip().split(':', 1)[1][1:]
    else:
        return element.strip().split(':', 1)[1][1:]

    return code_line


def process_html_files(source_folder, target_folder):
    for root, dirs, files in os.walk(source_folder):
        for f in files:
            if f.endswith('.gcov.html'):
                source_file_path = os.path.join(root, f)
                target_file_path = source_file_path.replace(source_folder, target_folder)
                target_file_path = target_file_path.replace(".gcov.html", "")
                target_directory = os.path.dirname(target_file_path)

                # 创建目标文件夹（如果不存在）
                os.makedirs(target_directory, exist_ok=True)

                # 处理 HTML 文件并保存到目标文件夹
                extract_code_from_html(source_file_path, target_file_path)
# 示例用法
url = 'preprocess_result/clang/lib/Basic/Sanitizers.cpp.gcov.html'
#code_lines = extract_code_from_html(url, "")
#for line in code_lines:
#    print(line)

source_folder = 'preprocess_result'
target_folder = 'preprocess_code'

process_html_files(source_folder, target_folder)
