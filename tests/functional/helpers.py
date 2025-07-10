from typing import Any, Dict, List, Optional, Union

from kissllm.client import State
from kissllm.stream import CompletionStream


class StateForTest(State):
    def __init__(
        self,
        messages,
        use_flexible_toolcall=True,
        tool_registry=None,
        use_tools: Optional[List[Dict[str, Any]]] | bool = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = "auto",
    ):
        super().__init__(use_flexible_toolcall, tool_registry, use_tools, tool_choice)
        self._messages = messages

    async def accumulate_response(self, response):
        if isinstance(response, CompletionStream):
            print("\n======Streaming Assistant Response:======")
            async for content in response.iter_content():
                if not content:
                    continue
                print(content, end="", flush=True)
            print("\n")

        return await super().accumulate_response(response)
