"""
RustChain LangChain Tool
========================
A LangChain BaseTool subclass for interacting with RustChain nodes.

Install:
    pip install langchain-rustchain

Usage:
    from langchain_rustchain import RustChainTool
    tool = RustChainTool()
    result = tool.check_balance("zhaog100")

Agent usage:
    from langchain.agents import initialize_agent, AgentType
    from langchain_rustchain import RustChainTool
    agent = initialize_agent([RustChainTool()], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    agent.run("What is the current epoch on RustChain?")
"""

import json
from typing import Optional, Type, Dict, Any, List

import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


# Default public node (verified 2026-04-17)
DEFAULT_NODE_URL = "https://rustchain.org"
# Fallback direct IP (self-signed TLS)
FALLBACK_NODE_URL = "https://50.28.86.131"


class RustChainToolSchema(BaseModel):
    """Input schema for RustChainTool."""
    action: str = Field(
        description=(
            "One of: check_balance, get_epoch, get_health, get_stats, "
            "get_wallet_history, get_balance_all. "
            "For check_balance, also provide 'wallet_id'. "
            "For get_wallet_history, also provide 'wallet_id' and optionally 'limit'."
        )
    )
    wallet_id: Optional[str] = Field(
        default=None,
        description="RustChain wallet/miner ID (e.g., 'zhaog100'). Required for check_balance and get_wallet_history."
    )
    limit: Optional[int] = Field(
        default=10,
        description="Number of results to return (for history queries)."
    )


class RustChainTool(BaseTool):
    """RustChain blockchain tool for LangChain agents.
    
    Provides access to RustChain node API endpoints including:
    - Wallet balance checks
    - Epoch information
    - Node health monitoring
    - Network statistics
    - Transaction history
    
    The RustChain API is agent-native: no auth required for read endpoints,
    wallet IDs are simple strings, and responses are JSON.
    """
    
    name: str = "rustchain"
    description: str = (
        "RustChain blockchain tool. Check wallet balances, get epoch info, "
        "monitor node health, view network stats, and query transaction history. "
        "No authentication required for read operations."
    )
    args_schema: Type[BaseModel] = RustChainToolSchema
    
    node_url: str = Field(default=DEFAULT_NODE_URL)
    timeout: int = Field(default=10)
    verify_ssl: bool = Field(default=True)
    
    def _make_request(self, endpoint: str, method: str = "GET", json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a request to the RustChain node API."""
        url = f"{self.node_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            resp = requests.request(
                method, url,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.SSLError:
            # Fallback to direct IP with self-signed cert
            if self.node_url != FALLBACK_NODE_URL:
                fallback_url = f"{FALLBACK_NODE_URL}/{endpoint.lstrip('/')}"
                resp = requests.request(
                    method, fallback_url,
                    json=json_data,
                    timeout=self.timeout,
                    verify=False,
                )
                resp.raise_for_status()
                return resp.json()
            raise
        except requests.exceptions.RequestException as e:
            return {"ok": False, "error": str(e)}
    
    def check_balance(self, wallet_id: str) -> Dict[str, Any]:
        """Check the RTC balance of a wallet."""
        return self._make_request(f"/wallet/balance?miner_id={wallet_id}")
    
    def get_epoch(self) -> Dict[str, Any]:
        """Get current epoch information."""
        return self._make_request("/epoch")
    
    def get_health(self) -> Dict[str, Any]:
        """Get node health status."""
        return self._make_request("/health")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get network statistics."""
        return self._make_request("/api/stats")
    
    def get_wallet_history(self, wallet_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get transaction history for a wallet."""
        return self._make_request(f"/wallet/history?miner_id={wallet_id}&limit={limit}")
    
    def get_balance_all(self) -> Dict[str, Any]:
        """Get total balance information (requires admin, may fail)."""
        return self._make_request("/wallet/balances/all")
    
    def _run(
        self,
        action: str,
        wallet_id: Optional[str] = None,
        limit: int = 10,
    ) -> str:
        """Execute the requested action."""
        action = action.lower().strip()
        
        if action == "check_balance":
            if not wallet_id:
                return "Error: wallet_id is required for check_balance"
            result = self.check_balance(wallet_id)
            if "error" in result:
                return f"Error: {result['error']}"
            return (
                f"Wallet: {result.get('miner_id', wallet_id)}\n"
                f"Balance: {result.get('amount_rtc', 0)} RTC "
                f"({result.get('amount_i64', 0)} uRTC)"
            )
        
        elif action == "get_epoch":
            result = self.get_epoch()
            return (
                f"Epoch: {result.get('epoch', 'N/A')}\n"
                f"Slot: {result.get('slot', 'N/A')}\n"
                f"Enrolled Miners: {result.get('enrolled_miners', 'N/A')}\n"
                f"Epoch Pot: {result.get('epoch_pot', 'N/A')} RTC\n"
                f"Total Supply: {result.get('total_supply_rtc', 'N/A')} RTC"
            )
        
        elif action == "get_health":
            result = self.get_health()
            return (
                f"Node Status: {'OK' if result.get('ok') else 'DOWN'}\n"
                f"Version: {result.get('version', 'N/A')}\n"
                f"Uptime: {result.get('uptime_s', 0)}s\n"
                f"DB Read/Write: {result.get('db_rw', 'N/A')}\n"
                f"Backup Age: {result.get('backup_age_hours', 'N/A')}h"
            )
        
        elif action == "get_stats":
            result = self.get_stats()
            return (
                f"Chain: {result.get('chain_id', 'N/A')}\n"
                f"Version: {result.get('version', 'N/A')}\n"
                f"Epoch: {result.get('epoch', 'N/A')}\n"
                f"Total Miners: {result.get('total_miners', 'N/A')}\n"
                f"Total Balance: {result.get('total_balance', 'N/A')} RTC\n"
                f"Features: {', '.join(result.get('features', []))}"
            )
        
        elif action == "get_wallet_history":
            if not wallet_id:
                return "Error: wallet_id is required for get_wallet_history"
            result = self.get_wallet_history(wallet_id, limit)
            txs = result.get("transactions", [])
            if not txs:
                return f"No transactions found for {wallet_id}"
            lines = [f"History for {wallet_id} ({result.get('total', 0)} total):"]
            for tx in txs[:limit]:
                lines.append(
                    f"  [{tx.get('type', '?')}] {tx.get('amount', 0)} RTC "
                    f"from {tx.get('from', '?')} — {tx.get('reason', '')[:50]}"
                )
            return "\n".join(lines)
        
        elif action == "get_balance_all":
            result = self.get_balance_all()
            if "error" in result:
                return f"Error: {result.get('error', result.get('reason', 'unknown'))}"
            return json.dumps(result, indent=2)
        
        else:
            return (
                f"Unknown action: {action}. "
                f"Available: check_balance, get_epoch, get_health, get_stats, "
                f"get_wallet_history, get_balance_all"
            )
    
    async def _arun(self, action: str, wallet_id: Optional[str] = None, limit: int = 10) -> str:
        """Async version — delegates to sync for now."""
        return self._run(action, wallet_id, limit)
