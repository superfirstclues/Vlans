from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time

switch = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": "super.firstclues",
    "password": "09_0WEfeZ4n_",
    "port": 22,
    "timeout": 60,
}

vlans_to_create = {
    110: "User_Network",
    120: "ACCT_Network",
    130: "MGMT_Network",
    140: "IT_Network",
}

max_retries = 3
retry_delay = 5

for attempt in range(1, max_retries + 1):
    try:
        print(f"Attempt {attempt} connecting to switch...")
        connection = ConnectHandler(**switch)

        # 1️⃣ Get existing VLANs
        output = connection.send_command("show vlan brief")
        existing_vlans = {int(line.split()[0]) for line in output.splitlines()
                          if line.strip() and line.split()[0].isdigit()}

        # 2️⃣ Create VLANs that don’t exist
        for vlan_id, vlan_name in vlans_to_create.items():
            if vlan_id not in existing_vlans:
                print(f"Creating VLAN {vlan_id} ({vlan_name})...")
                commands = [
                    f"vlan {vlan_id}",
                    f"name {vlan_name}"
                ]
                connection.send_config_set(commands)
            else:
                print(f"VLAN {vlan_id} already exists.")

        # 3️⃣ Show VLANs again and print only 110–140
        output = connection.send_command("show vlan brief")
        print("\n--- VLANs 110–140 ---")
        for line in output.splitlines():
            if line.strip() and line.split()[0].isdigit():
                vlan_id = int(line.split()[0])
                if 110 <= vlan_id <= 140:
                    print(line)

        connection.disconnect()
        break  # success, exit retry loop

    except (NetmikoTimeoutException, SSHException) as e:
        print(f"Connection failed: {e}")
        if attempt < max_retries:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Could not connect.")
            break

    except NetmikoAuthenticationException:
        print("Authentication failed.")
        break