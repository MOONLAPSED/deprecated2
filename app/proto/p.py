import json

from typing import Any
from typing import Dict

from dataclasses import dataclass

@dataclass
class PromptData:
    name: str
    version: int
    
@dataclass    
class Prompt:
    data: PromptData



async def test_prompt():
  p = Prompt(PromptData("test", 1))
  print(p)

if __name__ == "__main__":
  import asyncio
  asyncio.run(test_prompt())

