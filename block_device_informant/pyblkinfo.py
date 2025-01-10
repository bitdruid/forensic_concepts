import os
import sys
import argparse

import parted
from tabulate import tabulate

def collect_devices(block_device=None):
    with open("blkinfo.log", "w") as log_file:
        for device in parted.getAllDevices():

            table = []

            disk = parted.Disk(device)
            log_file.write(
                f"Device:  {os.path.basename(device.path)}\n"
                f"Model:   {device.model}\n"
                f"Table:   {disk.type}\n"
                f"Bytes:   {"{:,}".format(device.length * device.sectorSize)}\n"
                f"Sectors: {"{:,}".format(device.length)} - Bytes: {device.sectorSize}\n"
            )
            log_file.write("\n")
            for partition in disk.partitions:
                geometry = partition.geometry
                fileSystem = partition.fileSystem

                name = os.path.basename(partition.path)
                description = partition.name
                start = geometry.start
                end = geometry.end
                sectors = geometry.length
                bytes = sectors * device.sectorSize
                fs = fileSystem.type if fileSystem and fileSystem.type else None
                flags = None

                row = [name, "{:,}".format(start), "{:,}".format(end), "{:,}".format(sectors), "{:,}".format(bytes), fs, description, flags]
                table.append(row)

            headers=["PART","START","END","SECTORS","BYTES","FS","DESCRIPTION","FLAGS"]
            log_file.write(tabulate(table, headers, tablefmt="github"))

    with open("blkinfo.log", "r") as log_file:
        print("\n" + log_file.read())
 

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
        collect_devices(args.block_device)
    else:
        collect_devices()


if __name__ == "__main__":
    main()