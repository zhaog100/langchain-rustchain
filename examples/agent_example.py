# Copyright (c) 2026 思捷娅科技 (SJYKJ) — MIT License
"""Example: Using RustChain Tool with LangChain Agent."""

import os
from langchain_rustchain import RustChainTool

os.environ.setdefault("RUSTCHAIN_DEFAULT_WALLET", "zhaog100")
tool = RustChainTool()

print("=== Testing RustChain Tool ===\n")
print("1. Node Health:", tool.invoke({"action": "get_node_health"})[:100])
print("2. Epoch:", tool.invoke({"action": "get_current_epoch"})[:100])
print("3. Bounties:", tool.invoke({"action": "list_bounties", "limit": 3})[:100])
print("4. Balance:", tool.invoke({"action": "check_balance", "wallet_id": "zhaog100"})[:100])
