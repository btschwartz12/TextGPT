from dataclasses import dataclass
import json
import os
import subprocess
from typing import List 
import click
from revChatGPT.V1 import Chatbot
import shlex

from pprint import pprint

@dataclass
class ResponseMode():
    NAME: str
    PROMPT_MODIFICATION: str


@dataclass
class PromptData:
    """PromptData is a dataclass that holds the data for a prompt."""
    PREFIX: str
    SUFFIX: str
    MODES: List[ResponseMode]
    DEFAULT_MODE: str = "ROMANTIC"

class WingmanGPT:
    """WingmanGPT is a command-line tool that generates and sends text messages."""
    
    def __init__(self,  
                number: str, 
                confirm: bool, 
                token: str, 
                message: str, 
                mode: ResponseMode):
        """Take a message, give it to chatGPT, send response to number"""
        # Command line arguments
        self.__phone_number = self.__get_phone_number(number)
        self.__token = self.__get_token(token)
        self.__message = self.__get_message(message)
        self.__wants_to_confirm = True if not confirm else confirm
        # Prompt data
        self.__prompt_data: PromptData = self.__get_prompt_data()
        # Mode
        self.__mode_modification = self.__get_mode_modification(mode)

        # print all of the member variables, one for each line
        # print(f"Phone number: {self.__phone_number}\n\n")
        # print(f"Token: {self.__token}\n\n")
        # print(f"Message: {self.__message}\n\n")
        # print(f"Mode: {self.__mode_modification}\n\n")
        # print(f"Prompt data: {self.__prompt_data}\n\n")



    def __get_prompt_data(self) -> PromptData:
        """Get the prompt data from the prompt_data.json file"""
        # If prompts.json does not exist, throw an error
        if not os.path.exists("prompts.json"):
            raise Exception("prompts.json does not exist")
        with open("prompts.json", "r") as f:
            data = json.load(f)
            modes = []
            for mode in data["modes"]:
                modes.append(ResponseMode(mode["name"], mode["modifier"]))
            return PromptData(data["prefix"], data["suffix"], modes)

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
            with open("token", "r") as f:
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
            with open("message.txt", "r") as f:
                msg = f.read()
                if msg != "":
                    return msg
        # Now throw an error
        raise Exception("No message provided or found in message.txt")
        

    def __get_mode_modification(self, mode_str) -> str:
        """The response mode to be used for the prompt for ChatGPT.
        
        If no mode is provided, it will default to ROMANTIC.
        If an invalid mode is provided, it will throw an error.
        """
        available_modes = {response_mode.NAME: response_mode.PROMPT_MODIFICATION for response_mode in self.__prompt_data.MODES}

        if mode_str is None or mode_str == "":
            # Default
            return available_modes[self.__prompt_data.DEFAULT_MODE]
        if mode_str not in available_modes:
            raise Exception(f"Invalid mode: {mode_str}\n Available modes: {', '.join(available_modes.keys())}")
        return available_modes[mode_str]
        
    def __get_prompt(self):
        """Get the prompt to be used for the ChatGPT API"""
        PROMPT = ""

        PROMPT += self.__prompt_data.PREFIX
        PROMPT += f" Here is the message: \"{self.__message}\"." 
        PROMPT += f" Here is how I want you to modify the message: \"{self.__mode_modification}\"." 
        PROMPT += self.__prompt_data.SUFFIX

        return PROMPT
    
    def __get_response(self):
        """Get the ChatGPT Response"""
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

        # Properly escape special characters for a bash command, and remove single quotes
        prepared_response = "\"" + shlex.quote(response)[1:-1] + "\""
        # Send the message
        command = f"osascript -e 'tell application \"Messages\" to send {prepared_response} to buddy \"{self.__phone_number}\"'"
        subprocess.run(command, shell=True)

    def execute(self):
        """Execute the program"""
        try:
            response = self.__get_response()
        except Exception as e:
            print(e)
            print('Failed to get response from ChatGPT API')
            return

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
            print('Failed to send message.')



@click.command()
# Required arguments
@click.option('-n', '--number', required=True, help='Phone number to send the message to.')
# Optional arguments
@click.option('-t', '--token', help='ChatGPT API token.')
# confirmation 
@click.option('-c', '--confirm', is_flag=True, help='Confirm before sending the message.')
@click.option('-m', '--message', help='Message to send.')
@click.option('--mode', help='Mode to use for sending the message.')
def main(number, confirm, token, message, mode):
    """Tool for sending messages to a phone number."""
    # Instantiate WingmanGPT object

    # DEBUG = True
    # if DEBUG:
    #     number = '1234557890'
    #     confirm = None
    #     token = None
    #     message = '234234234'
    #     mode = 'ROMANTI'

    try:
        tgpt = WingmanGPT(number=number, confirm=confirm, token=token, message=message, mode=mode)
        tgpt.execute()
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    main()
