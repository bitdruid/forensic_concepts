#!bin/bash

MOUNT_DIR="$PWD/mnt"

create() {
    echo "------------------------------"
    echo "Creating ... setup..."
    echo "------------------------------"
}


fill() {
    echo "------------------------------"
    echo "Filling logical volume with files..."
    echo "------------------------------"

}


destroy() {
    echo "------------------------------"
    echo "Destroying..."
    echo "------------------------------"
}


remove() {
    echo "------------------------------"
    echo "Cleaning up ... setup..."
    echo "------------------------------"
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
