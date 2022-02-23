# Linux-embeded-PCU
Open Source Linux embedder power control unit with python API

## Software

This project has an independent API that controls the PCU and a linked UI for convivial control and monitoring.

### Interface

description

image

### API

description

image

## Hardware

description

### Raspberry Pi 4B

description

image

### USB Ethernet port

description

image

### How to use project

#### On work computer

Connect ssh:

```
ssh pi@pcu.local 
```

Sync file:

```
scp -prq pcu pi@pcu.local:/home/pi
```

#### On Raspberry Pi

Install pipenv:

```
sudo apt-get remove pipenv
pip3 install pipenv
```

Run adc:

```
python3 -m pipenv run adc
```

Run server:

```
python3 -m pipenv run server
```
