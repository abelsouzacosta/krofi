## Krofi

Krofi is a simple credential clipper tool that allows the user to get entries from its
KeeepassXc database using [rofi](https://github.com/davatorium/rofi) interface.

## How it works?

Krofi will ask for the credentials of the KeeepassXc database at the startup, then if the
password is correct it will list all the entries of the database, you can use the input
to select for a specific instance. Then you can press the following keys:

- Alt+u: to get the username
- Alt+p: to get the password
- Alt+t: to get the otp

After pressing one of the key combinations above you will have the respective credential
in your clipboard and the interface will close to re-open again after 10 seconds, allowing
you to copy another credential, after this 10 seconds the credentials will be cleared from
the clipboard.

You can exit from krofi after pressing Alt+x

## Install

In order to install this package you must have [poetry](https://python-poetry.org/) installed.

1 - Clone this repository

`git clone git@github.com:abelsouzacosta/krofi.git && cd krofi`

2 - Install all dependencies

`poetry install`

3 - Compile

`poetry run pyinstaller --onefile --add-data "/path/to/rofi/config:rofi_config" krofi/main.py`

This will create a `dist` directory with a `main` script inside it that you can execute
