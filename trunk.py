from netmiko import ConnectHandler

switch = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": "super.firstclues",
    "password": "09_0WEfeZ4n_",
    "port": 22,
}

connection = ConnectHandler(**switch)

trunk_commands = [
    "interface GigabitEthernet1/0/10",
    "switchport mode trunk",
    "switchport trunk allowed vlan 110,120,130,140",
    "description AUTOMATED_TRUNK_PORT"
]

output = connection.send_config_set(trunk_commands)
print(output)

connection.save_config()
connection.disconnect()

print("Trunk configuration completed.")