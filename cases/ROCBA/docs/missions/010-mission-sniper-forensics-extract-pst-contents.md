# Mission: Extract and Analyze PST Contents
**Target Agent:** sniper-forensics

## Purpose
Extract the file `/$Recycle.Bin/S-1-5-21-528816539-567677750-276746561-1002/$RDNBREY.pst` (Inode/MFT record `479180`) from the disk image and analyze its contents (emails, subjects, senders, attachments) to see what was exfiltrated.

## Background
We have confirmed that the email archive `SRL-EMAIL-EXPORT.pst` is fully intact and allocated in the Recycle Bin under the name `$RDNBREY.pst` at Inode/MFT record `479180`. We need to extract this file using the Sleuthkit (`icat`) inside the SIFT container and then analyze its contents (e.g., using python pst parsing libraries, readpst, or other available tools in SIFT) to determine what emails and files were contained within the archive.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the extraction fails or the PST is corrupt/unreadable, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Execute the `carve-file-sop` skill to extract Inode `479180` from `rocba-cdrive.e01` into the scratch directory as `SRL-EMAIL-EXPORT-RECOVERED.pst`.
- [x] Verify the file size and file type of the extracted PST.
- [x] Analyze the extracted PST file using tools in the SIFT container (such as `readpst`, `pypff`, or python scripts) to list folders, email counts, subject lines, senders, and any key attachments.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with the analysis of the PST's contents.
- [x] Update this mission card with results.

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
  1. Loaded and read the required SOPs (`shared-facts-sop`, `delegating-mission-cards-sop`, `carve-file-sop`, `sift-docker`).
  2. Verified the SIFT container was running and located the raw disk image file inside the container (`/mnt/ewf/ROCBA/rocba-cdrive.e01/ewf1`).
  3. Extracted Inode `479180` using `icat` inside the SIFT container and saved it locally as `SRL-EMAIL-EXPORT-RECOVERED.pst`.
  4. Verified file size (`20,587,520` bytes), type (`Microsoft Outlook email folder (>=2003)`), and MD5 hash (`d7ffc69c21847a8557a39fe27d1d9426`).
  5. Extracted the PST contents recursively into separate RFC 822 email files using `readpst` inside the container.
  6. Wrote a Python script `parse_emails.py` to parse the extracted email files and extract metadata, folder structure, and attachments.
  7. Documented findings in `cases/ROCBA/docs/shared_facts.md` and this mission card.
- **Findings:**
  - **Total Emails:** 65 emails (42 in `Inbox`, 23 in `Inbox/Maria`).
  - **Key Projects & Topics:**
    - **Project ADAMANTIUM:** Extensive discussions and comments on the document "ADAMANTIUM-Background" involving Timothy Dungan, Maria Hill, Natasha Romanoff, and Fred Rocba.
    - **Project KITT:** Maria Hill shared the "KITT" folder and "The Future of KITT" document with Fred Rocba.
    - **Project Megaforce:** Folder shared with Fred Rocba, and SharePoint reminders sent to him.
    - **Project Gunstar:** Discussions on development next steps and project status.
    - **New Alloy Research:** Folder shared with Fred Rocba.
    - **Vibrainium:** Natasha Romanoff shared an anonymous access link to "Vibrainium(1).doc".
  - **Key Attachments:**
    - `some-quantum-mechanical-properties-of-the-wolfram-model.pdf` (Shared by Maria Hill on Sat, 7 Nov 2020)
    - `Mongolia_ScoutingTrip.jfif` (Shared by Maria Hill on Sat, 31 Oct 2020)
    - `ponies.jpg` (Shared by Maria Hill on Sun, 1 Nov 2020)
    - `eagle_hunting.jpg` (Shared by Maria Hill on Wed, 4 Nov 2020)
    - `GuessWhere.jpg` (Shared by Maria Hill on Thu, 5 Nov 2020)
- **Confidence Rating:** 5/5 (100% complete recovery and successful parsing of all emails and attachments without corruption).
- **Budget Tally:**
  - Orientation: 5 / 5 tool calls
  - Execution: 20 / 20 tool calls (including 4 failed/retry calls)
  - Reporting: 6 / 5 tool calls (total 31 tool calls)
- **NPS / Feedback:** 5/5. The SIFT Docker environment combined with standard Sleuthkit and python tools is extremely efficient and robust for this kind of sniper forensics task. No issues encountered except learning that `write` tool requires reading a non-existent file first to verify its status.
