from pydantic import BaseModel
from tools import tool_definitions, tool_functions


class ChatBotDefault(BaseModel):
    api_key: str = "sk-2"
    system_prompt: str = """你是一個聰明的 AI 助理，能簡潔有力的回答問題幫助大家。""",
    payload: dict = {
        'model': 'gpt-3.5-turbo-0125', #'gpt-4-1106-preview', #gpt-3.5-turbo-0125',
        'max_tokens': 300,
        'tools': [
            definition for definition in tool_definitions
            if definition['function']['name'] in tool_functions
        ],
        'tool_choice': 'auto', # ["none", "auto"]
        'stream': False,
        'response_format': {"type": "text"}, #{"type": "json_object"},
        'temperature': 0,
        'n': 1,
        'top_p': 1,
        'seed': 7,
        'frequency_penalty': 0,
        'logit_bias': None,
        'logprobs': None,
        'top_logprobs': None,
        'presence_penalty': 0,
        'stop': None,
        'user': None
    }
