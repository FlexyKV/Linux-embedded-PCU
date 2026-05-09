import json
from datetime import datetime
from operator import itemgetter

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def map_measures(record_datetime, record_port_states, measures, return_period):
    """Aggregate raw records into periods and compute min/max/avg + state changes."""
    record_length = len(record_datetime)
    period_seconds = 0
    record_current = record_voltage = record_power = 0
    period_port_states = [(record_datetime[0], record_port_states[0])]
    period_datetimes = []
    currents = []
    voltages = []
    powers = []

    for i in range(record_length):
        period_seconds += 1
        record_current += measures[i][0]
        record_voltage += measures[i][1]
        record_power += measures[i][2]

        if record_port_states[i] != period_port_states[-1][1]:
            period_port_states.append((record_datetime[i], record_port_states[i]))

        if period_seconds == return_period or i == record_length - 1:
            period_datetimes.append(datetime_to_str(record_datetime[i - period_seconds + 1]))
            currents.append(record_current / period_seconds)
            voltages.append(record_voltage / period_seconds)
            powers.append(record_power / period_seconds)
            period_seconds = 0
            record_current = record_voltage = record_power = 0

    max_measures = (
        max(measures, key=itemgetter(0))[0],
        max(measures, key=itemgetter(1))[1],
        max(measures, key=itemgetter(2))[2],
    )
    min_measures = (
        min(measures, key=itemgetter(0))[0],
        min(measures, key=itemgetter(1))[1],
        min(measures, key=itemgetter(2))[2],
    )
    avg_measures = (
        sum(currents) / len(currents),
        sum(voltages) / len(voltages),
        sum(powers) / len(powers),
    )

    return [
        list(zip(period_datetimes, list(zip(currents, voltages, powers)))),
        avg_measures,
        max_measures,
        min_measures,
        period_port_states,
    ]


def parse_records_to_json(measures_info: list) -> str:
    """Serialise aggregated port records into the API JSON shape."""
    measures_datetime_dict = {
        measure_datetime: {"current": m[0], "voltage": m[1], "power": m[2]}
        for measure_datetime, m in measures_info[0]
    }

    avg, mx, mn = measures_info[1], measures_info[2], measures_info[3]
    avg_measures_dict = {"current": avg[0], "voltage": avg[1], "power": avg[2]}
    max_measures_dict = {"current": mx[0], "voltage": mx[1], "power": mx[2]}
    min_measures_dict = {"current": mn[0], "voltage": mn[1], "power": mn[2]}

    port_states = [(datetime_to_str(ps[0]), ps[1]) for ps in measures_info[4]]

    return json.dumps({
        "measures": measures_datetime_dict,
        "avg_measure": avg_measures_dict,
        "max_measure": max_measures_dict,
        "min_measure": min_measures_dict,
        "port_states": port_states,
    })


def parse_instant_record_to_json(record_datetime, record_port_states, measures):
    """Serialise the latest record + port states for all 8 ports."""
    payload = {"datetime": datetime_to_str(record_datetime)}
    for port_id in range(8):
        payload[f"port_{port_id}"] = {
            "port_state": record_port_states[port_id],
            "port_current": measures[port_id][0],
            "port_voltage": measures[port_id][1],
            "port_power": measures[port_id][2],
        }
    return json.dumps(payload)


def parse_port_state_to_json(port_id: int, state: int) -> str:
    return json.dumps({"port_id": port_id, "port_state": state})


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, DATETIME_FORMAT)


def datetime_to_str(date: datetime) -> str:
    return date.strftime(DATETIME_FORMAT)
