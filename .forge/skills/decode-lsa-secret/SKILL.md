---
name: decode-lsa-secret
description: Decodes raw hex-encoded LSA secrets (like those extracted by pypykatz) into readable plaintext. Use this skill when you encounter a `raw_secret` hex string from Windows registry parsing and need to extract the underlying credentials, domains, or phone numbers.
---

# Decode LSA Secret

This skill provides a Python script to decode the UTF-16LE hex strings often found in Windows LSA Secrets (such as `RASDIALPARAMS` or `DefaultPassword`). 

When tools like `pypykatz` parse the registry, they output the decrypted LSA secret as a raw hex string of bytes. This script converts that hex back into readable text by decoding the UTF-16LE characters and splitting them by null terminators.

## Usage

To decode a hex string, run the bundled python script using the `sniper-forensics` or `data-analyst` agent (or via shell if available):

```bash
uv run python .forge/skills/decode-lsa-secret/scripts/decode.py <HEX_STRING>
```

### Example

If you have the hex string `3500340038003900...`:

```bash
uv run python .forge/skills/decode-lsa-secret/scripts/decode.py 350034003800390032003300360037003100000031003600300038000000330000000000000053004800490045004c00440042004100530045005c00660072006f0063006200610000004200690067002d0050007500720070006c0065002d0054007200750063006b0000000000300000000000
```

**Expected Output:**
```text
Decoded Parts:
[1] 548923671
[2] 1608
[3] 3
[4] SHIELDBASE\frocba
[5] Big-Purple-Truck
[6] 0
```
