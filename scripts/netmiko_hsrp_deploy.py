"""
SudaNet Enterprise Network - HSRP High Availability Deployment
Author: Mahmoud Mohamed Saeed (IT & Network Engineer / Network Automation)
Description:
    Automates the deployment of Hot Standby Router Protocol (HSRP) across
    Core Switches (Core-SW1 and Core-SW2) with priority, preemption, and timers.
"""

from netmiko import ConnectHandler

core_switches = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.254.13', # Core-SW1 (Active)
        'username': 'admin',
        'password': 'CiscoAdminPassword123!',
        'secret': 'EnableSecret123!',
        'hsrp_priority': 110
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.254.14', # Core-SW2 (Standby)
        'username': 'admin',
        'password': 'CiscoAdminPassword123!',
        'secret': 'EnableSecret123!',
        'hsrp_priority': 100
    }
]

vlans_to_configure = [
    {'vlan_id': 10, 'vip': '192.168.10.1', 'name': 'MGMT-VLAN'},
    {'vlan_id': 20, 'vip': '192.168.20.1', 'name': 'STAFF-VLAN'},
    {'vlan_id': 30, 'vip': '192.168.30.1', 'name': 'SERVER-VLAN'},
    {'vlan_id': 50, 'vip': '192.168.50.1', 'name': 'DMZ-VLAN'}
]

def deploy_hsrp():
    for dev in core_switches:
        print(f"[*] Connecting to {dev['host']} to deploy HSRP...")
        try:
            with ConnectHandler(**dev) as net:
                net.enable()
                config_commands = []
                for vlan in vlans_to_configure:
                    group = vlan['vlan_id']
                    config_commands.extend([
                        f"interface Vlan{group}",
                        f" standby {group} ip {vlan['vip']}",
                        f" standby {group} priority {dev['hsrp_priority']}",
                        f" standby {group} preempt",
                        f" standby {group} timers 1 3"
                    ])
                
                output = net.send_config_set(config_commands)
                print(f"[+] HSRP Configured on {dev['host']}:\n{output}")
                net.send_command('write memory')
        except Exception as e:
            print(f"[-] Error on {dev['host']}: {e}")

if __name__ == '__main__':
    deploy_hsrp()
