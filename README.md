# WingmanGPT

## Overview
WingmanGPT is a command-line tool that allows you to send text messages that are customly modified by ChatGPT and sent to a specified number. 

### Notice
`This tool currently only works for Mac users.`

## Install

1. Clone the repository and `cd` to it.

```bash
$ git clone https://github.com/btschwartz12/WingmanGPT.git
$ cd /your/path/to/WingmanGPT
$ pwd
/your/path/to/WingmanGPT
```

2. Run the `install.sh` script, using the `source` command, activating the virtual environment
```bash
$ source install.sh
...
Successfully installed WingmanGPT-1.0.0
...
$ echo $VIRTUAL_ENV
/your/path/to/WingmanGPT/env
```

3. Verify the package exists in the envirnoment
```bash
$ which WingmanGPT
/your/path/to/WingmanGPT/env/bin/WingmanGPT
```

4. Get your API token from [OpenAI](https://chat.openai.com/api/auth/session), and initialize it for the tool. *Make sure you are signed in before doing this. You can get your token by accessing the linked url and copying the value for the 'accessToken' key.*

```bash
$ base make_token.sh [token]
$ cat token
...
your token
...
```
5. **Optional**: make a template message file. This allows you to not have to provide a message as a command-line option.

```bash
$ touch message.txt
$ echo 'My example message' > message.txt
```




## Usage

Please note that when running the program, you will get a warning from your Mac asking you if it can send a message. You must click OK for the tool to work.

```
Usage: WingmanGPT [OPTIONS]

REQUIRED:
(-n, --number): 
    Phone number to send the message to.

OPTIONAL:
(-t, --token) [TOKEN]: 
    ChatGPT API token. Not required if you make a token file in step 4 of installation.

(-m, --message) [MESSAGE]: 
    Message to be modified. Not required if you make a message file in step 5 of installation

(-c --confirm): 
    Optional flag that asks for confirmation before sending the message. Defaults to true.

(--mode) [MODE]: 
    Modification mode for your message. Default is romantic, but check out the [prompt data](prompts.json) to see the modes the tool actually uses.Default is ROMANTIC.

```


## ChatGPT Prompt

Everything that is used for the prompt, as well as the different modes, can be found in [prompts.json](prompts.json). 

Here is a short description of each mode:

- **ROMANTIC**: Generates a romantic message using ChatGPT.
- **FUN**: Generates a fun message using ChatGPT.

## Contributing

add to me :(

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Authors
- Ben Schwartz & Ryan Baxter

