# Linux-embedded-PCU
Open Source Linux embedded power control unit with python API and UI for convivial control and monitoring.

## Description
TODO
## Installation

### OS

Use Raspberry Pi imager to write Raspbian Lite OS on your SD card

Connect Pi to a screen and keyboard

### Raspbian settings

Update Raspbian

```
sudo apt-get update
sudo apt-get upgrade
```

Go to config:

```
sudo raspi-config
```

In system options, set a new password, and a desired PCU hostname

In interface options, enable SPI and SSH

Reboot system

### Install dependencies

Install pip3

```
sudo apt-get install python3-pip
```

Install pipenv:

```
pip3 install pipenv
```

Install bridge-utils

```
sudo apt-get install bridge-utils
```

### Sync PCU files

Clone Linux-embedded repository and copy files (here using SSH)

For Windows use scp:

```
scp -prq software/pcu pi@{hostname}.local:/home/pi
```

For linux you can use ssh-copy

### Setup launch

On the Pi, set up the pipenv virtual environment

```
cd pcu
python3 -m pipenv install
```

Use crontab to launch PCU at boot

```
crontab -e
```

Add commands at the end of the cron file and save

```
@reboot cd /home/pi/pcu && python3 -m pipenv run db_init > /home/pi/log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run adc > /home/pi/log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run serve > /home/pi/log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run logger > /home/pi/log.txt
```

Add ethernet bridge boot commands at the end of /etc/network/interfaces

```
auto br0
iface br0 inet dhcp
bridge_ports eth0 eth1
```


## Interface
TODO

description

image

## API

TODO

description/commands

## Hardware
TODO
description/list