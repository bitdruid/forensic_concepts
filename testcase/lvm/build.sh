#!/bin/bash

set -e
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

# Variables
SCRIPT_DIR=$(dirname "$(realpath "$0")")
MOUNT_DIR="$SCRIPT_DIR/mnt"
IMAGE1="disk1.img"
IMAGE2="disk2.img"
VG_NAME="evidence_vg"
LV_NAME="evidence_lv"
LV_SIZE="24M"

create() {
    echo "Creating LVM setup..."

    echo "Creating disk images..."
    truncate -s 16M "$SCRIPT_DIR/$IMAGE1"
    truncate -s 16M "$SCRIPT_DIR/$IMAGE2"
    sleep 1

    LOOP1=$(losetup --find --show "$SCRIPT_DIR/$IMAGE1")
    LOOP2=$(losetup --find --show "$SCRIPT_DIR/$IMAGE2")
    echo "Created loop devices: $LOOP1, $LOOP2"

    echo "Creating physical volumes..."
    pvcreate "$LOOP1" "$LOOP2"

    echo "Creating volume group..."
    vgcreate "$VG_NAME" "$LOOP1" "$LOOP2"

    echo "Creating logical volume..."
    lvcreate -L "$LV_SIZE" -n "$LV_NAME" "$VG_NAME"

    echo "Formatting logical volume with FAT16..."
    mkfs.vfat -F 16 "/dev/$VG_NAME/$LV_NAME"

    mkdir -p "$MOUNT_DIR"
    echo "Mounting logical volume..."
    mount "/dev/$VG_NAME/$LV_NAME" "$MOUNT_DIR"

    echo "LVM successfully created and mounted at $MOUNT_DIR"
}

remove() {
    echo "Cleaning up LVM setup..."

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting logical volume..."
        umount "$MOUNT_DIR"
    fi

    if vgdisplay "$VG_NAME" > /dev/null 2>&1; then
        echo "Removing volume group..."
        vgremove -y "$VG_NAME"
    fi

    LOOP1=$(losetup -j "$SCRIPT_DIR/$IMAGE1" | cut -d':' -f1)
    LOOP2=$(losetup -j "$SCRIPT_DIR/$IMAGE2" | cut -d':' -f1)

    if [ -n "$LOOP1" ] && [ -n "$LOOP2" ]; then
        echo "Removing physical volumes..."
        pvremove -y "$LOOP1" "$LOOP2"
    fi

    if [ -n "$LOOP1" ]; then
        echo "Detaching loop device $LOOP1..."
        losetup -d "$LOOP1"
    fi
    if [ -n "$LOOP2" ]; then
        echo "Detaching loop device $LOOP2..."
        losetup -d "$LOOP2"
    fi

    echo "Deleting disk images..."
    rm -f "$SCRIPT_DIR/$IMAGE1" "$SCRIPT_DIR/$IMAGE2"

    if [ -d "$MOUNT_DIR" ]; then
        echo "Removing mount directory..."
        rmdir "$MOUNT_DIR"
    fi

    echo "Cleanup completed."
}

# Main
if [ "$1" == "create" ]; then
    create
elif [ "$1" == "remove" ]; then
    remove
else
    echo "Usage: $0 {create|remove}"
    exit 1
fi
