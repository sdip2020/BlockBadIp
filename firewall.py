import requests
import csv
import subprocess

# Fetch the CSV data
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

# Parse the CSV data
mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.splitlines()))

# Iterate over the rows in the CSV
for row in mycsv:
    ip = row[1]
    if ip != "dst_ip":
        print("Added Rule to block:", ip)
        
        # Delete existing firewall rule
        rule = f"netsh advfirewall firewall delete rule name='BadIP' remoteip={ip}"
        subprocess.run(["Powershell", "-Command", rule])
        
        # Add outbound firewall rule
        rule = f"netsh advfirewall firewall add rule name='BadIP' dir=out action=block remoteip={ip}"
        subprocess.run(["Powershell", "-Command", rule])
        
        # Add inbound firewall rule
        rule = f"netsh advfirewall firewall add rule name='BadIP' dir=in action=block remoteip={ip}"
        subprocess.run(["Powershell", "-Command", rule])
