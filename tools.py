from googlesearch import search


def google_search(keyword):
    content = ""
    for item in search(keyword, advanced=True, num_results=3, lang='zh-tw'):
        content += f"Title: {item.title}\n Description: {item.description}\n\n"
    return content


def write_file(filepath, content):
    check = input(f"確定寫入檔案 {filepath}? (y/n) ")
    if check == "y":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功寫入訊息至 {filepath}"
    else:
        return f"拒絕寫入訊息至 {filepath}"


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
                    "description": "檔案路徑"
                },
                "content": {
                    "type": "string",
                    "description": "檔案內容"
                }
            }
        },
        "required": ["filepath", "content"]
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
}
