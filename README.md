# langchain-rustchain

> Native LangChain tool for RustChain — the DePIN blockchain for vintage hardware.

[![PyPI](https://img.shields.io/pypi/v/langchain-rustchain)](https://pypi.org/project/langchain-rustchain/)

## Install

```bash
pip install langchain-rustchain
```

## Quick Start

```python
from langchain_rustchain import RustChainTool

tool = RustChainTool()

# Check balance
print(tool.check_balance("zhaog100"))
# {"amount_i64": 90000000, "amount_rtc": 90.0, "miner_id": "zhaog100"}

# Get epoch info
print(tool.get_epoch())
# {"epoch": 135, "slot": 19554, "enrolled_miners": 16, ...}

# Node health
print(tool.get_health())
# {"ok": true, "version": "2.2.1-rip200", ...}
```

## Use with LangChain Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_rustchain import RustChainTool

llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    [RustChainTool()],
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

result = agent.run("What is the balance of wallet zhaog100 on RustChain?")
print(result)
```

## Available Actions

| Action | Description | Auth Required |
|--------|-------------|---------------|
| `check_balance` | Check wallet RTC balance | No |
| `get_epoch` | Current epoch/slot info | No |
| `get_health` | Node health & version | No |
| `get_stats` | Network statistics | No |
| `get_wallet_history` | Transaction history | No |
| `get_balance_all` | All balances (admin) | Yes |

## Bounty

This tool was built for [RustChain Bounty #3074](https://github.com/Scottcjn/rustchain-bounties/issues/3074) — 25 RTC + bonuses.

## License

MIT
