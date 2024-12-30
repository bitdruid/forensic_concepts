[![PyPI](https://img.shields.io/pypi/v/pyblkinfo)](https://pypi.org/project/pyblkinfo/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-orange)](https://ubuntu.com/download/desktop)

# blkinfo

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to output basic necessary infos about the current workstation. Forensic staff would be able to use this as a first step to document the system they are working on.

However, this project is just a CONCEPT - it shows how one step of documentation COULD be done - or moreover, what kind of output would be useful - as a small part of the overall forensic process.

It uses Linux `uname`, `systemd-detect-virt`, `lsb_release`, `lscpu`, `lspci`, `free`, `apt-mark` command to gather information about block devices.

## Installation

`pip install pywrkstinfo`

# Usage

- Run with `wrkstinfo`
- Output is written to stdout

# Example log

```
```
