import glob
import re
import os

def natural_key(filename):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', filename)]

# Load files
files = glob.glob("server_dump/*.txt")
files.sort(key=natural_key)

print(f"Found {len(files)} files")

# Dictionary to store which files contain which keyword
found = {
    "OKAY": [],
    "ERROR": [],
    "WARN": []
}

# Scan all files once
for f in files:
    try:
        with open(f, "r", errors="ignore") as file:
            content = file.read()

            if "OKAY" in content:
                found["OKAY"].append(f)

            if "ERROR" in content:
                found["ERROR"].append(f)

            if "WARN" in content:
                found["WARN"].append(f)

    except Exception as e:
        print(f"Could not read {f}: {e}")

# --- MENU ---
print("\nMENU")
print("1 - OKAY")
print("2 - ERROR")
print("3 - WARN")

choice = input("Choose an option: ")

if choice == "1":
    key = "OKAY"
elif choice == "2":
    key = "ERROR"
elif choice == "3":
    key = "WARN"
else:
    print("Invalid choice")
    exit()

print(f"\nFiles containing {key}:\n")

for f in found[key]:
    # Extract just the number from filename
    num = re.findall(r'\d+', f)
    if num:
        print(f"File {num[-1]} has a {key}")
    else:
        print(f"{f} has a {key}")
