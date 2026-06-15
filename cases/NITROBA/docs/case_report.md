> **🚨 CURRENT INVESTIGATIVE STATE:** Investigation completed. Case report finalized and attribution established.

# Case Report: NITROBA

## 1. Executive Summary
This investigation focuses on an incident of digital harassment at Nitroba State University (NSU). Lily Tuckrige, a Chemistry (CHEM109) teacher, has been receiving harassing emails at her personal email address (`lilytuckrige@yahoo.com`). 

Early indicators traced the email source to a Nitroba dorm room with IP address `140.247.62.34` (`G24.student.nitroba.org`), which is shared by three students: Alice, Barbara, and Candice. However, an open, passwordless Wi-Fi router installed in the room by Barbara's boyfriend Kenny allows anyone nearby to connect to the network. 

To identify the true sender, Nitroba's IT department captured network traffic in a packet capture file (`nitroba.pcap`). Through high-speed SQL triage and deep-dive packet inspection, the investigation successfully:
1. Mapped the dorm room network topology.
2. Isolated the harassing emails and traced them to the suspect IP `192.168.15.4`.
3. Identified the suspect's browser profile as an Internet Explorer 6 browser running on Windows XP, hosted on an Apple hardware device.
4. Uncovered a Google Calendar and Gmail session on the same suspect device and browser profile, revealing the personal email address `jcoachj@gmail.com`.
5. Correlated the email prefix `jcoachj` with the Chemistry 109 class list, positively identifying the attacker as student **Johnny Coach**.

## 2. Timeline of Events
| Timestamp (UTC) | MITRE Category | Event Details |
| --- | --- | --- |
| 2008-07-22 06:01:27 | Resource Development: T1585 | Attacker sends a secondary harassing message via `www.willselfdestruct.com` from IP `192.168.15.4` to `lilytuckrige@yahoo.com` with subject "you can't find us" and message "and you can't hide from us. Stop teaching. Start running." |
| 2008-07-22 06:02:57 | Initial Access: T1566 | Attacker sends a primary harassing email via `www.sendanonymousemail.net` (IP `69.80.225.91`) from IP `192.168.15.4` to `lilytuckrige@yahoo.com` with subject "Your class stinks" and message "Why do you persist in teaching a boring class? We don't like it. We don't like you." (TCP Stream 1631) |
| 2008-07-22 06:04:15 | Reconnaissance: T1589 | Attacker accesses Google Calendar and Gmail services using personal account `jcoachj@gmail.com` from the same IP `192.168.15.4` and browser User-Agent, establishing positive attribution to student Johnny Coach. |

## 3. Findings & Analysis

### A. Network Topology Mapping
Analysis of the packet capture `nitroba.pcap` reveals the following network layout:
- **Dorm Network Gateway & DNS Server**: `192.168.1.254`
- **Wi-Fi Router (WAN Interface)**: `192.168.1.64` (MAC: `00:1d:d9:2e:4f:61` - Cisco-Linksys)
- **Wi-Fi Router (LAN Interface)**: `192.168.15.1`
- **Suspect Device**: `192.168.15.4` (MAC: `00:17:f2:e2:c0:ce` - Apple)
  - **Browser User-Agent**: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (Internet Explorer 6 on Windows XP SP2)
  - **Forensic Note**: The MAC address belongs to an Apple computer, but the browser User-Agent is Windows XP. This indicates the attacker was running a Windows XP virtual machine in NAT mode, or dual-booting Windows XP via Boot Camp on an Apple Mac.

