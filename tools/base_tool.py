from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import inspect

class MCPTool(ABC):
    """MCP工具基类:cite[4]"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters = self._get_parameter_schema()
    
    def _get_parameter_schema(self) -> Dict[str, Any]:
        """从方法签名自动生成参数模式"""
        sig = inspect.signature(self.execute)
        parameters = {}
        
        for param_name, param in list(sig.parameters.items())[1:]:  # 跳过self
            param_info = {
                "type": self._python_type_to_json(param.annotation),
                "description": f"Parameter {param_name}",
                "required": param.default == param.empty
            }
            parameters[param_name] = param_info
        
        return {
            "type": "object",
            "properties": parameters,
            "required": [name for name, param in parameters.items() if param["required"]]
        }
    
    @staticmethod
    def _python_type_to_json(python_type: type) -> str:
        """Python类型转JSON schema类型"""
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        return type_map.get(python_type, "string")
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具操作"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，用于工具发现"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }