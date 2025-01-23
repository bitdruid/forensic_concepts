#!bin/bash

IMAGE0="evidence.img"
IMAGE0_SIZE=16M
MOUNT_DIR="$PWD/mnt"

create() {
    echo "------------------------------"
    echo "Creating ... setup..."
    echo "------------------------------"

    echo "Creating disk image..."
    truncate -s "$IMAGE0_SIZE" "$PWD/$IMAGE0"

    LOOP0=$(losetup --find --show "$PWD/$IMAGE0")
    echo "Created loop device: $LOOP0"

    echo "Formatting with FAT16..."
    # see @ https://superuser.com/questions/332252/how-to-create-and-format-a-partition-using-a-bash-script
fdisk "$LOOP0" <<EOF
o
n
p
1


w
EOF

    echo "Reloading partition table..."
    partprobe "$LOOP0"
    LOOP0="${LOOP0}p1"

    echo "Formatting partition with FAT16..."
    mkfs.vfat -F 16 "$LOOP0"

    mkdir -p "$MOUNT_DIR"
    echo "Mounting disk..."
    mount "$LOOP0" "$MOUNT_DIR"

    echo "Disk created and mounted at $MOUNT_DIR"
}


fill() {
    if ! mount | grep -q "$MOUNT_DIR"; then
        echo "Error: Disk is not mounted. Please run the create command first."
        exit 1
    fi
    echo "------------------------------"
    echo "Filling disk with files..."
    echo "------------------------------"

    echo "evidence" > "$MOUNT_DIR/evidence.txt"

    # CYCLES=1  # iterations (1 text + 2 binary)
    # BINARY_FILE_SIZE=1  # binary file MiB
    # TEXT_CONTENT="evidence"

    # TOTAL_EVIDENCE_FILES=$CYCLES

    # TEXT_FILE_INDEX=1  
    # BINARY_FILE_INDEX=1
    # for ((cycle = 1; cycle <= CYCLES; cycle++)); do
    #     # binary1
    #     BINARY_FILE_NAME_1="$MOUNT_DIR/file_${BINARY_FILE_INDEX}.dat"
    #     echo "Creating binary file $BINARY_FILE_NAME_1 of size ${BINARY_FILE_SIZE}MB..."
    #     dd if=/dev/urandom of="$BINARY_FILE_NAME_1" bs=1M count=$BINARY_FILE_SIZE status=none
    #     ((BINARY_FILE_INDEX++))

    #     # binary2
    #     BINARY_FILE_NAME_2="$MOUNT_DIR/file_${BINARY_FILE_INDEX}.dat"
    #     echo "Creating binary file $BINARY_FILE_NAME_2 of size ${BINARY_FILE_SIZE}MB..."
    #     dd if=/dev/urandom of="$BINARY_FILE_NAME_2" bs=1M count=$BINARY_FILE_SIZE status=none
    #     ((BINARY_FILE_INDEX++))

    #     # text
    #     TEXT_FILE_NAME="$MOUNT_DIR/evidence_${TEXT_FILE_INDEX}-${TOTAL_EVIDENCE_FILES}.txt"
    #     TEXT_CONTENT="evidence${TEXT_FILE_INDEX}"
    #     echo "Creating text file $TEXT_FILE_NAME with content 'evidence${TEXT_FILE_INDEX}'..."
    #     echo -n "$TEXT_CONTENT" > "$TEXT_FILE_NAME"
    #     ((TEXT_FILE_INDEX++))
    # done

    echo "All files created successfully in $MOUNT_DIR."
}


destroy() {
    echo "------------------------------"
    echo "Destroying disk with wrong Start-LBA..."
    echo "------------------------------"

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting disk..."
        umount "$MOUNT_DIR"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)

    echo "Rewriting Start-LBA with wrong value..."
    # overwrites 0x1c5-0x1c8 (Start-LBA) with 0xdeadbeef
    echo -n -e '\xde\xad\xbe\xef' | dd of="$LOOP0" bs=1 seek=454 conv=notrunc
    echo "Inserting entry for non-existent partition..."
    # OPEN-BSD partition (0xa6), starting at sector 34816 (0x00008800) with size 1024 MiB (= 2097152 sectors = 0x00002000)
    echo -e '\x00\x44\x01\x44\xa6\x83\x02\x84\x00\x88\x00\x00\x00\x00x20\x00' | dd of="$LOOP0" bs=1 seek=462 conv=notrunc

}


remove() {
    echo "------------------------------"
    echo "Cleaning up ... setup..."
    echo "------------------------------"

    if mount | grep -q "$MOUNT_DIR"; then
        echo "Unmounting disk..."
        umount "$MOUNT_DIR"
    fi

    LOOP0=$(losetup -j "$PWD/$IMAGE0" | cut -d':' -f1)

    echo "Removing loop device..."
    losetup -d "$LOOP0"

    echo "Removing disk image..."
    rm -f "$PWD/$IMAGE0"

    echo "Cleanup complete."
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
