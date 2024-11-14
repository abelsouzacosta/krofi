from rofi import Rofi
from os import getenv
from pykeepass import PyKeePass
from subprocess import run
from pyperclip import copy
from time import sleep

rofi_instance = Rofi()


# Will copy the credential to the clipboard
# then wait 10 seconds and clear the clipboard
def copy_entry(credential_entry):
    copy(credential_entry)
    sleep(10)
    copy("")


# command to run in subprocess
command = ["rofi", "-dmenu", "-p", "Enter database password: ", "-password"]

# ask for credentials
credential = run(command, capture_output=True, text=True).stdout.strip()
if not credential:
    rofi_instance.exit_with_error("Please provide valid credentials")

print(f"{credential}")
# get the database through a environment variable
database_path = getenv("KPDB")
print(f"{database_path}")
# open database and validate credentials
try:
    keepass_database = PyKeePass(database_path, password=credential)
except Exception:
    rofi_instance.exit_with_error("Was not possible to open the database")

# get all groups from the database
groups = keepass_database.groups

group_options = [group.name for group in groups]

index_group, key_group = rofi_instance.select("Groups", options=group_options)

# get the selected group in the previous step
selected_group = groups[index_group]
# get all entries from the group
entries_options = [entry.title for entry in selected_group.entries]

index_entry, key_entry = rofi_instance.select(
    f"Entries at {groups[index_group]}",
    options=entries_options,
    key1=("Alt+u", "Copy username"),
    key2=("Alt+p", "Copy password"),
)

selected_entry = selected_group.entries[index_entry]
print(f"index entry: {index_entry}, key_entry: {key_entry}")

if key_entry == 1:
    copy_entry(selected_entry.username)
if key_entry == 2:
    copy_entry(selected_entry.password)
