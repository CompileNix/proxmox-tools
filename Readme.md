## Home Of Some Proxmox Tools I Use

[TOC]

### new-snapshots.py

**Proxmox Snapshot Creator**

The Proxmox Snapshot Creator is a Python script designed to automate the process of creating snapshots for virtual machines (VMs) on a Proxmox server. The script uses the `proxmoxer` library to interact with the Proxmox API and creates snapshots for selected VMs.

**Features:**

* Automatically scans all nodes in the Proxmox cluster and lists all VMs
* Allows user to select which VMs to create snapshots for using a checkbox dialog
* Creates unique snapshot names based on a random ID and timestamp
* Can be run with blocking or non-blocking mode, allowing for asynchronous snapshot creation

**Usage:**

1. Set the following environment variables:
    * `PROXMOX_SERVER`: The URL of your Proxmox server
    * `PROXMOX_USER`: Your Proxmox user name
    * `PROXMOX_REALM`: Your Proxmox realm
    * `PROXMOX_TOKEN_NAME` and `PROXMOX_TOKEN_VALUE`: Your Proxmox API token (create a new one in the Proxmox web interface if you haven't already)
2. Run the script using Python 3

**Note:** This script is designed to be run on a machine with access to the Proxmox server, and requires the `proxmoxer` library to be installed.

### remove-snapshots.py

**Proxmox Snapshot Cleaner**

The Proxmox Snapshot Cleaner is a Python script that helps you manage snapshots on your Proxmox virtualization server. It scans all nodes and VMs for snapshots, lists them, and allows you to select which ones to delete.

**Features:**

* Scans all nodes and VMs for snapshots
* Lists all found snapshots with details like name, description, and date created
* Allows you to select which snapshots to delete using a checkbox dialog
* Deletes selected snapshots in parallel (using the Proxmox API)

**Usage:**

1. Set the following environment variables:
    * `PROXMOX_SERVER`: your Proxmox server's URL
    * `PROXMOX_USER`: your Proxmox username
    * `PROXMOX_REALM`: your Proxmox realm
    * `PROXMOX_TOKEN_NAME` and `PROXMOX_TOKEN_VALUE`: your Proxmox token credentials
2. Run the script using Python (e.g., `python remove-snapshots.py`)
3. The script will scan for snapshots, list them, and prompt you to select which ones to delete
4. Once you've selected the snapshots to delete, the script will delete them in parallel

**Note:** This script assumes you have a Proxmox server with the necessary environment variables set. It also requires the `proxmoxer` library to interact with the Proxmox API.
