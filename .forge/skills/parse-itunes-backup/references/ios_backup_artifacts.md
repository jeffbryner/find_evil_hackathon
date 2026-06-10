# iOS Backup Artifacts Reference

This reference lists the most common and valuable forensic databases, file paths, and table structures found within unpacked iOS iTunes backups.

---

## 1. System Communication Databases

### A. SMS / iMessage
- **Path**: `HomeDomain/Library/SMS/sms.db`
- **Description**: Stores all sent and received SMS and iMessage conversations.
- **Key Tables**:
  - `message`: Stores the message text (`text`), timestamps (`date` - Cocoa absolute time), sender/recipient ID (`handle_id`), and status.
  - `handle`: Maps `handle_id` to actual phone numbers or email addresses (`id`).
  - `chat`: Represents conversations.
  - `chat_message_join`: Joins `chat` and `message`.
  - `attachment`: Stores metadata for message attachments (photos, videos).
  - `message_attachment_join`: Joins `message` and `attachment`.

### B. Call History
- **Path**: `WirelessDomain/Library/CallHistory/call_history.db`
- **Description**: Stores call history (incoming, outgoing, missed, FaceTime).
- **Key Tables**:
  - `call`: Contains phone number/address (`address`), duration (`duration` in seconds), timestamp (`date` - Unix epoch or Cocoa epoch depending on iOS version), and whether it was answered (`answered`).

### C. Contacts / Address Book
- **Path**: `HomeDomain/Library/AddressBook/AddressBook.sqlitedb`
- **Description**: Stores contacts list.
- **Key Tables**:
  - `ABPerson`: Contains contact names.
  - `ABMultiValue`: Contains phone numbers and emails associated with the contact.

---

## 2. Browser & Web Activity

### A. Safari History
- **Path**: `HomeDomain/Library/Safari/History.db`
- **Description**: Stores web browsing history.
- **Key Tables**:
  - `history_visits`: Timestamps and visit details.
  - `history_items`: URL strings.

### B. Safari Bookmarks
- **Path**: `HomeDomain/Library/Safari/Bookmarks.db`
- **Description**: Stores bookmarks and reading list.

---

## 3. Productivity & Messaging Apps

### A. Apple Notes
- **Path**: `AppDomainGroup-group.com.apple.notes/NoteStore.sqlite`
- **Description**: Stores Apple Notes.
- **Key Tables**:
  - `ZICCLOUDSYNCINGOBJECT`: Contains note titles (`ZTITLE`), snippets (`ZSNIPPET`), creation dates (`ZCREATIONDATE`), and modification dates (`ZMODIFICATIONDATE`).
  - `ZICNOTEDATA`: Contains compressed/serialized note body content.

### B. WhatsApp
- **Path**: `AppDomain-net.whatsapp.WhatsApp/Documents/ChatStorage.sqlite`
- **Description**: Stores WhatsApp chat messages.
- **Key Tables**:
  - `ZWAMESSAGE`: Contains message text (`ZTEXT`), status, and timestamps.
  - `ZWACHATSESSION`: Contains chat session metadata.

### C. Skype
- **Path**: `AppDomain-com.skype.skype/Documents/main.db`
- **Description**: Stores Skype chat history and contacts.
- **Key Tables**:
  - `Messages`: Skype chat messages.
  - `Conversations`: Chat session metadata.

### D. Google Voice
- **Path**: `AppDomain-com.google.GVDialer/Documents/recents.db`
- **Description**: Stores Google Voice call and message recents.
- **Key Tables**:
  - `Recents`: Timestamps, phone numbers, names, and labels.

### E. Twitter / Tweetie
- **Drafts Folder**: `AppDomain-com.atebits.Tweetie2/Documents/com.atebits.tweetie.application-important-state/Dr_AVanko-476464110.drafts/`
- **Attachments Folder**: `AppDomain-com.atebits.Tweetie2/Documents/com.atebits.tweetie.compose.attachments/`
- **Description**: Stores draft tweets and their media attachments before they are posted.
- **Format**: Draft files (e.g., `composition.2`) are Binary Plists containing text, timestamps, and UUIDs linking to attachment images in the attachments folder.
