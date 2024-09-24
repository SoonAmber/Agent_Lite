'''
todo
    1. 设置环境变量
    2. 引入工具
    3. prompt模板
    4. 模型初始化
'''
import time
from tools import tools_map
from prompt import gen_prompt,user_prompt
from model_provided import ModelProvider
from dotenv import load_dotenv
load_dotenv()

mp=ModelProvider()

def parse_thoughts(response):
    '''
    response:
    {
        "action":{
            "name":"action name",
            "args":{
                "args name":"args value"
            }
        },
        "thought":{
            "text":"thought",
            "plan":"plan",
            "criticism":"criticism",
            "speaker":"当前步骤，返回的信息speaker",
            "reasoning":""
        }
    }
    '''
    try:
        thoughts = response.get("thought")
        if not thoughts:
            raise ValueError("response 中没有 'thought' 字段")
        
        observation = response.get("observation")
        plan = thoughts.get("plan", "")
        criticism = thoughts.get("criticism", "")
        reasoning = thoughts.get("reasoning", "")
        

        prompt = f"plan:{plan}\nreasoning:{reasoning}\ncriticism:{criticism}\nobservation:{observation}"
        return prompt
    except Exception as err:
        print("parse thoughts err:{}".format(err))
        return str(err)

def agent_execute(query,max_request_time=10):
    # 防止陷入死循环，设置最大循环次数
    cur_request_time = 0
    chat_history=[]
    agent_scratch=''
    #todo
    while cur_request_time < max_request_time:
        cur_request_time += 1
        #todo
        '''prompt包含的功能
        1. 任务的表述
        2. 工具的表述
        3. 用户的输入user_msg
        4. assistant_msg
        5. 限制
        6. 因为有反思，所以需要给出返回的实践描述'''
        prompt = gen_prompt(query,agent_scratch)
        start_time = time.time()
        print("第{}次开始调用llm".format(cur_request_time),flush = True)

        response = mp.chat(prompt, chat_history, user_prompt)
        #todo call LLM
        '''
        sys_prompt
        user_msg,assistant_msg_history
        '''
        
        end_time = time.time()
        print("第{}次结束调用llm，耗时{}".format(cur_request_time,end_time-start_time),flush = True)

        #报错处理
        if not response or not isinstance(response,dict):
            print("调用大模型错误，即将重试。。",response)
            continue
        '''
        response:
        {
            "action":{
                "name":"action name",
                "args":{
                    "args name":"args value"
                }
            },
            "thought":{
                "text":"thought",
                "plan":"plan",
                "criticism":"criticism",
                "speaker":"当前步骤，返回的信息speaker",
                "reasoning":""
            }
        }
        
        '''
        #解析action
        #还需要定义出action
        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")
        print("当前action name:",action_name,action_args)

        if action_name == "finish":
            final_answer = action_args.get("answer")# 这里的answer那来的没看懂。
            print("final answer是：",final_answer)
            break
        observation = response.get("observation")

        #加一些其他的action
        # 可以写个函数这样方便调用
        #action_name到函数的映射：map -> {action_name:func}
        try:
            # tools_map的实现
            func = tools_map.get(action_name)
            observation = func(**action_args) # observatin通常用来保存该操作的输出
            #如果 action_name 存在于 tools_map 中，函数将使用 action_args 中的参数执行特定的操作

        except Exception as err:
            print("调用工具异常：",err)

        agent_scratch = agent_scratch + "\n" + observation

        #user_msg = "决定使用哪个工具"
        assistant_msg = parse_thoughts(response)
        #chat_history.append([user_prompt,assistant_msg])
        chat_history.append({'assistant': assistant_msg, 'user': user_prompt})
    if cur_request_time >= max_request_time:
        print("非常遗憾此次任务执行失败，请重新尝试")
    else:
        print("任务执行成功")

def main():
    max_request_time=10
    #需求：支持用户的多次交互
    while True:
        query = input("请输入你的目标：")
        if query == "exit":
            return
        agent_execute(query,max_request_time=max_request_time)

if __name__ == "__main__":
     main()