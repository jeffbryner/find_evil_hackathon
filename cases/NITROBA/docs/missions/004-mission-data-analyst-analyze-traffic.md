# Mission: Analyze Network Traffic and Identify Attacker
**Target Agent:** data-analyst

## Purpose
The purpose of this mission is to analyze the parsed network traffic in `packets.parquet` and the raw `nitroba.pcap` to map the dorm room network, locate the harassing email sent to `lilytuckrige@yahoo.com`, identify the attacker's browser profile, and find identifying information in other connections from the same attacker to identify them from the CHEM109 class list.

## Background
We have parsed `nitroba.pcap` into `packets.parquet`. Now we must use the Hybrid Funnel approach (SQL queries followed by deep-dive tshark payload inspections) to trace the harassing email back to its source and identify the student responsible.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If no network traffic or packets containing `lilytuckrige@yahoo.com` or related headers are found after 5 distinct queries, stop and report.

## Task Checklist
- [x] Profile the active IP addresses in `packets.parquet` to map the dorm room network topology
- [x] Search `packets.parquet` for any packets containing the keyword `lilytuckrige` or `yahoo` or SMTP/HTTP/Webmail traffic
- [x] Locate the exact TCP stream ID(s) associated with the harassing email
- [x] Reassemble and inspect the payload of the harassing email stream using `tshark` inside the container
- [x] Extract the exact User-Agent string and browser characteristics of the sender
- [x] Identify other TCP streams and connections originating from the same IP address and using the same User-Agent string
- [x] Search those other streams for login credentials, usernames, email addresses, or form submissions that reveal the identity of the sender
- [x] Match the discovered identity against the Chemistry 109 class list
- [x] Update this mission card with the findings, including the attacker's IP, MAC/host info, User-Agent, identified student name, and the smoking-gun evidence (e.g., login credentials or session details)
- [x] Write a chronological technical log of 100% of executed queries and commands to the `004-mission-data-analyst-analyze-traffic-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
### 1. Dorm Room Network Topology
- **Local Network Gateway / DNS Server:** `192.168.1.254`
- **Wi-Fi Router WAN IP:** `192.168.1.64` (MAC: `00:1d:d9:2e:4f:61` - Cisco-Linksys)
- **Wi-Fi Router LAN IP:** `192.168.15.1`
- **Suspect Physical Device:** `192.168.15.4` (MAC: `00:17:f2:e2:c0:ce` - Apple Computer)
  - **Browser User-Agent:** `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (Internet Explorer 6 on Windows XP)
  - **Analysis:** The MAC address vendor is Apple, but the browser User-Agent is Windows XP. This indicates the suspect is running a Windows XP virtual machine (in NAT mode) or dual-booting on an Apple Mac computer.

### 2. Harassing Email Identification
- **Service Used:** `www.sendanonymousemail.net` (IP: `69.80.225.91`)
- **TCP Stream ID:** `1631`
- **Timestamp:** `2008-07-22T06:02:57.548149+00:00`
- **Sender IP:** `192.168.15.4`
- **Email Details:**
  - **Recipient:** `lilytuckrige@yahoo.com`
  - **Sender:** `the_whole_world_is_watching@nitroba.org`
  - **Subject:** `Your class stinks`
  - **Message:** `Why do you persist in teaching a boring class? We don't like it. We don't like you.`

- **Second Harassing Message:**
  - **Service Used:** `www.willselfdestruct.com`
  - **Timestamp:** `2008-07-22T06:01:27`
  - **Recipient:** `lilytuckrige@yahoo.com`
  - **Subject:** `you can't find us`
  - **Message:** `and you can't hide from us. Stop teaching. Start running.`

### 3. Attacker Identification & Smoking-Gun Evidence
- **Identified Account:** `jcoachj@gmail.com`
  - **Evidence:** The suspect IP `192.168.15.4` logged into Google Calendar and Gmail during the same timeframe. The POST requests to `www.google.com/calendar/caldetails` and `www.google.com/calendar/load` contained the base64-encoded string `amNvYWNoakBnbWFpbC5jb20=`, which decodes to `jcoachj@gmail.com`.
  - **Gmail Session Detail:** A POST request to `mail.google.com/mail/channel/bind` contained `req0_value=jcoachj%40gmail.com%2F475090`.
- **Chemistry 109 Class List Correlation:**
  - The student with username `jcoachj` is **Johnny Coach**.
  - **Conclusion:** **Johnny Coach** is the sender of the harassing emails.

## Discovered Leads (For Followup)
- None. The case is fully resolved.
