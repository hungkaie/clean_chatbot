# clean_chatbot
A simple clean chatbot with ChatGPT

## Installation
1. Create and source to you virtual environment
    ```
    virtualenv env
    source env/bin/activate
    ```
2. Install requirements: `pip install -r requirements.txt`

## Usage
1. Modify `api_key` in `ChatBotDefault` in `default.py` properly.
2. Run the main scipy: `python -m main`
3. Start to chat!

I also printed the message in the main chat function `ChatBot.chat` in `chatbot.py`, you can modify this as you may not want to see the message printed twice.

## Example
```
user: 搜尋今日台北、台中、高雄的最高溫幾攝氏幾度，然後寫入成 天氣.csv 檔案
ChatGPT(金毛): None
ChatGPT(金毛) call google_search with {'keyword': '台北今日最高溫攝氏度'}
ChatGPT(金毛) call google_search with {'keyword': '台中今日最高溫攝氏度'}
ChatGPT(金毛) call google_search with {'keyword': '高雄今日最高溫攝氏度'}
ChatGPT(金毛): None
ChatGPT(金毛) call write_file with {'filepath': '天氣.csv', 'content': '城市,最高溫度(攝氏度)\n台北,19.4\n台中,20.6\n高雄,20.6\n'}
確定寫入檔案 天氣.csv? (y/n) y
ChatGPT(金毛): 已成功搜尋到今日台北、台中、高雄的最高溫度，並將資料寫入了名為「天氣.csv」的檔案中。
user: 讀取 天氣.csv 並告訴我內容
ChatGPT(金毛): None
ChatGPT(金毛) call read_file with {'filepath': '天氣.csv'}
ChatGPT(金毛): 以下是從「天氣.csv」檔案中讀取到的內容：

|    | 城市   |   最高溫度(攝氏度) |
|---:|:-------|-------------------:|
|  0 | 台北   |               19.4 |
|  1 | 台中   |               20.6 |
|  2 | 高雄   |               20.6 |
```

## In Python
```python=
>>> from chatbot import ChatBot
>>> ai = ChatBot(name='阿金')
>>> ai.chat('Tell a joke', temperature=0.8, tool_choice="none") # Raise the `temperature` to get more creative answers, use `tool_choice="none"` to avoid function calling.
ChatGPT(阿金): Why couldn't the bicycle find its way home? Because it lost its bearings! 😄
```

## Settings
All settings can be found in `default.py`, make sure you modify the `api_key` and the `system_prompt` properly.

## Function calling
All function tools can be found in `tools.py`, it only contains `google_search` and `write_file` now.

I use "auto" mode for tools calling, if you want to change to "none", check the `payload` settins in `default.py`.

I also deal the parallel function calling (but default not to use), see the `ChatBot.get_all_tool_call_message` in `chatbot.py` for details.

## Others
- Check messages: `self.messages`
- Check log: `self.log`
- Check detail prompt object: `self.objs`
