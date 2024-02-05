import os
import pandas as pd
from googlesearch import search


def google_search(keyword):
    content = ""
    for item in search(keyword, advanced=True, num_results=3, lang='zh-tw'):
        content += f"Title: {item.title}\n Description: {item.description}\n\n"
    return content


def read_txt_file(filepath: str):
    with open(filepath, 'r', encoding="utf-8") as f:
        return f.read()


def read_csv_file(filepath: str):
    return pd.read_csv(filepath).to_markdown()


read_file_funs = {
    '.txt': read_txt_file,
    '.csv': read_csv_file
}


def write_file(filepath, content, need_check=True):
    if need_check:
        check = input(f"確定寫入檔案 {filepath}? (y/n) ")

    if check != "y":
        return f"拒絕寫入訊息至 {filepath}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"成功寫入訊息至 {filepath}"


def read_file(filepath):
    _, file_extension = os.path.splitext(filepath)
    read_file_fun = read_file_funs.get(file_extension)
    content = read_file_fun(filepath)

    return content


function_definitions = [
    {
        "name": "google_search",
        "description": "搜尋最新的或未知的資訊",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "搜尋關鍵字"
                }
            },
        "required": ["keyword"]
        },
    },
    {
        "name": "write_file",
        "description": "寫入檔案",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "要寫入的檔案路徑"
                },
                "content": {
                    "type": "string",
                    "description": "要寫入的檔案內容"
                }
            }
        },
        "required": ["filepath", "content"]
    },
    {
        "name": "read_file",
        "description": "讀取檔案",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "要讀取的檔案路徑"
                }
            }
        },
        "required": ["filepath"]
    },
]


tool_definitions = [
    {
        "type": "function",
        "function": definition
    }
    for definition in function_definitions
]


tool_functions = {
    "google_search": google_search,
    "write_file": write_file,
    "read_file": read_file
}
