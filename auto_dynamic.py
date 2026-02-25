from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time
import re

switch = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": "super.firstclues",
    "password": "09_0WEfeZ4n_",
    "port": 22,
    "timeout": 60,
    "conn_timeout": 30,
    "banner_timeout": 40,
}

vlans_to_create = {
    110: "User_Network",
    120: "ACCT_Network",
    130: "MGMT_Network",
    140: "IT_Network",
}

max_retries = 5
retry_delay = 10
ports_per_vlan = 2  # number of VLAN 1 ports to reclaim per VLAN

def get_vlan1_ports(connection):
    """Return list of ports currently assigned to VLAN 1 (default)"""
    vlan_output = connection.send_command("show vlan brief")
    vlan1_ports = []
    for line in vlan_output.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "1":  # VLAN 1
            ports_field = " ".join(parts[3:])
            vlan1_ports += [p.strip(",") for p in ports_field.split()]
    return vlan1_ports

for attempt in range(1, max_retries + 1):
    try:
        print(f"Attempt {attempt} connecting to switch...")
        connection = ConnectHandler(**switch)

        # 1️⃣ Create VLANs if missing
        vlan_output = connection.send_command("show vlan brief")
        existing_vlans = {int(line.split()[0]) for line in vlan_output.splitlines()
                          if line.strip() and line.split()[0].isdigit()}

        for vlan_id, vlan_name in vlans_to_create.items():
            if vlan_id not in existing_vlans:
                print(f"Creating VLAN {vlan_id} ({vlan_name})...")
                connection.send_config_set([f"vlan {vlan_id}", f"name {vlan_name}"])
                verify_output = connection.send_command(f"show vlan id {vlan_id}")
                if str(vlan_id) in verify_output:
                    print(f"✅ VLAN {vlan_id} successfully created.")
                else:
                    print(f"❌ VLAN {vlan_id} creation failed.")
            else:
                print(f"VLAN {vlan_id} already exists.")

        # 2️⃣ Get assignable ports from VLAN 1
        vlan1_ports = get_vlan1_ports(connection)
        print(f"\nAssignable ports from VLAN 1: {vlan1_ports}")

        # 3️⃣ Assign VLAN 1 ports to new VLANs and track assignments
        vlan_port_map = {}  # track assignments in real time
        for vlan_id in vlans_to_create:
            assigned_ports = vlan1_ports[:ports_per_vlan]
            vlan1_ports = vlan1_ports[ports_per_vlan:]
            vlan_port_map[vlan_id] = assigned_ports
            if not assigned_ports:
                print(f"No VLAN 1 ports left for VLAN {vlan_id}. Skipping assignment.")
                continue
            for port in assigned_ports:
                print(f"Assigning {port} to VLAN {vlan_id}...")
                commands = [
                    f"interface {port}",
                    f"switchport access vlan {vlan_id}",
                    "switchport mode access",
                    "no shutdown"
                ]
                connection.send_config_set(commands)
                port_output = connection.send_command(f"show running-config interface {port}")
                if f"switchport access vlan {vlan_id}" in port_output:
                    print(f"✅ {port} assigned to VLAN {vlan_id}.")
                else:
                    print(f"❌ Failed to assign {port} to VLAN {vlan_id}.")

        # 4️⃣ Display final summary table using tracked assignments
        print("\n=== VLAN Summary Table ===")
        print(f"{'VLAN ID':<8} {'Name':<20} {'Assigned Ports'}")
        print("-" * 50)
        for vlan_id, vlan_name in vlans_to_create.items():
            ports = vlan_port_map.get(vlan_id, [])
            ports_str = ", ".join(ports) if ports else "None"
            print(f"{vlan_id:<8} {vlan_name:<20} {ports_str}")

        connection.disconnect()
        break

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