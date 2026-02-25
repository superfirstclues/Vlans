from netmiko import ConnectHandler

switch = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": "super.firstclues",
    "password": "09_0WEfeZ4n_",
    "port": 22,
}

vlans = [
    "vlan 110",
    "name User_Network",
    "vlan 120",
    "name ACCT_Network",
    "vlan 130",
    "name MGMT_Network",
    "vlan 140",
    "name IT_Network",
]

# Assign a test port to IT_Network
port_assignment = [
    "interface GigabitEthernet1/0/9",
    "switchport mode access",
    "switchport access vlan 140",
    "description IT_NETWORK_ACCESS_PORT"
]

connection = ConnectHandler(**switch)

print("\n========== PUSHING VLAN CONFIGURATION ==========")
print(connection.send_config_set(vlans))

print("\n========== ASSIGNING PORT TO IT NETWORK ==========")
print(connection.send_config_set(port_assignment))

connection.save_config()

print("\n========== VLAN TABLE VERIFICATION ==========")

vlan_output = connection.send_command("show vlan brief")

# Filter out legacy VLANs
filtered_lines = []
for line in vlan_output.splitlines():
    if not line.strip().startswith(("1002", "1003", "1004", "1005")):
        filtered_lines.append(line)

print("\n".join(filtered_lines))

connection.disconnect()

print("\nVLAN deployment, port assignment, and verification completed.")