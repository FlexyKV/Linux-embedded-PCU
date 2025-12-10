# Linux Embedded Power Control Unit (PCU) ⚡

> **University Capstone Project**
>
> Open Source Linux embedded power control unit with Python API and UI for convivial control and monitoring.
# Linux Embedded Power Control Unit (PCU)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg) ![License](https://img.shields.io/badge/License-Open%20Source-green.svg)

**Open Source Linux embedded power control unit with Python API.**

This project is a comprehensive solution for controlling power outlets and monitoring power consumption via a Raspberry Pi. It features a custom hardware interface, a robust Python backend, and a RESTful API designed for reliability and ease of use in embedded environments.

## 📋 Features

* **Smart Control**: Independent toggle of 8 relays via GPIO.
* **Real-time Monitoring**: Voltage, current, and power measurement via MCP3008 ADC.
* **REST API**: Full programmatic control using Flask and JWT authentication.
* **System Optimization**: Implements RAM Disk storage for high-frequency logs to prevent SD card corruption.
* **Automated Services**: Self-healing background services managed via Cron and Pipenv.

---

## 🛠 Installation Guide

Follow these steps to set up the Power Control Unit from a fresh Raspberry Pi installation.

### 1. OS Preparation
1.  Use **Raspberry Pi Imager** to write **Raspbian Lite OS** on your SD card.
2.  Connect the Pi to a screen and keyboard for initial setup.

### 2. Raspbian Configuration
**Update System:**
```
sudo apt-get update sudo apt-get upgrade
```
**Run the config tool:**
```
sudo raspi-config
```
System Options: Set a new password and the PCU hostname.

Interface Options: Enable SPI and SSH.

Localisation: Set local system time (critical for logs).

Reboot: Restart the system.

### 3. Install Dependencies
**Install Python pip, network utils, and bridge-utils:**
```
sudo apt-get install python3-pip bridge-utils pip3 install pipenv
```
### 4. Mount a RAM Partition (Optimization)
To prevent SD card wear from frequent log writes, create a temporary RAM disk.

**Create directory:**
```
mkdir /var/tmp
```
**Edit fstab:**
```
sudo nano /etc/fstab
```
**Add this line to the end of the file (400MB RAM Disk):**
```
tmpfs /var/tmp tmpfs nodev,nosuid,size=400M 0 0
```
**Mount the disk:**
```
sudo mount -a
```
### 5. Sync PCU Files
**Clone the repository or copy files via SCP.**

For Windows (using SCP):
```
Replace {hostname} with your specific Pi hostname
scp -prq software/pcu pi@{hostname}.local:/home/pi
```
**Setup Python Environment:**
```
cd pcu python3 -m pipenv install
```
### 6. Setup Auto-Launch
**Use cron to launch PCU services at boot.**
```
crontab -e
```
**Add these commands at the end of the file:**
```
@reboot cd /home/pi/pcu && python3 -m pipenv run init_gpio > /home/pi/gpio_log.txt @reboot cd /home/pi/pcu && python3 -m pipenv run adc > /home/pi/adc_log.txt @reboot cd /home/pi/pcu && python3 -m pipenv run serve > /home/pi/serve_log.txt @reboot cd /home/pi/pcu && python3 -m pipenv run logger > /home/pi/logger_log.txt
```
### 7. Network Bridge
**Add ethernet bridge configuration to the end of /etc/network/interfaces:**
```
auto br0 iface br0 inet dhcp bridge_ports eth0 eth1
```
🔌 Hardware Documentation
For pinout tables and PCB schematics, refer to: 👉 [Hardware Pinout](https://www.google.com/search?q=hardware/pinout.md)

📡 API Documentation
For full API command references (Config, Port control, Records): 👉 [API Documentation](https://www.google.com/search?q=software/API.md)
