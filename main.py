from agent_core import AgentState, Agent


if __name__ == "__main__":
    agent = Agent("""
    你是一个专业的投资分析 Agent。
    用户会给你一个投资问题，你需要：
    1. 先获取相关股票价格
    2. 进行计算分析
    3. 给出明确的投资建议

    每次行动后，等待观察结果，再决定下一步。
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
