    echo "----- Workstation Status Collector -----"
    echo ""
    echo "--------------------"
    echo "VM-Status:"
    echo "--------------------"
    systemd-detect-virt
    echo ""
    echo "--------------------"
    echo "OS-Type:"
    echo "--------------------"
    uname -o
    echo ""
    echo "--------------------"
    echo "OS-Release:"
    echo "--------------------"
    lsb_release -ds 2>/dev/null
    echo ""
    echo "--------------------"
    echo "OS-Kernel:"
    echo "--------------------"
    uname -r
    echo ""
    echo "--------------------"
    echo "System-Information:"
    echo "--------------------"
    cpu_info=$(lscpu | grep -E '^Model name' | awk -F: '{print $2}' | xargs)
    cpu_cores=$(lscpu | grep -E '^Core\(s\) per socket' | awk -F: '{print $2}' | xargs)
    cpu_threads=$(lscpu | grep -E '^Thread\(s\) per core' | awk -F: '{print $2}' | xargs)
    cpu_sockets=$(lscpu | grep -E '^Socket\(s\)' | awk -F: '{print $2}' | xargs)
    total_threads=$((cpu_cores * cpu_threads * cpu_sockets))
    gpu_info=$(lspci | grep -i vga | awk -F: '{print $3}' | xargs)
    ram_kb=$(free -k | awk '/^Mem/ {print $2}')
    formatted_ram_kb=$(printf "%'d" "$ram_kb")
    printf "CPU:    %s\n" "$cpu_info"
    printf "GPU:    %s\n" "$gpu_info"
    printf "RAM:    %s kB\n" "$formatted_ram_kb"
    echo ""
    printf "CPU active sockets:   %s\n" "$cpu_sockets"
    printf "CPU active cores:     %s\n" "$cpu_cores"
    printf "CPU threads per core: %s\n" "$cpu_threads"
    printf "CPU total threads:    %s\n" "$total_threads"
    echo ""
    echo "--------------------"
    echo "Manually installed packages:"
    echo "--------------------"
    comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u) | xargs -r dpkg-query -W -f='${Package}\t${Version}\n' | column -
