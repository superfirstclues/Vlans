from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

switch = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": "super.firstclues",
    "password": "09_0WEfeZ4n_",
    "port": 22,
    "timeout": 20,
}

try:
    connection = ConnectHandler(**switch)
    output = connection.send_command("show vlan brief")
    print(output)
    connection.disconnect()

except NetmikoTimeoutException:
    print("Connection timed out.")

except NetmikoAuthenticationException:
    print("Authentication failed.")