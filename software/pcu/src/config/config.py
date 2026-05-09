import configparser
import json
import os

from src.repository.database_client.database_client import CONFIG_FILE_PATH, memory_type


def _read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config


def _write_config(section: str, key: str, value: str):
    config = _read_config()
    config.set(section, key, value)
    with open(CONFIG_FILE_PATH, "w") as configfile:
        config.write(configfile)
    return json.dumps({"status": 200})


def get_login_password():
    return _read_config()["APP"].get("password")


def set_memory_type(mem_type):
    if mem_type not in (memory_type.ram.name, memory_type.sd.name):
        return json.dumps({"error": "invalid database memory type"})
    return _write_config("DATABASE", "record_memory_type", mem_type)


def set_reference_voltage(v_ref):
    return _write_config("ADC", "reference_voltage", v_ref)


def set_login_password(password):
    return _write_config("APP", "password", password)


def set_log_ip(log_server_ip):
    return _write_config("APP", "log_server_ip", log_server_ip)


def set_log_port(log_server_port):
    return _write_config("APP", "log_server_port", log_server_port)


def reboot_pcu():
    os.system("sudo reboot &")
    return json.dumps({"status": 200})


def get_ip():
    ip = os.popen("hostname -I | awk '{print $1}'").read()
    return json.dumps({"status": 200, "ip": ip})
