# Copyright (c) 2026 思捷娅科技 (SJYKJ) — MIT License
"""RustChain Tool - Integrate RustChain as a native LangChain tool."""

import os
import urllib.request
import urllib.error
import json
from typing import Optional, Type

from pydantic import BaseModel, Field

try:
    from langchain_core.tools import BaseTool
except ImportError:
    from langchain.tools import BaseTool


class RustChainToolInput(BaseModel):
    """Input for RustChainTool."""
    action: str = Field(
        description="Action: check_balance, list_bounties, get_node_health, get_current_epoch"
    )
    wallet_id: Optional[str] = Field(default=None, description="Wallet ID")
    limit: Optional[int] = Field(default=10, description="Bounty limit")


class RustChainTool(BaseTool):
    """Tool for interacting with the RustChain API."""

    name: str = "rustchain_tool"
    description: str = (
        "Interact with RustChain blockchain. "
        "Actions: check_balance, list_bounties, get_node_health, get_current_epoch"
    )
    args_schema: Type[BaseModel] = RustChainToolInput

    base_url: str = Field(default="https://rustchain.org")
    wallet_id: str = Field(default_factory=lambda: os.environ.get("RUSTCHAIN_DEFAULT_WALLET", "agent"))

    def _run(self, action: str, wallet_id: Optional[str] = None, limit: int = 10) -> str:
        return self._execute(action, wallet_id, limit)

    async def _arun(self, action: str, wallet_id: Optional[str] = None, limit: int = 10) -> str:
        return self._execute(action, wallet_id, limit)

    def _execute(self, action: str, wallet_id: Optional[str], limit: int) -> str:
        wid = wallet_id or self.wallet_id
        headers = {"User-Agent": "RustChain-LangChain-Tool/1.0", "Accept": "application/json"}
        
        endpoints = {
            "check_balance": f"{self.base_url}/api/wallet/{wid}/balance",
            "list_bounties": f"{self.base_url}/api/bounties?limit={limit}",
            "get_node_health": f"{self.base_url}/api/node/health",
            "get_current_epoch": f"{self.base_url}/api/epoch",
        }
        
        url = endpoints.get(action)
        if not url:
            return f"Error: Unknown action '{action}'. Available: {list(endpoints.keys())}"
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return json.dumps(data, indent=2, default=str)
        except urllib.error.HTTPError as e:
            return f"HTTP Error {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"URL Error: {e.reason}"
        except Exception as e:
            return f"Error: {e}"
