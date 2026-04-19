---
name: sift-docker
description: Orchestrate forensic analysis using a SIFT workstation Docker container. Use this skill when you need to execute forensic tools (like fls, regfexport, md5sum) against mounted evidence, manage the container lifecycle, or map paths between the local host and the container environment.
---

# SIFT Docker Forensic Orchestration

This skill provides guidance and command templates for using the SIFT (SANS Investigative Forensic Toolkit) Docker container as the primary engine for artifact extraction and forensic tool execution.

## Core Concepts

- **Container ID**: Always stored in `scratch/container_id.txt`.
- **Evidence Mount**: Evidence is typically mounted at `/mnt/windows` inside the container.
- **Local to Container Mapping**: The project root is mapped to `/evidence` or similar in the container (verify with `docker inspect`).
- **Native Execution**: Prefer `docker exec` over Python wrappers for transparency and flexibility.

## Common Workflows

### 1. Executing Commands
Use the container ID from the scratch file to run tools:
```bash
docker exec $(cat scratch/container_id.txt) <command>
```

### 2. Registry Analysis
If `rip.pl` (RegRipper) fails, use `regfexport` to dump hive contents:
```bash
docker exec $(cat scratch/container_id.txt) regfexport /mnt/windows/Windows/System32/config/SOFTWARE
```

### 3. Calculating Hashes
Calculate hashes for suspicious files found in the evidence:
```bash
docker exec $(cat scratch/container_id.txt) md5sum /mnt/windows/path/to/file.exe
```

## Reference Material

- [Command Templates](references/commands.md): A library of common forensic commands.
- [Path Mappings](references/paths.md): Understanding where your files live in both worlds.

## Troubleshooting

- **Tool Not Found**: Some tools might be in `/usr/local/bin` or require full paths. Use `find /usr -name "*toolname*"` to locate them.
- **Perl Errors**: If a Perl script (like `rip.pl`) fails with syntax errors, it may be due to container environment issues. Fall back to simpler tools like `regfexport` or `strings`.
