import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from config import config
from auth import authenticator

class MCPServer:
    """MCP服务器实现:cite[9]"""
    
    def __init__(self):
        self.tools = {}
        self.connected = False
        self.websocket = None
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """设置日志记录"""
        logger = logging.getLogger("mcp_server")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def register_tool(self, tool) -> None:
        """注册工具到MCP服务器"""
        self.tools[tool.name] = tool
        self.logger.info(f"注册工具: {tool.name}")
    
    async def list_tools(self) -> Dict[str, Any]:
        """返回可用工具列表:cite[4]"""
        return {
            "tools": [tool.to_dict() for tool in self.tools.values()],
            "count": len(self.tools)
        }
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """调用指定工具"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"工具未找到: {tool_name}"
            }
        
        try:
            tool = self.tools[tool_name]
            self.logger.info(f"调用工具: {tool_name}, 参数: {parameters}")
            
            result = await tool.execute(**parameters)
            return result
        except Exception as e:
            self.logger.error(f"工具调用错误: {str(e)}")
            return {
                "success": False,
                "error": f"工具执行失败: {str(e)}"
            }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理来自大模型的消息"""
        message_type = message.get("type", "")
        
        if message_type == "list_tools":
            tools_info = await self.list_tools()
            return {
                "type": "tools_list",
                "tools": tools_info["tools"],
                "timestamp": asyncio.get_event_loop().time()
            }
        
        elif message_type == "call_tool":
            tool_name = message.get("tool_name")
            parameters = message.get("parameters", {})
            
            result = await self.call_tool(tool_name, parameters)
            return {
                "type": "tool_result",
                "tool_name": tool_name,
                "result": result,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        else:
            return {
                "type": "error",
                "error": f"未知的消息类型: {message_type}",
                "timestamp": asyncio.get_event_loop().time()
            }