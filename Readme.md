## Home Of Some Proxmox Tools I Use

[TOC]

### new-snapshots.py

This tool is designed to automate the process of creating snapshots for multiple Virtual Machines (VMs) on a Proxmox server. It uses the Proxmox API to interact with the server and create snapshots for selected VMs.

**Features:**

1. **Multi-Node Support**: The tool can scan multiple nodes on the Proxmox server, allowing you to create snapshots across multiple machines.
2. **VM Selection**: You can select which VMs to snapshot by interacting with a checkbox list dialog.
3. **Automatic Snapshot Naming**: The tool generates unique names for each snapshot using a random ID.

**Usage:**

1. Set environment variables `PROXMOX_SERVER`, `PROXMOX_USER`, `PROXMOX_REALM`, `PROXMOX_TOKEN_NAME`, and `PROXMOX_TOKEN_VALUE` with your Proxmox server credentials.
2. Run the script, which will scan the nodes on the Proxmox server for VMs.
3. Select which VMs to snapshot using the checkbox list dialog.
4. The tool will create snapshots for the selected VMs.

**Requirements:**

* Python 3
* `proxmoxer` library (installable via pip)
* `rich` library (installable via pip)
* `prompt_toolkit` library (installable via pip)

**Note:** This tool assumes that you have already set up your Proxmox server and have the necessary credentials to access it.

### new-snapshots.py

**Proxmox Snapshot Remover Tool**

The Proxmox Snapshot Remover Tool is a powerful and intuitive command-line utility that helps administrators manage snapshots on their Proxmox virtual environments. This tool allows users to scan for snapshots across multiple nodes, select which ones to delete, and execute the deletion process with ease.

**Key Features:**

1. **Snapshot Scanning:** The tool scans for snapshots across all Proxmox nodes in your infrastructure, providing a comprehensive list of available snapshots.
2. **Selective Deletion:** Users can select specific snapshots to delete using space bar selection, ensuring that only intended snapshots are removed.
3. **Progress Tracking:** The tool provides real-time progress tracking during the deletion process, allowing users to monitor the status of each task.
4. **Error Handling:** The tool is designed to handle errors and exceptions gracefully, ensuring that the deletion process continues even in case of unexpected issues.

**Prerequisites:**

1. **Proxmox Environment:** The tool assumes a Proxmox virtual environment with access to API credentials (server, user, realm, token name, and token value).
2. **Python 3.x:** The tool is written in Python 3.x and requires this version installed on the system.

**How to Use:**

1. Set up your Proxmox API credentials as environment variables (PROXMOX_SERVER, PROXMOX_USER, PROXMOX_REALM, PROXMOX_TOKEN_NAME, and PROXMOX_TOKEN_VALUE).
2. Run the tool using Python 3.x.
3. The tool will scan for snapshots across all nodes, displaying a list of available snapshots.
4. Select specific snapshots to delete using space bar selection.
5. Confirm the deletion process by running the tool again.
