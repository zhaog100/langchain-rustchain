#!/usr/bin/env python3
"""
Example: LangChain agent using RustChainTool.

Prerequisites:
    pip install langchain-rustchain langchain-openai

Set OPENAI_API_KEY environment variable before running.
"""

from langchain_rustchain import RustChainTool

def demo_without_agent():
    """Demo the tool directly without an LLM agent."""
    tool = RustChainTool()

    print("=== RustChain Tool Demo ===\n")

    # 1. Check node health
    print("1. Node Health:")
    print(tool._run("get_health"))
    print()

    # 2. Get current epoch
    print("2. Current Epoch:")
    print(tool._run("get_epoch"))
    print()

    # 3. Check balance
    print("3. Wallet Balance (zhaog100):")
    print(tool._run("check_balance", wallet_id="zhaog100"))
    print()

    # 4. Network stats
    print("4. Network Stats:")
    print(tool._run("get_stats"))
    print()

    # 5. Transaction history
    print("5. Transaction History:")
    print(tool._run("get_wallet_history", wallet_id="zhaog100", limit=5))
    print()


def demo_with_agent():
    """Demo the tool with a LangChain agent (requires OPENAI_API_KEY)."""
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY to run agent demo")
        return

    from langchain_openai import ChatOpenAI
    from langchain.agents import initialize_agent, AgentType
    from langchain_rustchain import RustChainTool

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = initialize_agent(
        [RustChainTool()],
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    queries = [
        "What is the current epoch on RustChain and how many miners are enrolled?",
        "Check the balance of wallet zhaog100",
        "Is the RustChain node healthy? What version is it running?",
    ]

    for q in queries:
        print(f"\nQ: {q}")
        result = agent.run(q)
        print(f"A: {result}")


if __name__ == "__main__":
    demo_without_agent()
    # demo_with_agent()  # Uncomment if OPENAI_API_KEY is set
