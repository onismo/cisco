from getpass import getpass
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
import time

start_time = time.time()

username = input('Enter Username: ')
password = getpass("Enter Password: ")
secret = password

results = ''

with open('commands_list.txt') as f:
    commands_list = list(line for line in (l.strip() for l in f) if line)

with open('devices_list.txt') as f:
    devices_list = list(line for line in (l.strip() for l in f) if line)

for device in devices_list:
    print('Connecting to device: ' + device)

    device_ssh = {
        'device_type': 'cisco_ios',
        'ip': device,
        'username': username,
        'password': password,
        'secret' : secret,
    }
    device_telnet = {
        'device_type': 'cisco_ios_telnet',
        'ip': device,
        'username': username,
        'password': password,
        'secret' : secret,
    }

    try:
        net_connect = ConnectHandler(**device_ssh)
        net_connect.enable()
    except SSHException:
        try:
            net_connect = ConnectHandler(**device_telnet)
            net_connect.enable()
        except Exception as error:
            print('Encountered error:', error)
            continue

    for show_command in commands_list:
        try:
            results += f'\n{device}#{show_command}\n'
            results += net_connect.send_command(show_command)
        except:
            print(f'Error with {device} for command: {show_command} ')
            continue
    
    # results += net_connect.send_config_set(commands_list) # configure terminal commands
    
timestamp = time.strftime("%Y%m%d-%H%M")
with open(f'backup_{timestamp}', 'w') as f:
    f.write(results)

print(f'Completed in {round(time.time() - start_time)} seconds. See backup_{timestamp}.txt')