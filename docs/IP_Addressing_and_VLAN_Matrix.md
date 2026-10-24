# SudaNet Enterprise IP Addressing & VLAN Design Plan
**Enterprise Network Architecture:** HQ (Kosti), Branch 1 (Khartoum NOC), Branch 2 (Port Sudan DR Site)

---

## 1. VLAN & Subnet Allocations (Subnets & Services)

| VLAN ID | VLAN Name | Network Subnet | Default Gateway (VIP) | Purpose & Connected Entities |
| :---: | :--- | :--- | :--- | :--- |
| **10** | `MGMT-VLAN` | `192.168.10.0/24` | `192.168.10.1` | Network device management (Switches, Routers, KVM, Out-of-band) |
| **20** | `STAFF-VLAN` | `192.168.20.0/24` | `192.168.20.1` | Corporate desktop users and general administrative staff workstations |
| **30** | `SERVER-VLAN` | `192.168.30.0/24` | `192.168.30.1` | Internal Enterprise Servers: Windows Server (AD DS `192.168.30.10`), Zabbix (`.20`), Automation (`.30`) |
| **50** | `DMZ-ZONE` | `192.168.50.0/24` | `192.168.50.1` | Demilitarized Zone: Web Server, Cowrie SSH Honeypot, Elasticsearch Telemetry |
| **70** | `NOC-USERS` | `192.168.70.0/24` | `192.168.70.98` | Branch 1 (Khartoum NOC) Network Operations Center engineers and monitors |
| **200** | `DR-SERVICES` | `192.168.200.0/24` | `192.168.200.1` | Branch 2 (Port Sudan DR Site) Disaster recovery hosts, replication targets |

---

## 2. Inter-Switch & WAN Point-to-Point Links (/30 Subnets)

| Link Name | Source Device & Interface | Destination Device & Interface | Subnet (/30) | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **P2P-CORE1-FW** | `Core-SW1 (Gi0/0)` | `pfSense (LAN opt1)` | `192.168.254.4/30` | Core routing to perimeter firewall |
| **P2P-CORE2-FW** | `Core-SW2 (Gi0/0)` | `pfSense (LAN opt2)` | `192.168.254.8/30` | Redundant core routing to firewall |
| **P2P-CORE-LINK** | `Core-SW1 (Gi0/1)` | `Core-SW2 (Gi0/1)` | `192.168.254.12/30` | Inter-Core OSPF & EtherChannel link |
| **P2P-CORE1-DIST1** | `Core-SW1 (Gi1/0)` | `Dist-SW1 (Gi0/1)` | `192.168.254.16/30` | Uplink from Core 1 to Distribution Switch 1 |
| **P2P-CORE2-DIST2** | `Core-SW2 (Gi1/0)` | `Dist-SW2 (Gi0/1)` | `192.168.254.20/30` | Uplink from Core 2 to Distribution Switch 2 |
| **WAN-HQ-ISP** | `Kosti-HQ Router (Gi0/2)` | `ISP Cloud Gateway` | `41.67.100.0/30` | Public WAN gateway peering via BGP |
| **WAN-KTR-ISP** | `KTR-Router (e0/1)` | `ISP Cloud Gateway` | `192.168.100.0/30` | Branch 1 WAN uplink |
| **WAN-PSD-ISP** | `PSD-Router (Gi0/1)` | `ISP Cloud Gateway` | `192.168.254.0/30` | Branch 2 Disaster Recovery WAN uplink |

---

## 3. Dynamic Routing Architecture
- **Internal Autonomous System:** OSPF Area 0 spanning all HQ Core and Distribution Switches and local routers.
- **External WAN Peering:** BGP peering between Enterprise Edge Routers and ISP Internet Cloud for multi-site failover and route propagation.
