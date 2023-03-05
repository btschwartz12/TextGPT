# WingmanGPT

## Overview
WingmanGPT is a command-line tool that allows you to send text messages that are customly modified by ChatGPT and sent to a specified number. 

[PyPi](https://pypi.org/project/WingmanGPT/) • [GitHub](https://github.com/btschwartz12/WingmanGPT/)

### Notice
`This tool currently only works for Mac users.`

Messages can be generated on any platform, but this tool uses the Messages app on Mac to send them. There are no plans currently to use a SMS API such as Twilio.

## Install

1. Make sure you have [python3](https://wiki.python.org/moin/BeginnersGuide/Download) and [pip](https://pip.pypa.io/en/stable/installation/) installed. You can then install the package directly from pip.

```bash
$ python3 -m venv env && source env/bin/activate # optional virtual environment
$ pip install WingmanGPT
```

2. Get your API token from your [OpenAI session data](https://chat.openai.com/api/auth/session) (copy the value for the `access_token` key). *Make sure you are signed in before doing this. You can get your token by accessing the linked url and copying the value for the 'accessToken' key.*

```bash
$ WingmanGPT make-token <token> 
$ cat token
<token>
```
3. **Optional**: make a template message file. This allows you to not have to provide a message as a command-line option.

```bash
$ WingmanGPT make-message "My custom message"
$ cat message
My custom message
```

## Usage

Please note that when running the program, you will get a warning from your Mac asking you if it can send a message. You must click OK for the tool to work.

```
Usage: WingmanGPT send [OPTIONS]

REQUIRED:
(-n, --number) [NUMBER]: 
    Phone number to send the message to.

OPTIONAL:
(-t, --token) [TOKEN]: 
    ChatGPT API token. Not required if you make a token file in step 2 of installation.

(-m, --message) [MESSAGE]: 
    Message to be modified. Not required if you make a message file in step 3 of installation.

(--noconfirm): 
    Optional flag that will send the message without confirmation.

(--mode) [MODE]: 
    Modification mode for your message. Check out prompts.json to see the modes the tool actually uses, as well as the default.

(-h, --help): 
    Show this message and exit.
```
### Example Usage

```bash
$ WingmanGPT send -n 1234567890 --mode=FUN --noconfirm -m "Tell me something about dogs" -t <token>
```
or
```bash
# Make a token file for multiple requests (step 2)
$ WingmanGPT make-token <token>
Token file created.
# Make a message file for multiple requests (step 3)
$ WingmanGPT make-message "I want a new dog"
Message file created.
# View available modes
$ WingmanGPT show-modes
...
# Send message
WingmanGPT send -n 1234567890 --mode=FUN
```

## ChatGPT Functionality

The ChatGPT wrapper class, [GPT](src/GPT.py) was inspired by acheong08's work on [ChatGPT API](https://github.com/acheong08/ChatGPT).

Everything that is used for the prompt, as well as the different modes, can be found in [prompts](src/prompts.py). 

To see all of the available modes from the command line, you can run:

```bash
$ WingmanGPT show-modes
```

## Build from Source

If you fork this repo and want to build the package locally, you can run these commands:

```bash
# Create virtual environment
python3 -m venv env && source env/bin/activate
# Install dependencies and build package
pip install -r requirements.txt
pip install -e .
# Verify installation
which WingmanGPT
.../your/path/to/WingmanGPT/env/bin/WingmanGPT
```

## Contributing

Anybody except Ho Jung Kim is allowed to contribute.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Authors
- Ben Schwartz, Ryan Baxter, and Paul Chafetz
