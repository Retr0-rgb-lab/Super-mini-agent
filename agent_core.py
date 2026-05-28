from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import json
from enum import Enum

with open('E:/Finance_AI/agent_project/practice/supermini_agent/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

import sys
sys.path.insert(0, 'E:/Finance_AI/agent_project/practice/supermini_agent/functions.py')
from function import get_current_price, get_historical_data, calculate_investment_return

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    DONE = "done"
    FAILED = "failed"

class Agent:
    def __init__(self, system_prompt):
        self.messages = [{"role": "system", "content": f"{system_prompt}"}]
        self.tools = tools
        self.state = AgentState.IDLE
        self.steps = []

    def call_llm(self):
        response = client.chat.completions.create(
                model="MiniMax-M2.7",
                messages=self.messages,
                tools=self.tools,
                extra_body={"reasoning_split": True}
            )
        return response
    
    def execute_tool(self, name, args):
        if name == "get_current_price":
            return get_current_price(**args)
        elif name == "get_historical_data":
            return get_historical_data(**args)
        elif name == "calculate_investment_return":
            return calculate_investment_return(**args)
        else:
            return f"Unknown tool: {name}"
        
    def chat(self, user_input, max_iters = 15):
        self.messages.append({"role": "user", "content": f"{user_input}"})
        self.steps = []
        self.state = AgentState.THINKING

        for i in range(max_iters):
            print(f"\n=== Step {i+1} ===")

            response = self.call_llm()
            msg = response.choices[0].message
            self.messages.append(msg.model_dump())

            if msg.tool_calls:
                self.state = AgentState.ACTING
                for tool_call in msg.tool_calls:
                    #执行
                    args = json.loads(tool_call.function.arguments)
                    function_name = tool_call.function.name
                    print(f"[行动] 调用工具: {function_name}, 参数: {args}")

                    result = self.execute_tool(function_name, args)
                    print(f"[观察] 结果: {result}")

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

                    self.steps.append({
                        "tool": function_name,
                        "args": args,
                        "result": result
                    })

            else:
                self.state = AgentState.DONE
                return msg.content
        
        self.state = AgentState.FAILED
        return "已达到最大对话轮次"
    
    def get_execution_trace(self):
        return self.steps