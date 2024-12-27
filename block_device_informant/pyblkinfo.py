# disk1     partition-table     size_bytes      sectors  uuid
# partition1  type  filesystem  start sector  end sector  sector amount  size  partuuid  label
# partition2  type  filesystem  start sector  end sector  sector amount  size  partuuid  label
# disk2     size bytes      sectors  uuid
# partition1  type  filesystem  start sector  end sector  sector amount  size  partuuid  label
# partition2  type  filesystem  start sector  end sector  sector amount  size  partuuid  label

import os
import json
import subprocess

DEVICE_PARTITION = {}

def collect_devices():
    """
    Collects all block devices and store them into DEVICE_PARTITION{device1: {...}, device2: {...}}
    """
    output = subprocess.check_output("lsblk --json -o NAME", shell=True).decode()
    output = json.loads(output)
    output = output["blockdevices"]
    for device in output:
        DEVICE_PARTITION[device["name"]] = {}

def collect_infos():
    """
    Reads all devices from DEVICE_PARTITION and stores info into DEVICE_PARTITION_INFO{device1: {device_info: [...], partition1: [...], ...}, device2: {device_info: [...], partition1: [...], ...}}
    """
    for device in DEVICE_PARTITION:

        output = subprocess.check_output(f"sfdisk -l /dev/{device}", shell=True).decode()

        # gets device info
        device_info = output.split("\n")[0]
        device_info = device_info.split(",")
        device_info = [i.strip() for i in device_info]
        DEVICE_PARTITION[device]["device_info"] = {}
        DEVICE_PARTITION[device]["device_info"]["table"] = output.split("Disklabel type: ")[1].split("\n")[0]
        DEVICE_PARTITION[device]["device_info"]["size"] = device_info[-2]
        DEVICE_PARTITION[device]["device_info"]["sectors"] = device_info[-1]
        DEVICE_PARTITION[device]["device_info"]["sector_size L/P"] = output.split("Sector size (logical/physical): ")[1].split("\n")[0]

        # gets partition info
        partition_info = output.split("\nDevice")[1]
        partition_info = partition_info.split("\n")
        del partition_info[0]
        partition_info = list(filter(None, partition_info))
        for line in partition_info:
            parts = line.split(None, 5)
            if len(parts) == 6:
                partition = parts[0].split("dev/")[1]
                start = parts[1]
                end = parts[2]
                sectors = parts[3]
                type = parts[5]
                DEVICE_PARTITION[device][partition] = {}
                DEVICE_PARTITION[device][partition]["name"] = partition
                DEVICE_PARTITION[device][partition]["start"] = start
                DEVICE_PARTITION[device][partition]["end"] = end
                DEVICE_PARTITION[device][partition]["sectors"] = sectors
                DEVICE_PARTITION[device][partition]["type"] = type
                DEVICE_PARTITION[device][partition]["fs"] = ' '.join(subprocess.check_output(f"lsblk -o FSTYPE,FSVER /dev/{partition}", shell=True).decode().split("\n")[1].split())

        __import__("pprint").pprint(DEVICE_PARTITION)
        os._exit(1)

def build_output():
    pass

def output():
    pass

def main():
    collect_devices()
    collect_infos()
    build_output()
    output()

if __name__ == "__main__":
    main()