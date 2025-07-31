import readline as readline
from dataclasses import dataclass
from enum import Enum, auto

from kissllm.utils import format_prompt


@dataclass
class OutputMetadata:
    pass


class IOChannel:
    def __init__(self, channel_type):
        self.channel_type = channel_type

    def create_sub_channel(self, channel_type, title=""):
        print()
        return self.__class__(channel_type)

    async def read(self):
        try:
            while True:
                line = input("User (Ctrl+D to quit): ")
                yield line
        except EOFError:
            pass

    async def write(self, content, metadata: OutputMetadata | None = None):
        if self.channel_type == IOTypeEnum.prompt_message:
            print("\n".join(format_prompt(content)))
        elif self.channel_type == IOTypeEnum.streaming_assistant:
            print(content, end="", flush=True)
        else:
            print(content)


class IOTypeEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    prompt_message = auto()
    streaming_assistant = auto()
