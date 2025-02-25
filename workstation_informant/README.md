[![PyPI](https://img.shields.io/pypi/v/pyblkinfo)](https://pypi.org/project/pyblkinfo/)
![Python Version](https://img.shields.io/badge/Python-3.6-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-orange)](https://ubuntu.com/download/desktop)

# wrkstinfo

This little project is just a conceptual work used for my thesis about documentation of forensic processes.

It's purpose is to output basic necessary infos about the current workstation. Forensic staff would be able to use this as a first step to document the system they are working on.

However, this project is just a CONCEPT - it shows how one step of documentation COULD be done - or moreover, what kind of output would be useful - as a small part of the overall forensic process.

It uses Linux `uname`, `systemd-detect-virt`, `lsb_release`, `lscpu`, `lspci`, `free`, `apt-mark`, `dpkg-query` command to gather information about the system.

## Installation

`pip install pywrkstinfo`

# Usage

- Run with `wrkstinfo`
- Output is written to stdout
- Stores log in your home dir `wrkstinfo.log`

# Example log

```
----- Workstation Status Collector -----

--------------------
OS-Type:
--------------------
Linux

--------------------
OS-Release:
--------------------
Ubuntu 24.10

--------------------
OS-Kernel:
--------------------
6.13.0-rc2-1-MANJARO

--------------------
System-Information:
--------------------
CPU:    Intel(R) Core(TM) i3-7100U CPU @ 2.40GHz
GPU:    
RAM:    16,256,576 kB
CPU active sockets:   1
CPU active cores:     2
CPU threads per core: 2
CPU total threads:    4

--------------------
Packages manually from all:
--------------------
   adduser                    3.137ubuntu2
X  apt                        2.9.8
X  autoconf                   2.72-3
   automake                   1:1.16.5-1.3ubuntu1
   autotools-dev              20220109.1
X  base-files                 13.3ubuntu6
X  base-passwd                3.6.4
X  bash                       5.2.32-1ubuntu1
   binfmt-support             2.2.2-7
   ...
```
