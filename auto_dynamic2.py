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
}

vlans_to_create = {
    110: "User_Network",
    120: "ACCT_Network",
    130: "MGMT_Network",
    140: "IT_Network",
}

max_retries = 3
retry_delay = 5
ports_per_vlan = 2  # Number of free ports to assign per VLAN

def get_free_ports(connection):
    """Return list of free/unassigned ports from 'show vlan brief' and interfaces"""
    vlan_output = connection.send_command("show vlan brief")
    assigned_ports = []
    for line in vlan_output.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            ports_field = " ".join(parts[3:])
            assigned_ports += [p.strip(",") for p in ports_field.split()]
    # Get all interfaces
    intf_output = connection.send_command("show ip interface brief")
    all_ports = [m.group(1) for line in intf_output.splitlines() if (m := re.match(r"(Gi\d+/\d+)", line))]
    free_ports = [p for p in all_ports if p not in assigned_ports]
    return free_ports

def get_vlan_ports(connection, vlan_id):
    """Return list of ports assigned to a VLAN"""
    output = connection.send_command(f"show vlan id {vlan_id}")
    ports = []
    for line in output.splitlines()[2:]:  # skip header lines
        parts = line.split()
        if parts and re.match(r"Gi\d+/\d+", parts[0]):
            ports.append(parts[0])
    return ports

for attempt in range(1, max_retries + 1):
    try:
        print(f"Attempt {attempt} connecting to switch...")
        connection = ConnectHandler(**switch)

        # 1️⃣ Get existing VLANs
        vlan_output = connection.send_command("show vlan brief")
        existing_vlans = {int(line.split()[0]) for line in vlan_output.splitlines()
                          if line.strip() and line.split()[0].isdigit()}

        # 2️⃣ Create VLANs if missing
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

        # 3️⃣ Discover free ports
        free_ports = get_free_ports(connection)
        print(f"\nDiscovered free ports: {free_ports}")

        # 4️⃣ Assign free ports dynamically
        vlan_port_map = {}
        for vlan_id in vlans_to_create:
            assigned_ports = free_ports[:ports_per_vlan]
            free_ports = free_ports[ports_per_vlan:]
            vlan_port_map[vlan_id] = assigned_ports
            if not assigned_ports:
                print(f"No free ports left for VLAN {vlan_id}. Skipping assignment.")
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

        # 5️⃣ Display final visual summary table
        print("\n=== VLAN Summary Table ===")
        print(f"{'VLAN ID':<8} {'Name':<20} {'Assigned Ports'}")
        print("-" * 50)
        for vlan_id, vlan_name in vlans_to_create.items():
            ports = get_vlan_ports(connection, vlan_id)
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