### B. Harassing Email Recovery
The harassing email was sent via the anonymous email service `www.sendanonymousemail.net` (IP `69.80.225.91`). The transaction was isolated in **TCP Stream 1631** at `2008-07-22 06:02:57 UTC`. The HTTP POST payload was recovered:
```http
POST /send.php HTTP/1.1
Host: www.sendanonymousemail.net
...
email=lilytuckrige@yahoo.com&sender=the_whole_world_is_watching@nitroba.org&subject=Your+class+stinks&message=Why+do+you+persist+in+teaching+a+boring+class%3F%0D%0A%0D%0AWe+don%27t+like+it.%0D%0A%0D%0AWe+don%27t+like+you.%0D%0A%0D%0A&security_code=xkpmkb&submit=+++SEND%21+++
```
A secondary harassing message was sent shortly before (at `06:01:27 UTC`) using `www.willselfdestruct.com` with the message: `"and you can't hide from us. Stop teaching. Start running."`

### C. Attribution & Identification
During the same browsing session, the device at `192.168.15.4` using the exact same User-Agent string made several requests to Google services:
1. **Google Calendar Session**: POST requests to `www.google.com/calendar/caldetails` and `www.google.com/calendar/load` contained a base64-encoded parameter: `amNvYWNoakBnbWFpbC5jb20=`.
   - **Decoded Value**: `jcoachj@gmail.com`
2. **Gmail Channel Binding**: A POST request to `mail.google.com/mail/channel/bind` contained the explicit query parameter: `req0_value=jcoachj%40gmail.com%2F475090`.

Cross-referencing the email prefix `jcoachj` with the Chemistry 109 student list:
- **Student Match**: **Johnny Coach** (email prefix `jcoachj`)
- **Conclusion**: **Johnny Coach** is the individual who sent the harassing messages.

## 4. Confirmed Exfiltrated/Accessed Data
- **Exfiltrated Data**: None.
- **Accessed Data**: No unauthorized access to NSU systems was detected. The incident was restricted to unauthorized harassing communications sent to the teacher's personal email.

## 5. MITRE ATT&CK Mapping
- **Resource Development: T1585 (Establish Accounts)**: The attacker utilized public anonymous email sending services (`www.sendanonymousemail.net` and `www.willselfdestruct.com`) to bypass standard email tracking.
- **Initial Access: T1566 (Phishing)**: Harassing messages were delivered via unauthenticated web-to-email services to the victim's inbox.
- **Reconnaissance: T1589 (Gather Victim Identity Information)**: The attacker gathered and targeted the personal email address of the teacher (`lilytuckrige@yahoo.com`).

## 6. Recommendations
1. **Implement Network Access Control (802.1X)**: Restrict dorm room Ethernet ports to authorized MAC addresses and block unauthorized routers/switches.
2. **Mandatory Wi-Fi Authentication**: Transition dorm networks to WPA3-Enterprise, ensuring that all network connections are bound to individual student authentication credentials.
3. **Disciplinary Action**: Refer student Johnny Coach to NSU's disciplinary board for violating the University's Acceptable Use Policy and digital harassment.

## 7. Evidence
- **Artifact**: `NITROBA-Scenario.pdf` (converted to text at `/scratch/NITROBA-Scenario.txt`)
  - **Description**: Case scenario document describing the harassment, suspects, and investigation guidelines.
  - **Discovery**: Found in `cases/NITROBA/docs/` and processed under Mission `001-mission-sniper-forensics-extract-scenario-pdf`.
- **Artifact**: `nitroba.pcap`
  - **Description**: Network packet capture of the dorm room network traffic.
  - **Metadata**: Size: 56,180,821 bytes, MD5: `9981827f11968773ff815e39f5458ec8`, SHA-256: `2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb`.
  - **Discovery**: Located in `cases/NITROBA/images/` and inventoried under Mission `002-mission-data-analyst-data-inventory`.
- **Artifact**: `packets.parquet`
  - **Description**: Parsed network packet capture metadata table in Parquet format.
  - **Discovery**: Created in `cases/NITROBA/scratch/nitroba.pcap/parquet/` and verified under Mission `003-mission-data-analyst-parse-pcap`.
- **Artifact**: `004-mission-data-analyst-analyze-traffic.md`
  - **Description**: Technical analysis mission card documenting the network mapping and attacker identification.
  - **Discovery**: Completed under Mission `004-mission-data-analyst-analyze-traffic`.
