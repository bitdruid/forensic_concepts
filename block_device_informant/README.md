[![PyPI](https://img.shields.io/pypi/v/pyblkinfo)](https://pypi.org/project/pyblkinfo/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# blkinfo

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to output basic necessary infos about all attached block devices in a fast usable format. Forensic staff would be able to use this as a first step to document the system they are working on.

However, this project is just a CONCEPT - it demonstrates how one step of documentation COULD be performed as a small part of the entire forensic process. One limitation is that the script does not directly interact with the block devices but rather gathers information through system commands. This means it relies on the accuracy and availability of these commands. Additionally, the script has not been extensively tested with all possible device configurations.

It uses Linux `lsblk` and `fdisk` commands to gather information about block devices.

## Installation

`pip install pyblkinfo`

# Usage

- Run with `blkinfo`
- Output is written to stdout
- Stores log in your home dir `blkinfo.log`

# Example log

```
```
