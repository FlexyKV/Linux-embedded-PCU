# Linux Embedded Power Control Unit (PCU)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)
![License](https://img.shields.io/badge/License-Open%20Source-green.svg)

> **University Capstone Project** — Open source Linux embedded power control unit with a Python REST API for control and monitoring.

This project is a comprehensive solution for controlling power outlets and monitoring power consumption via a Raspberry Pi. It features a custom hardware interface, a Python backend, and a RESTful API designed for reliability and ease of use in embedded environments.

## Features

- **Smart Control** — independent toggle of 8 relays via GPIO.
- **Real-time Monitoring** — voltage, current, and power measurement via MCP3008 ADC.
- **REST API** — full programmatic control using Flask and JWT authentication.
- **System Optimization** — RAM disk storage for high-frequency logs to prevent SD card corruption.
- **Automated Services** — self-healing background services managed via cron and Pipenv.

---

## Installation Guide

Follow these steps to set up the Power Control Unit from a fresh Raspberry Pi installation.

### 1. OS Preparation

1. Use **Raspberry Pi Imager** to write **Raspbian Lite OS** on your SD card.
2. Connect the Pi to a screen and keyboard for initial setup.

### 2. Raspbian Configuration

Update the system:

```sh
sudo apt-get update
sudo apt-get upgrade
```

Run the config tool:

```sh
sudo raspi-config
```

- **System Options** — set a new password and the PCU hostname.
- **Interface Options** — enable SPI and SSH.
- **Localisation** — set local system time (critical for logs).
- **Reboot** — restart the system.

### 3. Install Dependencies

Install Python pip, network utils, and bridge-utils:

```sh
sudo apt-get install python3-pip bridge-utils
pip3 install pipenv
```

### 4. Mount a RAM Partition (Optimization)

To prevent SD card wear from frequent log writes, create a temporary RAM disk.

Create the directory:

```sh
mkdir /var/tmp
```

Edit fstab:

```sh
sudo nano /etc/fstab
```

Add this line at the end (400MB RAM disk):

```
tmpfs /var/tmp tmpfs nodev,nosuid,size=400M 0 0
```

Mount the disk:

```sh
sudo mount -a
```

### 5. Sync PCU Files

Clone the repository or copy files via SCP. For Windows (using SCP), replace `{hostname}` with your Pi hostname:

```sh
scp -prq software/pcu pi@{hostname}.local:/home/pi
```

Set up the Python environment:

```sh
cd pcu
python3 -m pipenv install
```

### 6. Setup Auto-Launch

Use cron to launch PCU services at boot:

```sh
crontab -e
```

Add these commands at the end of the file:

```
@reboot cd /home/pi/pcu && python3 -m pipenv run init_gpio > /home/pi/gpio_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run adc      > /home/pi/adc_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run serve    > /home/pi/serve_log.txt
@reboot cd /home/pi/pcu && python3 -m pipenv run logger   > /home/pi/logger_log.txt
```

### 7. Network Bridge

Add ethernet bridge configuration to the end of `/etc/network/interfaces`:

```
auto br0
iface br0 inet dhcp
    bridge_ports eth0 eth1
```

---

## Documentation

- **Hardware** — [Hardware Pinout](https://github.com/FlexyKV/Linux-embedded-PCU/blob/main/hardware/pinout.md)
- **API** — [API Documentation](https://github.com/FlexyKV/Linux-embedded-PCU/blob/main/software/API.md)
