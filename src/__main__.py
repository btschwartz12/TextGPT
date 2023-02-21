"""Main module for the WingmanGPT program."""

# pylint: disable=invalid-name,broad-exception-raised,broad-exception-caught


from dataclasses import dataclass
import json
import os
import subprocess
import shlex
from typing import List
import click
from revChatGPT.V1 import Chatbot


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


class WingmanGPT:
    """Command-line tool that generates and sends text messages."""

    def __init__(self,
                 number: str,
                 noconfirm: bool,
                 token: str,
                 message: str,
                 mode: ResponseMode,
                 prompt_data: PromptData):
        """Take a message, give it to chatGPT, send response to number."""
        # Command line arguments
        self.__phone_number = self.__get_phone_number(number)
        self.__token = self.__get_token(token)
        self.__message = self.__get_message(message)
        self.__wants_to_confirm = not noconfirm
        # Prompt data
        self.__prompt_data: PromptData = prompt_data
        # Mode
        self.__mode_modification = self.__get_mode_modification(mode)

    def __get_token(self, token):
        """Get the token to be used for the ChatGPT API.

        It will first check to see if the token is passed as an argument.
        If not, it will check to see if there is a token file.
        If not, it will throw an error.
        """
        # First see if it is passed as an argument
        if isinstance(token, str) and token != "":
            return token
        # Now check to see if there is a token file
        if os.path.exists("token"):
            with open("token", "r", encoding='utf-8') as f:
                tok = f.read()
                if tok != "":
                    return tok
        # Now throw an error
        raise Exception("No token provided or found in token file")

    def __get_phone_number(self, number):
        """Get the phone number to send the message to.

        If the phone nuber is not a string or is not 10 characters long,
        it will throw an error.
        """
        if not isinstance(number, str) or len(number) != 10:
            raise Exception("Invalid phone number")
        # Make sure all of the characters are digits
        for char in number:
            if not char.isdigit():
                raise Exception("Invalid phone number")
        return number

    def __get_message(self, message):
        """Get the message to be used for the prompt for ChatGPT.

        First check to see if the message is passed as an argument.
        If not, check to see if there is a message.txt file.
        If not, throw an error.
        """
        # First see if it is passed as an argument
        if isinstance(message, str) and message != "":
            return message
        # Now check to see if there is a message.txt file
        if os.path.exists("message.txt"):
            with open("message.txt", "r", encoding='utf-8') as f:
                msg = f.read()
                if msg != "":
                    return msg
        # Now throw an error
        raise Exception("No message provided or found in message.txt")

    def __get_mode_modification(self, mode_str) -> str:
        """Get response mode to be used for the prompt for ChatGPT.

        If no mode is provided, it will default to ROMANTIC.
        If an invalid mode is provided, it will throw an error.
        """
        available_modes = {response_mode.NAME:
                           response_mode.PROMPT_MODIFICATION
                           for response_mode in self.__prompt_data.MODES}

        if mode_str is None or mode_str == "":
            # Default
            return available_modes[self.__prompt_data.DEFAULT_MODE]
        if mode_str not in available_modes:
            raise Exception(f"Invalid mode: {mode_str}\n Available modes: \
                            {', '.join(available_modes.keys())}")
        return available_modes[mode_str]

    def __get_prompt(self):
        """Get the prompt to be used for the ChatGPT API."""
        PROMPT = ""

        PROMPT += " ".join(self.__prompt_data.PREFIX)
        PROMPT += f" Here is the message: \"{self.__message}\"."
        PROMPT += " Here is how I want you to modify the message: "
        PROMPT += f"\"{self.__mode_modification}\"."
        PROMPT += " ".join(self.__prompt_data.SUFFIX)

        return PROMPT

    def __get_response(self):
        """Get the ChatGPT Response."""
        # Get the prompt to be used
        PROMPT = self.__get_prompt()
        # Configure the ChatGPT API
        token = self.__token
        # strip any newlines from the token
        token = token.replace("\n", "")
        chatbot = Chatbot(config={
            # Change to bens bc hes rich boi
            "access_token": token
        })
        # Get the response
        response = ""
        for data in chatbot.ask(PROMPT):
            response = data["message"]
        # Strip the quotes from the response
        response = response[1:-1]
        return response

    def __send_message(self, response):
        """Send message to phone number."""
        # Properly escape special characters for a bash command
        prepared_response = "\"" + shlex.quote(response)[1:-1] + "\""
        # Send the message
        command = "osascript -e 'tell application \"Messages\" to send "
        command += f"{prepared_response} to buddy \"{self.__phone_number}\"'"
        try:
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            raise Exception(f"Failed to send message: \n\n{e}") from e

    def execute(self):
        """Execute the program.

        This will first get the response from ChatGPT,
        then it will ask the user if they want to send the message,
        and then it will send the message.
        """
        try:
            response = self.__get_response()
        except Exception as e:
            print(e)
            print('Failed to get response from ChatGPT API')
            return
        # Try to send the message
        try:
            if self.__wants_to_confirm:
                print(f"********\nMessage: {response}\n********")
                confirm = input("Send message? (y/n): ")
                if confirm.lower() != "y":
                    print("Message not sent.")
                    return
            self.__send_message(response)
            print('Message Sent.')
        except Exception as e:
            print(f'Failed to send message. \n\n{e}')


def get_prompt_data() -> PromptData:
    """Get the prompt data from the prompt_data.json file."""
    # If prompts.json does not exist, throw an error
    if not os.path.exists("prompts.json"):
        raise Exception("prompts.json does not exist")
    with open("prompts.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        modes = []
        for mode in data["modes"]:
            modes.append(ResponseMode(mode["name"],
                                      mode["description"],
                                      mode["modifier"]))
        return PromptData(data["prefix"],
                          data["suffix"],
                          modes,
                          data["default_mode"])


@click.command()
# Required arguments
@click.option('-n', '--number', help='Phone number to send the message to.')
# Optional arguments
@click.option('-t', '--token', help='ChatGPT API token.')
# confirmation
@click.option('--noconfirm', is_flag=True,
              help='Do not confirm before sending the message.')
@click.option('-m', '--message', help='Message to send.')
@click.option('--mode', help='Mode to use for sending the message.')
@click.option('--show-modes', is_flag=True, help='Show available modes.')
def main(number, noconfirm, token, message, mode, show_modes):
    """Tool for sending messages to a phone number."""
    # Get the prompt data
    try:
        prompt_data: PromptData = get_prompt_data()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return
    # If show_modes is true, show the modes and exit
    if show_modes:
        prompt_data.show_modes()
        return
    # Make sure phone number is provided
    if number is None:
        print("Phone number is required.")
        return
    # Instantiate WingmanGPT object
    try:
        tgpt = WingmanGPT(number=number, noconfirm=noconfirm, token=token,
                          message=message, mode=mode, prompt_data=prompt_data)
        tgpt.execute()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
