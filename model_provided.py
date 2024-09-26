import os
import dashscope
from prompt import gen_prompt, user_prompt
from dashscope.api_entities.dashscope_response import Message
import json

class ModelProvider(object):
    def __init__(self):
        self.api_key = os.environ.get("DASHSCOPE_API_KEY")  # 从环境变量获取 API key
        self.model_name = "qwen-plus"  # 设置默认的模型名称
        self._client = dashscope.Generation()
        self.max_turns = 3  # 设置对话的最大轮数

    def chat(self, prompt, chat_history, user_prompt):
        cur_retry_time = 0
        while cur_retry_time < self.max_turns:
            cur_retry_time += 1
            try:
                messages = [Message(role='system', content=prompt)]

                # 遍历历史记录，添加到消息列表中
                for history in chat_history:
                    # messages.append(Message(role=history['assistant'], content=history["0"]))
                    # messages.append(Message(role=history['user'], content=history["1"]))
                    messages.append(Message(role='assistant', content=history['assistant']))
                    messages.append(Message(role='user', content=history['user']))

                # 添加用户的当前输入
                messages.append(Message(role='user', content=user_prompt))

                # 调用模型生成回复

                response = self._client.call(
                    model=self.model_name,
                    api_key=self.api_key,
                    messages=messages,
                )


                # JSON 响应格式
                """
                {
                  "status_code": 200,
                  "request_id": "5b42b0c6-9c18-9161-9f29-5d7affcb5aee",
                  "code": "",
                  "message": "",
                  "output": {
                    "text": "{\n    \"action\": {\n        \"name\": \"search\",\n        \"args\": {\n            \"query\": \"最佳项目管理工具\"\n        }\n    },\n    \"thought\": {\n        \"plan\": \"首先搜索最佳项目管理工具，以便为用户提供合适的建议。\",\n        \"criticism\": \"在搜索之前，我应该考虑用户的特定需求，如团队规模、预算和具体管理需求。\",\n        \"speaker\": \"正在查找最佳项目管理工具的信息。\",\n        \"reasoning\": \"通过搜索，我可以获取有关各种项目管理工具的广泛信息，从而为用户提供基于当前可用数据的最佳建议。\"\n    },\n    \"observation\": \"搜索结果包含了多个项目管理工具的比较，包括Trello、Asana、Jira等。\",\n    \"answer\": \"已找到多个项目管理工具，包括Trello、Asana和Jira。接下来，我需要了解用户的具体需求，以提供最合适的建议。\"\n}",
                    "finish_reason": "stop",
                    "choices": null
                  },
                  "usage": {
                    "input_tokens": 652,
                    "output_tokens": 193,
                    "total_tokens": 845,
                    "completion_tokens_details": null
                  }
                }
                """
                # 解析响应中的内容
                content = json.loads(response['output']['text'])

                # 输出解析到的文本内容
                print(f"生成的内容: {content}")

                # 返回内容
                return content

            except Exception as err:
                # 捕捉并打印异常
                print("调用大模型出错 chat err:{}".format(err))
                return {}
