import json
import subprocess

DEVICE_PARTITION = {}
PARTITION_TYPE = {}

def load_types():
    """
    Loads the partition types from sfdisk --list-types (-T)
    """
    output = subprocess.check_output("sfdisk --list-types", shell=True).decode()
    output = output.split("\n")[1:]
    for line in output:
        if line:
            line = line.split()
            PARTITION_TYPE[line[0]] = line[1]

def collect_devices():
    """
    Collects all block devices and store them into DEVICE_PARTITION{device1: {...}, device2: {...}}
    """
    output = subprocess.check_output("lsblk --json -o NAME", shell=True).decode()
    output = json.loads(output)
    output = output["blockdevices"]
    for device in output:
        DEVICE_PARTITION[device["name"]] = {}
        DEVICE_PARTITION[device["name"]]["device_info"] = {}

def collect_infos():
    """
    Reads all devices from DEVICE_PARTITION and stores info into DEVICE_PARTITION_INFO{device1: {device_info: [...], partition1: [...], ...}, device2: {device_info: [...], partition1: [...], ...}}
    """
    for device in DEVICE_PARTITION:
        try:
            output_device = subprocess.check_output(f"fdisk -l /dev/{device}", shell=True, stderr=subprocess.STDOUT).decode()
            output_partition = subprocess.check_output(f"sfdisk --json /dev/{device}", shell=True).decode()
        except subprocess.CalledProcessError as e:
            DEVICE_PARTITION[device]["device_info"]["Status"] = "No information found"
            continue

        # gets device info
        device_info = output_device.split("\n")[0]
        device_info = device_info.split(",")
        device_info = [i.strip() for i in device_info]
        DEVICE_PARTITION[device]["device_info"]["model"] = ' '.join(subprocess.check_output(f"lsblk -o VENDOR,MODEL /dev/{device}", shell=True).decode().split("\n")[1].split())
        DEVICE_PARTITION[device]["device_info"]["table"] = output_device.split("Disklabel type: ")[1].split("\n")[0]
        DEVICE_PARTITION[device]["device_info"]["size"] = "{:,}".format(int(device_info[-2].split()[0])) + " bytes"
        DEVICE_PARTITION[device]["device_info"]["sectors"] = "{:,}".format(int(device_info[-1].split()[0])) + " sectors"
        DEVICE_PARTITION[device]["device_info"]["sector_size"] = output_device.split("Sector size (logical/physical): ")[1].split("bytes /")[0].strip()

        # gets partition info
        partition_info = json.loads(output_partition)["partitiontable"]["partitions"]
        for entry in partition_info:
            partition = entry["node"]
            DEVICE_PARTITION[device][partition] = {}
            DEVICE_PARTITION[device][partition]["name"] = entry["node"].split("dev/")[1]
            DEVICE_PARTITION[device][partition]["start"] = "{:,}".format(int(entry["start"]))
            DEVICE_PARTITION[device][partition]["end"] = "{:,}".format(int(entry["size"]) + int(entry["start"]) - 1)
            DEVICE_PARTITION[device][partition]["sectors"] = "{:,}".format(int(entry["size"]))
            DEVICE_PARTITION[device][partition]["type"] = PARTITION_TYPE[entry["type"]]
            DEVICE_PARTITION[device][partition]["size"] = "{:,}".format(int(entry["size"]) * int(DEVICE_PARTITION[device]["device_info"]["sector_size"].split("/")[0].split("bytes")[0].strip()))
            DEVICE_PARTITION[device][partition]["fs"] = ' '.join(subprocess.check_output(f"lsblk -o FSTYPE,FSVER {partition}", shell=True).decode().split("\n")[1].split())

def output():
    """
    Writes the output to a log file as a dynamically tabulated table and prints it to the console.
    """
    with open("blkinfo.log", "w") as log_file:
        for device in DEVICE_PARTITION:

            # device info
            device_info = DEVICE_PARTITION[device].get("device_info", {})
            if device_info.get('Status'):
                log_file.write(f"Device: {device}\nStatus: {device_info['Status']}\n\n")
                continue
            log_file.write(
                f"Device:  {device}\n"
                f"Model:   {device_info.get('model', 'N/A')}\n"
                f"Table:   {device_info.get('table', 'N/A')}\n"
                f"Size:    {device_info.get('size', 'N/A')}\n"
                f"Sectors: {device_info.get('sectors', 'N/A')} - Size: {device_info.get('sector_size', 'N/A')} bytes\n"
            )
            
            # partition table
            table_data = []
            headers = ["Name", "Start Sector", "End Sector", "Sectors", "Bytes", "Type", "FS"]
            for partition in DEVICE_PARTITION[device]:
                if partition != "device_info":
                    partition_data = DEVICE_PARTITION[device][partition]
                    table_data.append({
                        "Name": partition_data.get('name', 'N/A'),
                        "Start Sector": str(partition_data.get('start', 'N/A')),
                        "End Sector": str(partition_data.get('end', 'N/A')),
                        "Sectors": str(partition_data.get('sectors', 'N/A')),
                        "Bytes": str(partition_data.get('size', 'N/A')),
                        "Type": partition_data.get('type', 'N/A'),
                        "FS": partition_data.get('fs', 'N/A')
                    })

            # Pretty print the table
            # @see: https://stackoverflow.com/questions/17330139/python-printing-a-dictionary-as-a-horizontal-table-with-headers
            if table_data:
                colList = headers
                myList = [colList]  # header
                for item in table_data:
                    myList.append([str(item[col] if item[col] is not None else '') for col in colList])
                
                colSize = [max(map(len, col)) for col in zip(*myList)]
                colAmount = len(colSize)
                tableSize = sum(colSize) + len(colSize) + colAmount * 2 - 3
                log_file.write("-" * tableSize + "\n")

                formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
                myList.insert(1, ['-' * i for i in colSize])
                for item in myList:
                    log_file.write(formatStr.format(*item) + "\n")
            else:
                log_file.write("No partitions found\n")
            
            log_file.write("\n")

    with open("blkinfo.log", "r") as log_file:
        print("\n" + log_file.read())

def main():
    load_types()
    collect_devices()
    collect_infos()
    output()

if __name__ == "__main__":
    main()