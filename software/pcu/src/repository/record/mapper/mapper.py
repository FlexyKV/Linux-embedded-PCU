import json
from datetime import datetime
from operator import itemgetter


def map_measures(record_datetime, record_port_states, measures, return_period):
    """
    map record to period and extract min, max, average and port state changes
    """
    record_length = len(record_datetime)
    period_seconds, record_current, record_voltage, record_power = 0, 0, 0, 0
    period_port_states = [(record_datetime[0], record_port_states[0])]
    period_datetimes = []
    currents = []
    voltages = []
    powers = []

    for record_index in range(record_length):
        period_seconds += 1
        record_current += measures[record_index][0]
        record_voltage += measures[record_index][1]
        record_power += measures[record_index][2]

        if record_port_states[record_index] != period_port_states[-1][1]:
            period_port_states.append((record_datetime[record_index], record_port_states[record_index]))

        if period_seconds == return_period or record_index == record_length - 1:
            period_datetimes.append(datetime_to_str(record_datetime[record_index - period_seconds + 1]))
            currents.append(record_current / period_seconds)
            voltages.append(record_voltage / period_seconds)
            powers.append(record_power / period_seconds)
            period_seconds, record_current, record_voltage, record_power = 0, 0, 0, 0

    max_measures = (max(measures, key=itemgetter(0))[0], max(measures, key=itemgetter(1))[1],
                    max(measures, key=itemgetter(2))[2])
    min_measures = (min(measures, key=itemgetter(0))[0], min(measures, key=itemgetter(1))[1],
                    min(measures, key=itemgetter(2))[2])
    avg_measures = (sum(currents) / len(currents), sum(voltages) / len(voltages), sum(powers) / len(powers))

    measure_records = [list(zip(period_datetimes, list(zip(currents, voltages, powers)))),
                       avg_measures, max_measures, min_measures,
                       period_port_states]
    return measure_records


def parse_records_to_json(measures_info: list) -> json:

    # measure datetime data
    measures_datetime_dict = {}
    for measure_datetime, measure in measures_info[0]:
        measure_dict = {"current": measure[0], "voltage": measure[1], "power": measure[2]}
        measures_datetime_dict[measure_datetime] = measure_dict

    # measure avg, min, max, data
    avg_measures_dict = {"current": measures_info[1][0], "voltage": measures_info[1][1], "power": measures_info[1][2]}
    max_measures_dict = {"current": measures_info[2][0], "voltage": measures_info[2][1], "power": measures_info[2][2]}
    min_measures_dict = {"current": measures_info[3][0], "voltage": measures_info[3][1], "power": measures_info[3][2]}

    # port state changes
    port_states = list(map(lambda ps: (datetime_to_str(ps[0]), ps[1]), measures_info[4]))

    port_measures = {"measures": measures_datetime_dict, "avg_measure": avg_measures_dict,
                     "max_measure": max_measures_dict, "min_measure": min_measures_dict,
                     "port_states": port_states}
    return json.dumps(port_measures)


def parse_instant_record_to_json(record_datetime, record_port_states, measures):
    instant_measures = {"datetime": datetime_to_str(record_datetime),
                        "port_0": {"port_state": record_port_states[0], "port_current": measures[0][0],
                                   "port_voltage": measures[0][1], "port_power": measures[0][2]},
                        "port_1": {"port_state": record_port_states[1], "port_current": measures[1][0],
                                   "port_voltage": measures[1][1], "port_power": measures[1][2]},
                        "port_2": {"port_state": record_port_states[2], "port_current": measures[2][0],
                                   "port_voltage": measures[2][1], "port_power": measures[2][2]},
                        "port_3": {"port_state": record_port_states[3], "port_current": measures[3][0],
                                   "port_voltage": measures[3][1], "port_power": measures[3][2]},
                        "port_4": {"port_state": record_port_states[4], "port_current": measures[4][0],
                                   "port_voltage": measures[4][1], "port_power": measures[4][2]},
                        "port_5": {"port_state": record_port_states[5], "port_current": measures[5][0],
                                   "port_voltage": measures[5][1], "port_power": measures[5][2]},
                        "port_6": {"port_state": record_port_states[6], "port_current": measures[6][0],
                                   "port_voltage": measures[6][1], "port_power": measures[6][2]},
                        "port_7": {"port_state": record_port_states[7], "port_current": measures[7][0],
                                   "port_voltage": measures[7][1], "port_power": measures[7][2]}}
    return json.dumps(instant_measures)


def parse_port_state_to_json(port_id: int, state: int) -> json:
    port_state = {"port_id": port_id, "port_state": state}
    return json.dumps(port_state)


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')


def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

