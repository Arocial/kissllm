from kissllm.client import State
from kissllm.stream import CompletionStream


class StateForTest(State):
    def __init__(
        self,
        messages,
        use_flexible_toolcall=True,
        tool_registry=None,
    ):
        super().__init__(use_flexible_toolcall, tool_registry)
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
