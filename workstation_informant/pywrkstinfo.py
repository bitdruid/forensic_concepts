import os
import sys
import platform
import psutil
import distro
import subprocess

def run_bash(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def collect_system_info():
    print("----- Workstation Status Collector -----")
    print("")

    print("--------------------")
    print("OS-Type:")
    print("--------------------")
    print(platform.system())
    print("")

    print("--------------------")
    print("OS-Release:")
    print("--------------------")
    os_release = distro.name(pretty=True) if platform.system() == "Linux" else platform.version()
    print(os_release)
    print("")

    print("--------------------")
    print("OS-Kernel:")
    print("--------------------")
    print(platform.release())
    print("")

    print("--------------------")
    print("System-Information:")
    print("--------------------")

    cpu_info = run_bash("lscpu | grep -E '^Model name' | awk -F: '{print $2}' | xargs")
    cpu_cores = int(run_bash("lscpu | grep -E '^Core\\(s\\) per socket' | awk -F: '{print $2}' | xargs"))
    cpu_threads = int(run_bash("lscpu | grep -E '^Thread\\(s\\) per core' | awk -F: '{print $2}' | xargs"))
    cpu_sockets = int(run_bash("lscpu | grep -E '^Socket\\(s\\)' | awk -F: '{print $2}' | xargs"))
    total_threads = cpu_cores * cpu_threads * cpu_sockets
    
    gpu_info = run_bash("lspci | grep -i vga | awk -F: '{print $3}' | xargs")
    
    ram_kb = psutil.virtual_memory().total // 1024
    formatted_ram_kb = f"{ram_kb:,}"

    print(f"CPU:    {cpu_info}")
    print(f"GPU:    {gpu_info}")
    print(f"RAM:    {formatted_ram_kb} kB")
    print("")
    print(f"CPU active sockets:   {cpu_sockets}")
    print(f"CPU active cores:     {cpu_cores}")
    print(f"CPU threads per core: {cpu_threads}")
    print(f"CPU total threads:    {total_threads}")
    print("")

    print("--------------------")
    print("Manually installed packages:")
    print("--------------------")
    try:
        manual_packages = subprocess.run(
            "comm -23 <(apt-mark showmanual | sort -u) "
            "<(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u) "
            "| xargs -r dpkg-query -W -f='${Package}\\t${Version}\\n' | column",
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True, executable="/bin/bash"
        ).stdout.strip()
        print(manual_packages)
    except Exception as e:
        print(f"Error fetching manually installed packages: {str(e)}")

def main():
    if os.geteuid() != 0:
        print("\nThis tool must be run as root!\n")
        sys.exit(1)
    collect_system_info()
