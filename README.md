# clean_chatbot
A simple clean chatbot with ChatGPT


## Usage
1. Modify `api_key` in `ChatBotDefault` in `default.py` properly.
2. Create and source to you virtual environment
    ```
    virtualenv env
    source env/bin/activate
    ```
3. Install requirements: `pip install -r requirements.txt`
4. Run the main scipy: `python -m main`
5. Start to chat!

I also printed the message in the main chat function `ChatBot.chat` in `chatbot.py`, you can modify this as you may not want to see the message printed twice.

## Example of user imput
```bash
搜尋今日台北、台中、高雄的最高溫幾攝氏幾度，然後寫入成 天氣.txt 檔案
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
