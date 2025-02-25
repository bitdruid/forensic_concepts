import os
import sys
import argparse
import subprocess
import json
from tabulate import tabulate

def load_partition_info(block_device):
    """
    Loads partition information from lsblk
    """
    try:
        output = subprocess.check_output(f"lsblk -O -b --json {block_device}", shell=True, stderr=subprocess.DEVNULL).decode()
        partition_info = json.loads(output)
    except subprocess.CalledProcessError as e:
        if e.returncode == 32:
            print(f"\nError: The device '{block_device}' is not a block device.\n")
        else:
            print(f"\nError: Failed to run lsblk for '{block_device}' with error code {e.returncode}.\n")
        sys.exit(1)

    def replace_none_with_empty_string(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None or (isinstance(value, str) and value.lower() == "none"):
                    data[key] = ""
                else:
                    replace_none_with_empty_string(value)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                replace_none_with_empty_string(item)

    replace_none_with_empty_string(partition_info)
    
    return partition_info

def output(block_device=None):
    """
    Writes data to log and prints
    """
    def collect_device_info(device):
        """
        Collects data
        """
        table = []
        partition_info = load_partition_info(device)
        device_name = os.path.basename(device)
        total_size = partition_info['blockdevices'][0]['size']
        log_sec = partition_info['blockdevices'][0]['log-sec']

        with open(log_file, "w") as f:
            f.write(
                f"Device:  {device_name}\n"
                f"Model:   {partition_info['blockdevices'][0]['model']}\n"
                f"Table:   {partition_info['blockdevices'][0]['pttype']}\n"
                f"Bytes:   {total_size:,}\n"
                f"Sectors: {int((total_size / log_sec)):,} - {log_sec} bytes\n"
            )
            f.write(f"")
            for partition in partition_info['blockdevices'][0].get('children', []):

                name = partition["name"]
                bytes = partition["size"]
                sectors = int(bytes / log_sec)
                start = partition["start"]
                end = int(start + (bytes / log_sec) - 1)

                fs_type = partition.get("fstype", "")
                fs_ver = partition.get("fsver", "")
                part_type = partition.get("parttype", "")
                part_name = partition.get("parttypename", "")
                label = partition.get("label", "")

                fs = f"{fs_type} {fs_ver}"
                type = f"{part_type} {part_name}"
                row = [name, f"{start:,}", f"{end:,}", f"{sectors:,}", f"{bytes:,}", fs, type, label]
                table.append(row)

            headers = ["PART", "START", "END", "SECTORS", "BYTES", "FS", "TYPE", "LABEL"]
            f.write(tabulate(table, headers, tablefmt="simple_outline"))
            f.write("\n")

    log_file = os.path.expanduser("~/blkinfo.log")
    if block_device:
        if not os.path.exists(block_device):
            print(f"\nError: The specified file or device '{block_device}' does not exist.\n")
            sys.exit(1)
        collect_device_info(block_device)
    else:
        print("\nError: No block device specified.\n")
        sys.exit(1)

    with open(log_file, "r") as f:
        print(f.read())

def main():
    if os.geteuid() != 0:
        print("\nThis tool must be run as root!\n")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Get an overview of attached block-devices or image-files.")
    parser.add_argument(
        "block_device",
        nargs="?",
        default=None,
        help="Optional block device or block device file to analyze (e.g., /dev/sda or path to an image file)."
    )
    args = parser.parse_args()

    if args.block_device:
        output(args.block_device)
    else:
        print("\nError: No block device specified.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
