import os
from typing import Dict, Any

class Config:
    """配置管理类"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.app_token = os.getenv("MCP_APP_TOKEN", "your-app-token-here")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4")
        self.websocket_url = os.getenv("OPENAI_WS_URL", "wss://api.openai.com/v1/realtime")
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
    def validate(self) -> bool:
        """验证配置完整性"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not self.app_token:
            raise ValueError("MCP_APP_TOKEN environment variable is required")
        return True

config = Config()