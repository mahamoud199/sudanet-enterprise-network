"""
SudaNet Enterprise Network - Automated Fleet Configuration Backup
Author: Mahmoud Mohamed Saeed (IT & Network Engineer / Network Automation)
Description:
    Connects to all routers and switches in the SudaNet enterprise fleet,
    extracts running configurations, and saves them with timestamps.
"""

import os
from datetime import datetime
from netmiko import ConnectHandler

FLEET_DEVICES = [
    {'device_type': 'cisco_ios', 'host': '192.168.254.1', 'name': 'Kosti-HQ-R1'},
    {'device_type': 'cisco_ios', 'host': '192.168.254.13', 'name': 'Core-SW1'},
    {'device_type': 'cisco_ios', 'host': '192.168.254.14', 'name': 'Core-SW2'},
    {'device_type': 'cisco_ios', 'host': '192.168.254.29', 'name': 'Dist-SW1'},
    {'device_type': 'cisco_ios', 'host': '192.168.254.30', 'name': 'Dist-SW2'},
    {'device_type': 'cisco_ios', 'host': '192.168.70.98', 'name': 'KTR-Router'},
    {'device_type': 'cisco_ios', 'host': '192.168.200.1', 'name': 'PSD-Router'}
]

AUTH = {
    'username': 'admin',
    'password': 'CiscoAdminPassword123!',
    'secret': 'EnableSecret123!'
}

def backup_fleet(output_dir='../backups'):
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    for dev in FLEET_DEVICES:
        dev_conn = {**dev, **AUTH}
        dev_name = dev['name']
        print(f"[*] Starting backup for {dev_name} ({dev['host']})...")
        try:
            with ConnectHandler(**dev_conn) as net:
                net.enable()
                config = net.send_command('show running-config')
                file_name = f"{output_dir}/{dev_name}_{date_str}.cfg"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(config)
                print(f"[+] Successfully backed up {dev_name} to {file_name}")
        except Exception as e:
            print(f"[-] Failed to backup {dev_name}: {e}")

if __name__ == '__main__':
    backup_fleet()
