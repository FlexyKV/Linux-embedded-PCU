import json
from datetime import datetime


def port_measure_mapper(measures: list) -> json:
    datetimes = list(map(lambda dt: datetime_to_str(dt), measures[0]))
    currents = measures[1]
    voltages = measures[2]
    powers = [current * voltage for current, voltage in zip(currents, voltages)]
    port_states = list(map(lambda ps: (datetime_to_str(ps[0]), ps[1]), measures[3]))

    """find total number of seconds in time range to identify seconds not found, handle in javascript ?"""
    # time = (end_time - start_time).total_seconds()

    port_measures = {"datetime": datetimes, "current": currents, "voltage": voltages,
                     "power": powers, "port_states": port_states}

    return json.dumps(port_measures)


def port_state_mapper(port_id: int, state: int) -> json:
    port_state = {"port_id": port_id, "port_state": state}
    return json.dumps(port_state)


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')


def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


