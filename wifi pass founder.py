import subprocess as sp
import time
import re
from datetime import datetime
import os

# Function to get Wi-Fi profiles and passwords
def get_wifi_profiles():
    output = sp.getoutput('netsh wlan show profiles name=*')
    wifi_name_list = []
    for name_index in [m.start() for m in re.finditer('Name', output)]:
        wifi_name_list.append(output[name_index:name_index+output[name_index:].find('Control options')].split(':')[1].strip())

    passwords = []
    for name in wifi_name_list:
        output = sp.getoutput(f'netsh wlan show profile name="{name}" key=clear')
        output = output[output.find('Key Content'):output.find('Cost settings')]
        output = output[output.find(':')+2:]
        output = output.strip()
        passwords.append((name, output))
    return passwords

# Function to print the table
def print_table(data):
    # Print the table header
    print("{:<30} | {:<}".format("Wi-Fi Name", "Password"))
    print("-" * 60)
    
    # Print the Wi-Fi names and passwords in a tabular format
    for name, password in data:
        print("{:<30} | {:<}".format(name, password))

# Function to save the table to a file
def save_table_to_file(data, filepath):
    with open(filepath, 'w') as file:
        file.write("{:<30} | {:<}\n".format("Wi-Fi Name", "Password"))
        file.write("-" * 60 + "\n")
        for name, password in data:
            file.write("{:<30} | {:<}\n".format(name, password))

# Main script execution
passwords = get_wifi_profiles()
print_table(passwords)

# Ask user if they want to save the passwords
save_passwords = input("Do you want to save the passwords? (yes/no): ").strip().lower()

if save_passwords == 'yes':
    # Create the folder if it doesn't exist
    folder = "wifi_pass"
    os.makedirs(folder, exist_ok=True)
    
    # Create filename with current date and time, using commas for clarity
    now = datetime.now()
    filename = now.strftime("wifi_passwords_%Y-%m-%d_%H,%M,%S.txt")
    filepath = os.path.join(folder, filename)
    
    # Save passwords to the file
    save_table_to_file(passwords, filepath)
    
    print(f"Passwords have been saved to {filepath}")
    time.sleep(3)  # Wait for 3 seconds before closing the window
    os._exit(0)  # Close the script
else:
    print("Passwords have not been saved.")
    time.sleep(10)  # Wait for 10 seconds before closing the windowy