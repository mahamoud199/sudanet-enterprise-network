"""
SudaNet Enterprise Network - Automated Threat Isolation Engine
Author: Mahmoud Mohamed Saeed (IT & Network Engineer / Cybersecurity Analyst)
Description:
    This script connects to the Cisco Edge Router via Netmiko upon receiving
    confirmed intrusion alerts (e.g. from Cowrie SSH Honeypot / Zabbix),
    and injects dynamic ACL deny statements to isolate the threat at the perimeter.
"""

import sys
import logging
from netmiko import ConnectHandler
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='threat_response.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Router connection parameters
EDGE_ROUTER = {
    'device_type': 'cisco_ios',
    'host': '192.168.254.1',
    'username': 'secadmin',
    'password': 'SecureRouterPassword123!',
    'secret': 'EnableSecretPassword123!',
    'port': 22,
    'session_timeout': 30
}

def isolate_threat(attacker_ip, router_info=EDGE_ROUTER):
    """
    Dynamically injects a deny rule for the attacking IP into EDGE_SECURITY_FILTER.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] [{timestamp}] Initiating automated containment for Attacker IP: {attacker_ip}")
    logging.info(f"Triggered automated isolation for threat IP: {attacker_ip}")

    # Access-list commands
    acl_commands = [
        'ip access-list extended EDGE_SECURITY_FILTER',
        f'remark [AUTOMATED-BLOCK] Added by Defense Engine on {timestamp}',
        f'1 deny ip host {attacker_ip} any log',
        'permit ip any any'
    ]

    try:
        print(f"[*] Connecting to Cisco Edge Router ({router_info['host']}) via Netmiko SSH...")
        with ConnectHandler(**router_info) as net_connect:
            net_connect.enable()
            print("[+] Successfully authenticated and entered privileged EXEC mode.")
            
            output = net_connect.send_config_set(acl_commands)
            print("[+] Applied dynamic ACL block rules:")
            print(output)
            
            # Save configuration
            net_connect.send_command('write memory')
            print("[+] Saved running-config to startup-config.")
            
            logging.info(f"Successfully blocked {attacker_ip} on {router_info['host']}")
            return True

    except Exception as e:
        error_msg = f"[-] Failed to isolate threat {attacker_ip}: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        return False

if __name__ == '__main__':
    target_ip = sys.argv[1] if len(sys.argv) > 1 else '198.51.100.44'
    isolate_threat(target_ip)
