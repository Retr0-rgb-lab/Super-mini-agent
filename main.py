from agent_core import AgentState, Agent

if __name__ == "__main__":

    agent = Agent("""
    你是一个专业的金融 Agent。
    用户会给你一个问题，你需要：
    1：理解问题
    2：决定是否要调用工具
    3：返回回答或工具调用结果
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