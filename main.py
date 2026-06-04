from agent_core import AgentState, Agent

if __name__ == "__main__":
    
    agent = Agent("""
    你是一个专业的金融研究助手。
    你可以：
    1. 使用 lookup_financial_report 检索本地知识库
    2. 使用 web_search 搜索互联网
    3. 使用 get_current_price 获取实时股价
    4. 使用 get_historical_data 获取历史数据
    5. 使用 calculate_investment_return 计算投资收益
    
    你必须：
    - 在回答中使用 [1], [2] 等格式标注引用来源
    - 只引用实际检索到的内容，不要编造引用
    - 如果没有检索到相关信息，明确告知用户
    """)
    

    print("=== 金融 Agent 多轮对话 ===")
    print("输入 N 或 n 退出程序\n")

    while True:
        user_input = input("Enter: ")
        if user_input.lower() == "n":
            print("程序结束")
            break

        result = agent.chat(user_input)
        print(f"\nAI: {result}")
        print()