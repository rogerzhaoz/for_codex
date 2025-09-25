import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, Any
from .base_tool import MCPTool

class GetCurrentTimeTool(MCPTool):
    """获取当前时间工具"""
    
    def __init__(self):
        super().__init__(
            name="get_current_time",
            description="获取当前的日期和时间"
        )
    
    async def execute(self, timezone: str = "UTC") -> Dict[str, Any]:
        try:
            current_time = datetime.now().isoformat()
            return {
                "success": True,
                "result": {
                    "timestamp": current_time,
                    "timezone": timezone
                },
                "message": f"当前时间: {current_time} ({timezone})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class WeatherLookupTool(MCPTool):
    """天气查询工具"""
    
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="查询指定城市的天气情况",
        )
    
    async def execute(self, city: str, unit: str = "celsius") -> Dict[str, Any]:
        try:
            # 注意：这里需要实际的天气API端点，目前为示例实现
            # 实际使用时需要替换为真实的天气服务API
            mock_weather_data = {
                "city": city,
                "temperature": 22,
                "unit": unit,
                "condition": "sunny",
                "humidity": 65
            }
            
            await asyncio.sleep(1)  # 模拟API调用延迟
            
            return {
                "success": True,
                "result": mock_weather_data,
                "message": f"{city}的天气: {mock_weather_data['temperature']}°{unit[0].upper()}, {mock_weather_data['condition']}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"天气查询失败: {str(e)}"
            }

class CalculatorTool(MCPTool):
    """简单计算器工具"""
    
    def __init__(self):
        super().__init__(
            name="calculate",
            description="执行简单的数学计算"
        )
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        try:
            # 安全评估数学表达式
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return {
                    "success": False,
                    "error": "表达式包含不安全字符"
                }
            
            result = eval(expression)  # 注意：生产环境需要更安全的方式
            
            return {
                "success": True,
                "result": result,
                "message": f"{expression} = {result}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"计算错误: {str(e)}"
            }