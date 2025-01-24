#!/bin/bash

IMAGE0="evidence.img"
IMAGE0_SIZE=16M
MOUNT_DIR="$PWD/mnt"

create() {
    echo "------------------------------"
    echo "Creating disk setup..."
    echo "------------------------------"

    echo "Creating disk image..."
    truncate -s "$IMAGE0_SIZE" "$PWD/$IMAGE0"

    LOOP0=$(losetup --find --show "$PWD/$IMAGE0")
    echo "Created loop device: $LOOP0"

    echo "Creating msdos partition table..."
    echo 'type=83' | sfdisk "$LOOP0" > /dev/null 2>&1 # surpress "Re-reading the partition table failed..."

    echo "Reloading partition table..."
    partprobe "$LOOP0"
    LOOP0="${LOOP0}p1"

    echo "Formatting partition with FAT16..."
    mkfs.vfat -F 16 "$LOOP0"

    mkdir -p "$MOUNT_DIR"
    echo "Mounting disk to $MOUNT_DIR..."
    mount "$LOOP0" "$MOUNT_DIR"

    echo "DONE"
}


fill() {
    echo "------------------------------"
    echo "Filling disk with files..."
    echo "------------------------------"

    echo "evidence" > "$MOUNT_DIR/evidence.txt"

    echo "DONE"
}


destroy() {
    echo "------------------------------"
    echo "Destroying disk with wrong partition table..."
    echo "------------------------------"

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting disk..."
        umount "$MOUNT_DIR"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)

    echo "Rewriting Start-LBA with deadbeef..."
    # overwrites 0x1c5-0x1c8 (Start-LBA) with 0xdeadbeef
    echo -n -e '\xde\xad\xbe\xef' | dd of="$LOOP0" bs=1 seek=454 conv=notrunc
    echo "Inserting entry for non-existent OPEN-BSD partition..."
    # OPEN-BSD partition (0xa6), starting at sector 34816 (0x00008800) with size 1024 MiB (= 2097152 sectors = 0x00002000)
    #echo -e '\x00\x44\x01\x44\xa6\x83\x02\x84\x00\x88\x00\x00\x00\x00\x20\x00' | dd of="$LOOP0" bs=1 seek=462 conv=notrunc
    
    echo "DONE"
}


remove() {
    echo "------------------------------"
    echo "Cleaning up disk setup..."
    echo "------------------------------"

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting disk..."
        umount "$MOUNT_DIR"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)

    if [ -n "$LOOP0" ]; then
        echo "Detaching loop device $LOOP0..."
        losetup -d "$LOOP0"
    fi

    if [ -f "$PWD/$IMAGE0" ]; then
        echo "Removing disk image..."
        rm -f "$PWD/$IMAGE0"
    fi

    if [ -d "$MOUNT_DIR" ]; then
        echo "Removing mount directory..."
        rmdir "$MOUNT_DIR"
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
