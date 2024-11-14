from rofi import Rofi
from os import getenv
from pykeepass import PyKeePass
from subprocess import run
from pyperclip import copy
from time import sleep
from urllib import parse
from pyotp import TOTP

# initializes rofi
rofi_instance = Rofi()

# this command will run in a subprocess
# i couldn't make the python library for rofi execute
# dmenu with the '-password' parameter, so this is a workaround
command = ["rofi", "-dmenu", "-p", "Enter database password: ", "-password"]

# will get the database password
# if any is given returns an error
credential = run(command, capture_output=True, text=True).stdout.strip()
if not credential:
    rofi_instance.exit_with_error("Please provide valid credentials")

# get the database through a environment variable
# the environment variable KPDB should be a absolute path your .kbdx file
# like /home/<youruser>/dir/dir1/Pass.kbdx
database_path = getenv("KPDB")
# open database and validate credentials
try:
    keepass_database = PyKeePass(database_path, password=credential)
except Exception:
    rofi_instance.exit_with_error("Was not possible to open the database")

# get all groups from the database
groups = keepass_database.groups

# grouping all the group names into a list
group_options = [group.name for group in groups]

index_group, key_group = rofi_instance.select("Groups", options=group_options)

# get the selected group in the previous step
selected_group = groups[index_group]

# get all entries from the selected group
entries_options = [entry.title for entry in selected_group.entries]

index_entry, key_entry = rofi_instance.select(
    f"Entries at {groups[index_group]}",
    options=entries_options,
    key1=("Alt+u", "Copy username"),
    key2=("Alt+p", "Copy password"),
    key3=("Alt+t", "Copy TOTP"),
)

# get the selected entry in the previous step
selected_entry = selected_group.entries[index_entry]


# will get the secret of the otp uri attribute
def get_secret_from_uri(uri):
    # Will return a parsed url
    parsed_uri = parse.urlparse(uri)
    # Get the parameters of the uri parsing them into a dictionary
    params = parse.parse_qs(parsed_uri.query)
    # get the secret
    secret = params.get("secret", [None])[0]
    return secret


# will receive the secret of the url given to 'get_secret_from_uri'
# and will generate an otp code
def generate_otp_code(secret):
    totp = TOTP(secret)
    code = totp.now()
    return code


# Will copy the credential to the clipboard
# then wait 10 seconds and clear the clipboard
def copy_entry(credential_entry):
    copy(credential_entry)
    sleep(10)
    copy("")


if key_entry == 1:
    copy_entry(selected_entry.username)
if key_entry == 2:
    copy_entry(selected_entry.password)
if key_entry == 3:
    secret = get_secret_from_uri(selected_entry.otp)
    code = generate_otp_code(secret)
    copy_entry(code)
