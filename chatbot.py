import json
import requests
from copy import deepcopy
from joblib import Parallel, delayed
from tools import tool_functions
from default import ChatBotDefault


class ChatBot:
    def __init__(
        self,
        name: str = ChatBotDefault().name,
        api_key: str = ChatBotDefault().api_key,
        system_prompt: str = ChatBotDefault().system_prompt[0],
        payload: dict = ChatBotDefault().payload,
    ):
        super(ChatBot, self).__init__()
        self.name = name
        self.api_key = api_key
        self.system_message = {"role": "system", "content": system_prompt.format(name=name)}
        self.payload = payload

        self.headers = {
            "Authorization": f'Bearer {api_key}',
            "Content-Type": "application/json"
        }
        self.messages = [self.system_message]

        self.tool_functions = {}
        for tool in payload['tools']:
            tool_name = tool['function']['name']
            self.tool_functions[tool_name] = tool_functions[tool_name]
        self.objs = []
        self.log = []

    @staticmethod
    def post_to_api(
        api_key: str = None,
        headers: dict = None,
        messages: list = [{"role": "system", "content": ChatBotDefault().system_prompt}],
        payload = ChatBotDefault().payload,
    ):
        if headers is None:
            if api_key is None:
                raise Exception("Post without both `api_key` and `headers` is not valid, at least to provide `api_key`")
            headers = {
                "Authorization": f'Bearer {api_key}',
                "Content-Type": "application/json"
            }

        payload['messages'] = messages
        response = requests.post(
            url='https://api.openai.com/v1/chat/completions',  # chat endpoint,
            headers=headers,
            data=json.dumps(payload)
        )

        return response

    def get_chat_response_message(
        self, **payload_to_update,
    ):
        payload = deepcopy(self.payload)
        payload.update(payload_to_update)

        response = self.post_to_api(
            headers=self.headers,
            messages=self.messages,
            payload=payload
        )
        obj = json.loads(response.text)
        self.objs.append(obj)

        if response.status_code == 200:
            return obj["choices"][0]["message"]
        else:
            return obj["error"]


    def get_tool_call_message(
        self, tool_call
    ):
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])
        tool_function = self.tool_functions[tool_name]

        log_message = f"ChatGPT({self.name}) call {tool_name} with {tool_args}"
        print(log_message)
        self.log.append(log_message)

        tool_ouput = tool_function(**tool_args)
        tool_message = {
            "role": "tool",
            "content": tool_ouput,
            "name": tool_name,
            "tool_call_id": tool_call["id"],
        }

        return tool_message

    def get_all_tool_call_message(
        self, response_message, njobs=1
    ):
        tool_calls = response_message.get("tool_calls")

        if njobs > 1:
            if len(tool_calls) < njobs:
                njobs = len(tool_calls)

            tool_messages = Parallel(n_jobs=njobs)(
                delayed(self.get_tool_call_message)(tool_call)
                for tool_call in tool_calls
            )

        else:
            tool_messages = []
            for tool_call in tool_calls:
                tool_messages.append(
                    self.get_tool_call_message(tool_call)
                )

        return tool_messages

    def chat(
        self,
        message=None,
        role="user",
        **payload_to_update,
    ):
        if role == "user":
            log_message = f"{role}: {message}"
            print(log_message)
            self.log.append(log_message)

            message = [{"role": role, "content": message}]

        self.messages += message
        response_message = self.get_chat_response_message(**payload_to_update)
        self.messages.append(response_message)

        log_message = f"ChatGPT({self.name}): {response_message['content']}"
        print(log_message)
        self.log.append(log_message)

        if response_message.get("tool_calls"):
            tool_messages = self.get_all_tool_call_message(response_message)
            return self.chat(message=tool_messages, role="tool")
        else:
            return response_message
