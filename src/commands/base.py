from typing import Any
from mypy.error_formatter import ABC



class BaseCommand(ABC):
    id: str = ""
    description: str = ""

    async def  execute(self, **kwargs: Any) -> Any:
        pass
