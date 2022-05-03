# Linux-embedded-PCU
Open Source Linux embedded power control unit with python API and UI for convivial control and monitoring.

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

change localisation to get local system time

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

### Mount a RAM partition

Create the temporary directory for the RAM Disk
```
mkdir /var/tmp
```

Edit the fstab file using your favourite editor (e.g. nano)

```
sudo nano /etc/fstab
```

Add the following line to /etc/fstab to create a 400MB RAM Disk

```
tmpfs /var/tmp tmpfs nodev,nosuid,size=400M 0 0
```

Execute the following command to mount the newly created RAM Disk

```
sudo mount -a
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
@reboot cd /home/pi/pcu && python3 -m pipenv run init_gpio > /home/pi/gpio_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run adc > /home/pi/adc_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run serve > /home/pi/serve_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run logger > /home/pi/logger_log.txt
```

Add ethernet bridge boot commands at the end of /etc/network/interfaces

```
auto br0
iface br0 inet dhcp
bridge_ports eth0 eth1
```