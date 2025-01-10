import os
import sys
import argparse

import parted
from tabulate import tabulate


def output(block_device=None):
    def collect_device_info(device):
        table = []
        disk = parted.Disk(device)
        f.write(
            f"Device:  {os.path.basename(device.path)}\n"
            f"Model:   {device.model}\n"
            f"Table:   {disk.type}\n"
            f"Bytes:   {"{:,}".format(device.length * device.sectorSize)}\n"
            f"Sectors: {"{:,}".format(device.length)} - Bytes: {device.sectorSize}\n"
        )        
        for partition in disk.partitions:
            geometry = partition.geometry
            fileSystem = partition.fileSystem

            name = os.path.basename(partition.path)
            description = partition.name
            start = geometry.start
            end = geometry.end
            sectors = geometry.length
            bytes = sectors * device.sectorSize
            # sectors = int(partition.getLength(unit="sectors"))
            # bytes = int(partition.getLength(unit="B"))
            fs = fileSystem.type if fileSystem and fileSystem.type else None
            flags = partition.getFlagsAsString()

            row = [name, "{:,}".format(start), "{:,}".format(end), "{:,}".format(sectors), "{:,}".format(bytes), fs, description, flags]
            table.append(row)

        headers = ["PART", "START", "END", "SECTORS", "BYTES", "FS", "DESCRIPTION", "FLAGS"]
        f.write(tabulate(table, headers, tablefmt="rounded_outline"))
        f.write("\n")

    log_file = os.path.expanduser("~/blkinfo.log")
    with open(log_file, "w") as f:
        if block_device:
            try:
                device = parted.getDevice(block_device)
                collect_device_info(device)
            except Exception as e:
                f.write(f"Error: {e}\n")
        else:
            for device in parted.getAllDevices():
                collect_device_info(device)

    with open(log_file, "r") as f:
        print(f.read())
 

def main():

    if os.geteuid() != 0:
        print("\nThis tool must be run as root!\n")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Track bash shell activity.")
    parser.add_argument(
        "block_device",
        nargs="?",
        default=None,
        help="Optional block device or block device file to analyze (e.g., /dev/sda or path to an image file)."
    )
    args = parser.parse_args()

    if args.block_device:
        if not os.path.exists(args.block_device):
            print(f"\nError: The specified file or device '{args.block_device}' does not exist.\n")
            sys.exit(1)
        output(args.block_device)
    else:
        output()


if __name__ == "__main__":
    main()