#!/bin/bash

set -e
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

MOUNT_DIR="$PWD/mnt"
IMAGE0="evidence0.img"
IMAGE0_SIZE=16M
IMAGE1="evidence1.img"
IMAGE1_SIZE=8M
VG_NAME="evidence_vg"
LV_NAME="evidence_lv"
LV_SIZE="16M"


create() {
    echo "------------------------------"
    echo "Creating LVM setup..."
    echo "------------------------------"

    echo "Creating disk images..."
    truncate -s "$IMAGE0_SIZE" "$PWD/$IMAGE0"
    truncate -s "$IMAGE1_SIZE" "$PWD/$IMAGE1"
    sleep 1

    LOOP0=$(losetup --find --show "$PWD/$IMAGE0")
    LOOP1=$(losetup --find --show "$PWD/$IMAGE1")
    echo "Created loop devices: $LOOP0, $LOOP1"

    echo "Creating physical volumes..."
    pvcreate --norestorefile -u mnYfLc-AdVG-z036-DU2L-e8d2-76GU-2vMuU3 "$LOOP0"
    pvcreate --norestorefile -u PjypXK-UskX-30oP-SmM3-Jvtj-192v-aA1eHV "$LOOP1"

    echo "Creating volume group..."
    vgcreate "$VG_NAME" "$LOOP0" "$LOOP1"

    echo "Creating logical volume..."
    lvcreate -L "$LV_SIZE" -n "$LV_NAME" "$VG_NAME"

    echo "Formatting logical volume with FAT16..."
    mkfs.vfat -F 16 "/dev/$VG_NAME/$LV_NAME"

    mkdir -p "$MOUNT_DIR"
    echo "Mounting logical volume to $MOUNT_DIR..."
    mount "/dev/$VG_NAME/$LV_NAME" "$MOUNT_DIR"

    echo "DONE"
}


fill() {
    echo "------------------------------"
    echo "Filling logical volume with files..."
    echo "------------------------------"

    CYCLES=7  # iterations (1 text + 2 binary)
    BINARY_FILE_SIZE=1  # binary file MiB
    TEXT_CONTENT="evidence"

    TOTAL_EVIDENCE_FILES=$CYCLES

    TEXT_FILE_INDEX=1  
    BINARY_FILE_INDEX=1
    for ((cycle = 1; cycle <= CYCLES; cycle++)); do
        # binary1
        BINARY_FILE_NAME_1="$MOUNT_DIR/file_${BINARY_FILE_INDEX}.dat"
        echo "Creating binary file $BINARY_FILE_NAME_1 of size ${BINARY_FILE_SIZE}MB..."
        dd if=/dev/urandom of="$BINARY_FILE_NAME_1" bs=1M count=$BINARY_FILE_SIZE status=none
        ((BINARY_FILE_INDEX++))

        # binary2
        BINARY_FILE_NAME_2="$MOUNT_DIR/file_${BINARY_FILE_INDEX}.dat"
        echo "Creating binary file $BINARY_FILE_NAME_2 of size ${BINARY_FILE_SIZE}MB..."
        dd if=/dev/urandom of="$BINARY_FILE_NAME_2" bs=1M count=$BINARY_FILE_SIZE status=none
        ((BINARY_FILE_INDEX++))

        # text
        TEXT_FILE_NAME="$MOUNT_DIR/evidence_${TEXT_FILE_INDEX}-${TOTAL_EVIDENCE_FILES}.txt"
        TEXT_CONTENT="evidence${TEXT_FILE_INDEX}"
        echo "Creating text file $TEXT_FILE_NAME with content 'evidence${TEXT_FILE_INDEX}'..."
        echo -n "$TEXT_CONTENT" > "$TEXT_FILE_NAME"
        ((TEXT_FILE_INDEX++))
    done

    echo "DONE"
}


destroy() {
    echo "------------------------------"
    echo "Destroying LVM while keeping disk0..."
    echo "------------------------------"

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting logical volume..."
        umount "$MOUNT_DIR"
    fi

    if lvdisplay "/dev/$VG_NAME/$LV_NAME" > /dev/null 2>&1; then
        echo "Removing logical volume..."
        lvremove -y "/dev/$VG_NAME/$LV_NAME"
    fi

    if vgdisplay "$VG_NAME" > /dev/null 2>&1; then
        echo "Removing volume group..."
        vgremove -y "$VG_NAME"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)
    LOOP1=$(losetup -j "$PWD/$IMAGE1" | cut -d':' -f1)

    if [ -n "$LOOP0" ]; then
        echo "Detaching loop device $LOOP0..."
        losetup -d "$LOOP0"
    fi

    if [ -n "$LOOP1" ]; then
        echo "Removing physical volume on disk1..."
        pvremove -y "$LOOP1"
        echo "Detaching loop device $LOOP1..."
        losetup -d "$LOOP1"
        echo "Deleting disk1 image..."
        rm -f "$PWD/$IMAGE1"
    fi

    echo "Disk0 ($LOOP0) left."

    echo "DONE"
}


remove() {
    echo "------------------------------"
    echo "Cleaning up LVM setup..."
    echo "------------------------------"

    losetup -D

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting logical volume..."
        umount "$MOUNT_DIR"
    fi

    if vgdisplay "$VG_NAME" > /dev/null 2>&1; then
        echo "Removing volume group..."
        vgremove -y "$VG_NAME"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)
    LOOP1=$(losetup -j "$PWD/$IMAGE1" | cut -d':' -f1)

    if [ -n "$LOOP0" ]; then
        echo "Removing physical volume from $LOOP0..."
        pvremove -y "$LOOP0"
        echo "Detaching loop device $LOOP0..."
        losetup -d "$LOOP0"
    fi

    if [ -n "$LOOP1" ]; then
        echo "Removing physical volume from $LOOP1..."
        pvremove -y "$LOOP1"
        echo "Detaching loop device $LOOP1..."
        losetup -d "$LOOP1"
    fi

    echo "Deleting disk images..."
    rm -f "$PWD/$IMAGE0" "$PWD/$IMAGE1"

    if [ -d "$MOUNT_DIR" ]; then
        echo "Removing mount directory..."
        rmdir "$MOUNT_DIR"
    fi

    if [ -n "$PWD/spare.img" ]; then
        echo "Removing spare.img..."
        rm -f "$PWD/spare.img"
    fi
    
    if [ -n "$PWD/pv.head" ]; then
        echo "Removing pv.head..."
        rm -f "$PWD/pv.head"
    fi

    echo "DONE"
}

#####
###### Main
#####

if [ "$1" == "build" ]; then
    remove
    create
    fill
    destroy
elif [ "$1" == "create" ]; then
    create
elif [ "$1" == "remove" ]; then
    remove
elif [ "$1" == "fill" ]; then
    fill
elif [ "$1" == "destroy" ]; then
    destroy
else
    echo "Usage: $0 {build|create|remove|fill|destroy}"
    exit 1
fi
