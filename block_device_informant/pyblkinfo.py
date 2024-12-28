import os
import json
import subprocess

DEVICE_PARTITION = {}

def collect_data():
    output = subprocess.check_output("lsblk --json -b -o NAME,LABEL,VENDOR,MODEL,PTTYPE,START,SIZE,LOG-SEC,FSTYPE,FSVER", shell=True).decode()
    output = json.loads(output)
    output = output["blockdevices"]

    try:
        for entry in output:
            for key, value in entry.items():
                if value is None:
                    entry[key] = ""
            device = entry["name"]
            DEVICE_PARTITION[device] = {}
            DEVICE_PARTITION[device]["device_info"] = {}
            DEVICE_PARTITION[device]["device_info"]["model"] = entry["vendor"].strip() + " " + entry["model"].strip()
            DEVICE_PARTITION[device]["device_info"]["table"] = entry["pttype"]
            DEVICE_PARTITION[device]["device_info"]["size"] = entry["size"]
            DEVICE_PARTITION[device]["device_info"]["sectors"] = entry["size"] // entry["log-sec"]
            DEVICE_PARTITION[device]["device_info"]["sector_size"] = str(entry["log-sec"])

            for entry2 in entry["children"]:
                for key, value in entry2.items():
                    if value is None:
                        entry2[key] = ""
                partition = entry2["name"]
                DEVICE_PARTITION[device][partition] = {}
                DEVICE_PARTITION[device][partition]["name"] = entry2["name"]
                DEVICE_PARTITION[device][partition]["label"] = entry2["label"]
                DEVICE_PARTITION[device][partition]["start"] = entry2["start"]
                DEVICE_PARTITION[device][partition]["end"] = entry2["start"] + (entry2["size"] // entry["log-sec"]) - 1
                DEVICE_PARTITION[device][partition]["sectors"] = entry2["size"] // entry["log-sec"]
                DEVICE_PARTITION[device][partition]["size"] = entry2["size"]
                DEVICE_PARTITION[device][partition]["fs"] = entry2["fstype"] + " " + entry2["fsver"]
    except Exception as e:
        DEVICE_PARTITION[device]["device_info"]["Status"] = "No information available"

def output():
    """
    Writes the output to a log file as a dynamically tabulated table and prints it to the console.
    """
    log_file = os.path.expanduser("~/blkinfo.log")
    with open(log_file, "w") as log_file:
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
                f"Size:    {"{:,}".format(int(device_info.get('size', 0)))} bytes\n"
                f"Sectors: {"{:,}".format(int(device_info.get('sectors', 'N/A')))} - logical size: {device_info.get('sector_size', 'N/A')} bytes\n"
            )
            
            # partition table
            table_data = []
            headers = ["Name", "Label", "Start Sector", "End Sector", "Sectors", "Bytes", "FS"]
            for partition in DEVICE_PARTITION[device]:
                if partition != "device_info":
                    partition_data = DEVICE_PARTITION[device][partition]
                    table_data.append({
                        "Name": partition_data.get('name', 'N/A'),
                        "Label": partition_data.get('label', 'N/A'),
                        "Start Sector": "{:,}".format(int(partition_data.get('start', 0))),
                        "End Sector": "{:,}".format(int(partition_data.get('end', 0))),
                        "Sectors": "{:,}".format(int(partition_data.get('sectors', 0))),
                        "Bytes": "{:,}".format(int(partition_data.get('size', 0))),
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

    with open(log_file.name, "r") as log_file:
        print(log_file.read())

    print(f"Output written to {log_file.name}\n")

def main():
    collect_data()
    output()

if __name__ == "__main__":
    main()