import os
import sys
import subprocess
import platform

import psutil
import distro
from tabulate import tabulate

def run_bash(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def collect_system_info():
    log_file = os.path.expanduser("~/wrkstinfo.log")
    with open(log_file, "w") as f:

        f.write("----- Workstation Status Collector -----\n\n")

        f.write("--------------------\n")
        f.write("OS-Type:\n")
        f.write("--------------------\n")
        f.write(platform.system() + "\n\n")

        f.write("--------------------\n")
        f.write("OS-Release:\n")
        f.write("--------------------\n")
        os_release = distro.name(pretty=True) if platform.system() == "Linux" else platform.version()
        f.write(os_release + "\n\n")

        f.write("--------------------\n")
        f.write("OS-Kernel:\n")
        f.write("--------------------\n")
        f.write(platform.release() + "\n\n")

        f.write("--------------------\n")
        f.write("System-Information:\n")
        f.write("--------------------\n")

        cpu_info = run_bash("lscpu | grep -E '^Model name' | awk -F: '{print $2}' | xargs")
        cpu_cores = int(run_bash("lscpu | grep -E '^Core\\(s\\) per socket' | awk -F: '{print $2}' | xargs"))
        cpu_threads = int(run_bash("lscpu | grep -E '^Thread\\(s\\) per core' | awk -F: '{print $2}' | xargs"))
        cpu_sockets = int(run_bash("lscpu | grep -E '^Socket\\(s\\)' | awk -F: '{print $2}' | xargs"))
        total_threads = cpu_cores * cpu_threads * cpu_sockets

        gpu_info = run_bash("lspci | grep -i vga | awk -F: '{print $3}' | xargs")

        ram_kb = psutil.virtual_memory().total // 1024
        formatted_ram_kb = f"{ram_kb:,}"

        f.write(f"CPU: {cpu_info}\n")
        f.write(f"GPU: {gpu_info}\n")
        f.write(f"RAM: {formatted_ram_kb} kB\n")
        f.write(f"CPU active sockets:   {cpu_sockets}\n")
        f.write(f"CPU active cores:     {cpu_cores}\n")
        f.write(f"CPU threads per core: {cpu_threads}\n")
        f.write(f"CPU total threads:    {total_threads}\n\n")

        # f.write("--------------------\n")
        # f.write("Packages manually installed:\n")
        # f.write("--------------------\n")

        # manually_installed = run_bash("apt-mark showmanual | xargs -r dpkg-query -W -f='${Package}\\t${Version}\\n'").split("\n")
        # table = [line.split("\t") for line in manually_installed]
        # f.write(tabulate(table, tablefmt="plain") + "\n\n")

        # f.write("--------------------\n")
        # f.write("Packages all installed:\n")
        # f.write("--------------------\n")

        # all_packages = run_bash("dpkg-query -W -f='${Package}\t${Version}\n'").splitlines()
        # table = [line.split("\t") for line in manually_installed]
        # f.write(tabulate(table, tablefmt="plain"))

        f.write("--------------------\n")
        f.write("Packages manually from all:\n")
        f.write("--------------------\n")

        manually_installed = set(run_bash("apt-mark showmanual").splitlines())
        all_packages = run_bash("dpkg-query -W -f='${Package}\t${Version}\n'").splitlines()
        package_table = []

        for line in all_packages:
            if "\t" in line:
                pkg_name, pkg_version = line.split("\t", 1)
                is_manual = "X" if pkg_name in manually_installed else ""
                package_table.append([is_manual, pkg_name, pkg_version])
                
        f.write(tabulate(package_table, tablefmt="plain"))
    
    with open(log_file, "r") as f:
        print(f.read())


def main():
    if os.geteuid() != 0:
        print("\nThis tool must be run as root!\n")
        sys.exit(1)
    collect_system_info()

if __name__ == "__main__":
    main()
