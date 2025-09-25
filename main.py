#!/usr/bin/env python3
"""
MCP实时服务主入口点
"""

import asyncio
import signal
import sys
from config import config
from mcp_server import MCPServer
from websocket_client import WebSocketClient
from tools.example_tools import GetCurrentTimeTool, WeatherLookupTool, CalculatorTool

class MCPRealtimeService:
    """MCP实时服务主类"""
    
    def __init__(self):
        self.mcp_server = MCPServer()
        self.ws_client = WebSocketClient(self.mcp_server)
        self.running = False
    
    def setup_signal_handlers(self):
        """设置信号处理器用于优雅关闭"""
        def signal_handler(sig, frame):
            print("\n接收到关闭信号，正在优雅关闭...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def register_tools(self):
        """注册所有可用工具"""
        # 注册示例工具
        self.mcp_server.register_tool(GetCurrentTimeTool())
        self.mcp_server.register_tool(WeatherLookupTool())
        self.mcp_server.register_tool(CalculatorTool())
        
        print("工具注册完成")
    
    async def run(self):
        """运行MCP服务"""
        try:
            config.validate()
            self.setup_signal_handlers()
            self.register_tools()
            
            print("正在连接到OpenAI实时API...")
            if await self.ws_client.connect():
                print("连接成功，开始服务...")
                self.running = True
                
                # 发送工具列表给大模型
                tools_info = await self.mcp_server.list_tools()
                await self.ws_client.send_message({
                    "type": "tools_announcement",
                    "tools": tools_info["tools"]
                })
                
                # 开始接收消息
                await self.ws_client.receive_messages()
            else:
                print("连接失败，请检查配置和网络连接")
                
        except Exception as e:
            print(f"服务运行错误: {e}")
        finally:
            await self.ws_client.close()
            print("服务已关闭")

async def main():
    """主函数"""
    service = MCPRealtimeService()
    await service.run()

if __name__ == "__main__":
    # 检查依赖
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"缺少依赖包: {e}")
        print("请运行: pip install websockets requests")
        sys.exit(1)
    
    # 运行服务
    asyncio.run(main())