#!/usr/bin/env python3
"""Example agent using RustChain LangChain tool."""
from langchain_rustchain import RustChainTool

def main():
    """Demonstrate RustChain LangChain tool usage."""
    print("🌾 RustChain LangChain Tool Demo")
    print("=" * 40)
    
    # Initialize tool
    tool = RustChainTool()
    
    # Check balance
    print("1. Checking wallet balance...")
    try:
        balance = tool.check_balance("zhaog100")
        print(f"   ✅ Balance: {balance} RTC")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # List bounties
    print("\n2. Listing bounties...")
    try:
        bounties = tool.list_bounties(limit=3)
        for i, bounty in enumerate(bounties, 1):
            print(f"   {i}. {bounty['title']} ({bounty['reward_rtc']} RTC)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get node health
    print("\n3. Checking node health...")
    try:
        health = tool.get_node_health()
        print(f"   ✅ Version: {health.get('version', 'unknown')}")
        print(f"   ✅ Uptime: {health.get('uptime_s', 0)} seconds")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get current epoch
    print("\n4. Getting current epoch...")
    try:
        epoch = tool.get_current_epoch()
        print(f"   ✅ Epoch: {epoch.get('epoch', 'unknown')}")
        print(f"   ✅ Miners: {epoch.get('enrolled_miners', 0)}")
        print(f"   ✅ Pot: {epoch.get('epoch_pot', 0)} RTC")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Demo completed successfully!")
    print("The RustChain LangChain tool is ready for agent integration.")

if __name__ == "__main__":
    main()
