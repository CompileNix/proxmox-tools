#!python3

import os
import time
import signal
import sys
import random
import base64
import proxmoxer
import proxmoxer.tools
from rich.progress import BarColumn, MofNCompleteColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.progress import Progress
from rich.console import Console
from rich import print as rprint
from rich.pretty import pprint
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
proxmox = proxmoxer.ProxmoxAPI(server, backend='https', user=f'{user}@{realm}', token_name=token_name, token_value=token_value, verify_ssl=True, timeout=None)


def create_snapshot(node, vm, blocking=True):
    random_id = random.randint(0, 2**32 - 1)
    random_id_str = base64.b64encode(str(random_id).encode()).decode().rstrip('=')
    params = {
        'snapname': f'{user}_Automatic_Snapshot_{random_id_str}',
        'description': time.strftime('%a, %d %b %Y %H:%M:%S %z'),
        'vmstate': int(True),
    }
    print(f"create snapshot for {vm['name']}...")
    taskid = proxmox.nodes(node["node"]).qemu(vm['vmid']).snapshot.post(**params)
    if blocking:
        return proxmoxer.tools.Tasks.blocking_status(proxmox, taskid, timeout=3600)
    else:
        return taskid


print(f'looking for proxmox nodes...')
vms = []
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:
    scanning_total_steps = 0
    scanning_progress = progress.add_task("Scanning Nodes", total=None)
    nodes = proxmox.nodes.get()
    scanning_total_steps = len(nodes)
    progress.update(scanning_progress, total=scanning_total_steps)

    for node in nodes:
        print(f'looking for vms on {node["node"]}...')
        new_vms = proxmox.nodes(node["node"]).qemu.get()
        progress.update(scanning_progress, advance=1)
        for vm in new_vms:
            print(f'found vm on {node["node"]}: {vm["vmid"]} - {vm["name"]}')
            vms.append({
                'node': node,
                'vm': vm,
            })
    if len(vms) > 0:
        vms = sorted(vms, key=lambda x: x['vm']['vmid'])
    rprint(f'found {len(vms)} total vm\'s')

if len(vms) == 0:
    sys.exit(0)

items = []
defaults = []
for vm in vms:
    (node, vm) = vm.values()
    item = f'{vm["vmid"]}: {vm["name"]}'
    items.append((item, item))
    defaults.append(item)
# result = checkboxlist_dialog(
#     title="Select VMs:",
#     text="Please select VM's for which you want to create a snapshot, using space bar:",
#     values=items,
#     default_values=defaults,
# ).run()
    rprint(f'- {vm["vmid"]} -> {vm["name"]}')
result = input('Please select VM\'s (id), using space separator. Or press enter to select all VMs: ')
# if not result:
#     sys.exit(0)
selected_vms = []
if not result:
    selected_vms = vms
else:
    result_split = result.split(' ')
    for vm in vms:
        (node, vm) = vm.values()
        # if f'{vm["vmid"]}: {vm["name"]}' in result:
        if str(vm["vmid"]) in result_split:
            selected_vms.append({
                'node': node,
                'vm': vm,
            })

with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
) as progress:
    creation_total_steps = len(selected_vms)
    creation_progress = progress.add_task("Creating Snapshots", total=creation_total_steps)
    for vm in selected_vms:
        (node, vm) = vm.values()
        create_snapshot(node, vm)
        progress.update(creation_progress, advance=1)
