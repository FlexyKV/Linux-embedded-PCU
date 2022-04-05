import configparser
import json
import os

from src.repository.database_client.database_client import memory_type, CONFIG_FILE_PATH


def get_login_password():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    login_password = config["APP"].get("password")
    return login_password


def set_memory_type(mem_type):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    if mem_type != memory_type.ram.name and mem_type != memory_type.sd.name:
        return json.dumps({"error": "invalid database memory type"})
    config.set("DATABASE", "record_memory_type", mem_type)
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def set_reference_voltage(v_ref):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set("ADC", "reference_voltage", v_ref)
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def set_login_password(password):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set("APP", "password", password)
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def set_log_ip(log_server_ip):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set("APP", "log_server_ip", log_server_ip)
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def set_log_port(log_server_port):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set("APP", "log_server_port", log_server_port)
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def reboot_pcu():
    os.system("sudo reboot &")
    return json.dumps({"status": 200})
