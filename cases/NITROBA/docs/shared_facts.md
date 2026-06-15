# Data Inventory
- **File Path**: `cases/NITROBA/docs/NITROBA-Scenario.pdf`
  - **Type**: Case Scenario PDF (converted to text at `/scratch/NITROBA-Scenario.txt`)
  - **Description**: Contains case background, student class list, and objectives.
- **File Path**: `cases/NITROBA/images/nitroba.pcap`
  - **Type**: Network Packet Capture
  - **Description**: Captured network traffic from the Nitroba dorm room network to identify the harassment email sender.
  - **Size**: 56,180,821 bytes
  - **MD5**: `9981827f11968773ff815e39f5458ec8`
  - **SHA-256**: `2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb`
  - **Container Path**: `/case/images/nitroba.pcap`
  - **Status**: Verified & Accessible inside the SIFT container

# Compromised Accounts
- **Account**: `lilytuckrige@yahoo.com` (Target of harassment emails)
- **Account**: `jcoachj@gmail.com` (Gmail/Google Calendar account of Johnny Coach, used on suspect machine `192.168.15.4`)

# Known Malicious IPs & Domains
- **IP**: `140.247.62.34` (`G24.student.nitroba.org`) - Dorm room IP address (source of harassing emails).
- **IP**: `192.168.15.4` (Suspect Apple Mac machine running Windows XP virtual machine, MAC: `00:17:f2:e2:c0:ce`)
- **IP**: `192.168.1.64` (Cisco-Linksys Wi-Fi router WAN IP, MAC: `00:1d:d9:2e:4f:61`)
- **IP**: `192.168.15.1` (Cisco-Linksys Wi-Fi router LAN IP)
- **Domain**: `www.sendanonymousemail.net` (Used to send harassing email)
- **Domain**: `www.willselfdestruct.com` (Used to send secondary harassing message)

# Suspicious Files & Staging Directories

# Decoded Payloads & Scripts
- **Harassing Email (TCP Stream 1631 via www.sendanonymousemail.net)**:
  - **Recipient**: `lilytuckrige@yahoo.com`
  - **Sender**: `the_whole_world_is_watching@nitroba.org`
  - **Subject**: `Your class stinks`
  - **Message**: `Why do you persist in teaching a boring class? We don't like it. We don't like you.`
- **Secondary Harassing Message (via www.willselfdestruct.com)**:
  - **Recipient**: `lilytuckrige@yahoo.com`
  - **Subject**: `you can't find us`
  - **Message**: `and you can't hide from us. Stop teaching. Start running.`

# Confirmed Exfiltrated/Accessed Data

# Pending Investigative Leads

# Known Forensic Artifacts (IGNORE)
