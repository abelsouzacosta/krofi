from rofi import Rofi
from os import getenv
from pykeepass import PyKeePass
from subprocess import run

rofi_instance = Rofi()

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

group_options = []
for group in groups:
    group_options.append(group.name)

index_group, key_group = rofi_instance.select("Groups", options=group_options)
# get all entries from the group

entries_options = []
for entry in groups[index_group].entries:
    entries_options.append(entry.title)

index_entry, key_entry = rofi_instance.select(
    f"Entries at {groups[index_group]}", options=entries_options
)

print(f"index entry: {index_entry}, key_entry: {key_entry}")
# get a specific entry from the database
