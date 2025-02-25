[![PyPI](https://img.shields.io/pypi/v/pyblkinfo)](https://pypi.org/project/pyblkinfo/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-orange)](https://ubuntu.com/download/desktop)

# blkinfo

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to output basic necessary infos about all attached block devices in a fast usable format. Forensic staff would be able to use this as a first step to document the system they are working on.

However, this project is just a CONCEPT - it shows how one step of documentation COULD be done - or moreover, what kind of output would be useful - as a small part of the overall forensic process. One limitation is that the script does only accept block devices and no images. Additionally, the script has not been extensively tested with all possible device configurations.

It uses Linux `lsblk` command to gather information about the block devices.

## Installation

`pip install pyblkinfo`

# Usage

- Run with `blkinfo <optional path>`
- Output is written to stdout
- Stores log in your home dir `blkinfo.log`

# Example log

```
Device:  sda
Model:   VBOX HARDDISK
Table:   dos
Bytes:   107,374,182,400
Sectors: 209,715,200 - 512 bytes
┌────────┬─────────┬─────────────┬─────────────┬─────────────────┬───────┬────────────┬─────────┐
│ PART   │ START   │ END         │ SECTORS     │ BYTES           │ FS    │ TYPE       │ LABEL   │
├────────┼─────────┼─────────────┼─────────────┼─────────────────┼───────┼────────────┼─────────┤
│ sda1   │ 2,048   │ 209,712,509 │ 209,710,462 │ 107,371,756,544 │ btrfs │ 0x83 Linux │         │
└────────┴─────────┴─────────────┴─────────────┴─────────────────┴───────┴────────────┴─────────┘
```
