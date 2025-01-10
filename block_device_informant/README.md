[![PyPI](https://img.shields.io/pypi/v/pyblkinfo)](https://pypi.org/project/pyblkinfo/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-orange)](https://ubuntu.com/download/desktop)

# blkinfo

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to output basic necessary infos about all attached block devices in a fast usable format. Forensic staff would be able to use this as a first step to document the system they are working on.

However, this project is just a CONCEPT - it shows how one step of documentation COULD be done - or moreover, what kind of output would be useful - as a small part of the overall forensic process. One limitation is that the script does only accept block devices and not a specific partition. It accepts images as parameter (`blkinfo <path>`). Additionally, the script has not been extensively tested with all possible device configurations.

It uses Linux python `pyparted` library to gather information about block devices.

## Installation

`pip install pyblkinfo`

# Usage

- Run with `blkinfo <optional path>`
- Output is written to stdout
- Stores log in your home dir `blkinfo.log`

# Example log

```
Device:  nvme0n1
Model:   Force MP510
Table:   gpt
Bytes:   240,057,409,536
Sectors: 468,862,128 - Bytes: 512
┌───────────┬─────────────┬─────────────┬─────────────┬─────────────────┬───────┬──────────────────────────────┬───────────────────────┐
│ PART      │ START       │ END         │ SECTORS     │ BYTES           │ FS    │ DESCRIPTION                  │ FLAGS                 │
├───────────┼─────────────┼─────────────┼─────────────┼─────────────────┼───────┼──────────────────────────────┼───────────────────────┤
│ nvme0n1p1 │ 4,096       │ 618,495     │ 614,400     │ 314,572,800     │ fat32 │                              │ boot, esp             │
│ nvme0n1p2 │ 618,496     │ 273,551,359 │ 272,932,864 │ 139,741,626,368 │ btrfs │ root                         │                       │
│ nvme0n1p3 │ 273,551,360 │ 273,584,127 │ 32,768      │ 16,777,216      │       │ Microsoft reserved partition │ msftres, no_automount │
│ nvme0n1p4 │ 273,584,128 │ 468,860,927 │ 195,276,800 │ 99,981,721,600  │ ntfs  │ Basic data partition         │ msftdata              │
└───────────┴─────────────┴─────────────┴─────────────┴─────────────────┴───────┴──────────────────────────────┴───────────────────────┘
```
