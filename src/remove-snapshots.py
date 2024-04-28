#!python3

import os
import time
import signal
import sys
import proxmoxer
import proxmoxer.tools
from rich.progress import BarColumn, MofNCompleteColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, track
from rich.progress import Progress
from rich.console import Console
console = Console()
from rich.traceback import install
install(show_locals=False)
from prompt_toolkit.shortcuts import checkboxlist_dialog

def exit_gracefully(*args):
    print(f"\nExiting requested by process signal INT or TERM")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

server = os.environ.get('PROXMOX_SERVER')
user = os.environ.get('PROXMOX_USER')
realm = os.environ.get('PROXMOX_REALM')
token_name = os.environ.get('PROXMOX_TOKEN_NAME')
token_value = os.environ.get('PROXMOX_TOKEN_VALUE')
proxmox = proxmoxer.ProxmoxAPI(server, backend='https', user=f'{user}@{realm}', token_name=token_name, token_value=token_value, verify_ssl=True)


def print_snapshot(snapshot):
    snap_time = time.localtime(int(snapshot['snaptime']))
    console.print(f'[green]{vm["name"]}[/green]:', highlight=False)
    console.print(f'    Name: [bold]{snapshot["name"]}[/bold]', highlight=False)
    if snapshot["description"]:
        print(f'    Description: {snapshot["description"]}')
    print(f'    Date: {time.strftime("%a, %d %b %Y %H:%M:%S %z", snap_time)}')

def remove_snapshot(node, vm, snapshot, blocking=True):
    print(f"remove snapshot {snapshot['name']} for VM {vm['name']}...")
    # time.sleep(1)
    taskid = proxmox.nodes(node["node"]).qemu(vm['vmid']).snapshot(snapshot['name']).delete()
    if blocking:
        return proxmoxer.tools.Tasks.blocking_status(proxmox, taskid, timeout=900)
    else:
        return taskid


print(f'looking for proxmox nodes...')
current_snapshots = []
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:
    scanning_total_steps = 0
    scanning_progress = progress.add_task("Scanning", total=None)
    nodes = proxmox.nodes.get()
    scanning_total_steps = len(nodes)
    progress.update(scanning_progress, total=scanning_total_steps)

    for node in nodes:
        print(f'looking for vms on {node["node"]}...')
        vms = proxmox.nodes(node["node"]).qemu.get()
        progress.update(scanning_progress, advance=1)
        scanning_total_steps += len(vms)
        progress.update(scanning_progress, total=scanning_total_steps)

        for vm in vms:
            print(f'looking for snapshots on {node["node"]} for vm {vm["name"]}...', end='')
            snapshots = proxmox.nodes(node["node"]).qemu(vm['vmid']).snapshot.get()
            progress.update(scanning_progress, advance=1)

            # there is always one "fake" snapshot named "current"
            if snapshots and len(snapshots) > 1:
                print(f'found {len(snapshots) - 1}')
            else:
                print(f'found none')
                continue

            for snapshot in snapshots:
                if snapshot['name'] == 'current':
                    continue
                current_snapshots.append({
                    'node': node,
                    'vm': vm,
                    'snapshot': snapshot
                })
print(f'found {len(current_snapshots)} total snapshots')

if len(current_snapshots) == 0:
    sys.exit(0)

for snapshot in current_snapshots:
    (node, vm, snapshot) = snapshot.values()
    print_snapshot(snapshot)

items = []
defaults = []
for snapshot in current_snapshots:
    (node, vm, snapshot) = snapshot.values()
    item = f"{vm['name']} ({vm['vmid']}): {snapshot['name']}"
    items.append((item, item))
    defaults.append(item)

result = checkboxlist_dialog(
    title="Select Snapshots:",
    text="Please select snapshots you want to remove using space bar:",
    values=items,
    default_values=defaults,
).run()
if not result:
    sys.exit(0)
selected_snapshots = []
for snapshot in current_snapshots:
    (node, vm, snapshot) = snapshot.values()
    if f"{vm['name']} ({vm['vmid']}): {snapshot['name']}" in result:
        selected_snapshots.append({
            'node': node,
            'vm': vm,
            'snapshot': snapshot
        })

with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:
    deletion_total_steps = len(selected_snapshots)
    deletion_progress = progress.add_task("Deleting", total=deletion_total_steps)
    for snapshot in selected_snapshots:
        (node, vm, snapshot) = snapshot.values()
        remove_snapshot(node, vm, snapshot)
        progress.update(deletion_progress, advance=1)
