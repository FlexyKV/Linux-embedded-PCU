import json
from datetime import datetime


def port_measure_mapper(measures: list) -> json:
    timestamp = list(map(lambda dt: datetime_to_str(dt[0]), measures))
    currents = list(map(lambda current: current[1][0], measures))
    voltages = list(map(lambda voltage: voltage[1][1], measures))
    powers = list(map(lambda power: power[1][0] * power[1][1], measures))

    """find total number of seconds in time range to identify seconds not found, handle in javascript ?"""
    # time = (end_time - start_time).total_seconds()

    port_measures = {"timestamp": timestamp, "current": currents, "voltage": voltages, "power": powers}

    return json.dumps(port_measures)


def port_state_mapper(port_id: int, state: int) -> json:
    port_state = {"port_id": port_id, "port_state": state}
    return json.dumps(port_state)


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')


def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


