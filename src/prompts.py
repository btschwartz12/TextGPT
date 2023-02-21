"""Prompts used for WingmanGPT."""

from dataclasses import dataclass
from typing import List


@dataclass
class ResponseMode():
    """ResponseMode is a dataclass that holds the data for a response mode."""
    NAME: str
    DESCRIPTION: str
    PROMPT_MODIFICATION: str


@dataclass
class PromptData:
    """PromptData is a dataclass that holds the data for a prompt."""
    PREFIX: str
    SUFFIX: str
    MODES: List[ResponseMode]
    DEFAULT_MODE: str

    def show_modes(self):
        """Show the modes."""
        print('AVAILABLE MODES:')
        for mode in self.MODES:
            print(f"\t{mode.NAME}: {mode.DESCRIPTION}")

# The prefix to the prompt
__prefix = [
    "I am going to ask you to take a message, and then modify it or make it better in a certain way.",
    "I am going to give you the message witin double quotes, then after I will give you what I want to do to the message.",
    "I want you to take the message and modify it, and then print back only the modify message, no headers or anything about your message.",
    "This means that the message you give back to me will be one paragraph, just the modified message.",
    "I am going to give you the message now."
]

# The suffix is the same for all modes
__suffix = [
    "Please compute the modified message and give me back only the message, put in double quotes.",
        "No emojis.",
        "ONLY GIVE ME THE MODIFIED MESSAGE, DO NOT SAY ANYTHING ELSE."
]

__modes = [
    ResponseMode(
        NAME="ROMANTIC",
        DESCRIPTION="Make the message sound more romantic",
        PROMPT_MODIFICATION="Can you make this sound better to send to my girlfriend?"
    ),
    ResponseMode(
        NAME="FUN",
        DESCRIPTION="Make the message sound satirical",
        PROMPT_MODIFICATION="can you make this sound more satirical to send to my girlfriend?"
    ),
    ResponseMode(
        NAME="STORY",
        DESCRIPTION="Turn the message into a short story",
        PROMPT_MODIFICATION="can you tell me a short story about this, that is dark yet promising?"
    ),
    ResponseMode(
        NAME="POETIC",
        DESCRIPTION="Make the message sound more poetic",
        PROMPT_MODIFICATION="Can you make this sound more poetic?"
    ),
    ResponseMode(
        NAME="SEDUCTIVE",
        DESCRIPTION="Make the message sound seductive",
        PROMPT_MODIFICATION="Can you make this sound like I am trying to lure this girl?"
    ),
    ResponseMode(
        NAME="DEROGATORY",
        DESCRIPTION="Make the message sound mean",
        PROMPT_MODIFICATION="Can you make this sound like I am trying to piss this person up?"
    ),
    ResponseMode(
        NAME="PERSUASIVE",
        DESCRIPTION="Make the message sound more persuasive",
        PROMPT_MODIFICATION="Can you make this sound more persuasive?"
    ),
    ResponseMode(
        NAME="BUSINESS",
        DESCRIPTION="Make the message sound more formal",
        PROMPT_MODIFICATION="Can you make this sound more formal? I am sending this message to my business partner"
    ),
    ResponseMode(
        NAME="SAVAGE",
        DESCRIPTION="Make it SAVAGE",
        PROMPT_MODIFICATION="Can you make this sound more savage? I am sending this message to someone I dislike"
    )
]

prompt_data = PromptData(
    PREFIX=__prefix,
    SUFFIX=__suffix,
    MODES=__modes,
    DEFAULT_MODE="ROMANTIC"
)

__all__ = ["prompt_data"]
