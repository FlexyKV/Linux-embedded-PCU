import json
from datetime import datetime


# missing min and max of period
class MeasureMapper:
    def __init__(self, record_datetime, record_port_states, measures, return_period, start_time, end_time):
        self.record_datetime = record_datetime
        self.record_port_states = record_port_states
        self.measures = measures
        self.return_period = return_period
        self.start_time = start_time
        self.end_time = end_time
        self.period_port_states = [(record_datetime[0], record_port_states[0])]
        self.period_datetimes = []
        self.currents = []
        self.voltages = []
        self.powers = []
        self.missing_dt_records = []
        self.period_seconds, self.record_current, self.record_voltage, self.record_power, self.missing_records \
            = 0, 0, 0, 0, 0
        self.max_measures = ()
        self.min_measures = ()
        self.avg_measures = ()

    def __verify_start_time_record(self):
        start_timedelta = self.record_datetime[0] - self.start_time
        if start_timedelta.total_seconds() > 1.5:
            self.missing_dt_records.append((self.start_time, self.record_datetime[0]))

    def __verify_end_time_record(self):
        end_timedelta = self.end_time - self.record_datetime[-1]
        if end_timedelta.total_seconds() > 1.5:
            self.missing_dt_records.append((self.record_datetime[-1], self.end_time))

    def __add_record_measures_to_period(self, index):
        self.record_current += self.measures[index][0]
        self.record_voltage += self.measures[index][1]
        self.record_power += self.measures[index][2]

    def __verify_port_state_change(self, index):
        if self.record_port_states[index] != self.period_port_states[-1][1]:
            self.period_port_states.append((self.record_datetime[index], self.record_port_states[index]))

    def __append_periodic_measures(self, index):
        self.period_datetimes.append(datetime_to_str(self.record_datetime[index - self.period_seconds + 1]))
        self.currents.append(self.record_current / self.period_seconds)
        self.voltages.append(self.record_voltage / self.period_seconds)
        self.powers.append(self.record_power / self.period_seconds)
        self.period_seconds, self.record_current, self.record_voltage, self.record_power, self.missing_records \
            = 0, 0, 0, 0, 0

    def __calculate_max_min_avg(self, currents, voltages, powers):
        # TODO take min and max from all data not period data
        self.max_measures = (max(currents), max(voltages), max(powers))
        self.min_measures = (min(currents), min(voltages), min(powers))
        self.avg_measures = (sum(currents) / len(currents), sum(voltages) / len(voltages), sum(powers) / len(powers))

    def map_measures(self):
        record_length = len(self.record_datetime)
        self.__verify_start_time_record()
        for record_index in range(record_length):
            self.period_seconds += 1
            self.__add_record_measures_to_period(record_index)
            self.__verify_port_state_change(record_index)

            # if this is not the last record in the record, calculate number of seconds until next record
            if record_index != record_length - 1:
                record_timedelta = self.record_datetime[record_index + 1] - self.record_datetime[record_index]
                # if next record > 1.5 second, set as missing record
                if record_timedelta.total_seconds() > 1.5:
                    self.missing_dt_records.append((self.record_datetime[record_index],
                                                    self.record_datetime[record_index + 1]))

                    # append measure avg as finished period even if it is shorter (is there a better way?)
                    self.__append_periodic_measures(record_index)
                    continue
            if self.period_seconds == self.return_period or record_index == record_length - 1:
                self.__append_periodic_measures(record_index)

        self.__verify_end_time_record()

        self.__calculate_max_min_avg(self.currents, self.voltages, self.powers)

        measure_records = [list(zip(self.period_datetimes, list(zip(self.currents, self.voltages, self.powers)))),
                           self.avg_measures, self.max_measures, self.min_measures,
                           self.period_port_states, self.missing_dt_records]
        return measure_records


def parse_record_to_json(measures_info: list) -> json:

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

    # missing records
    missing_records = list(map(lambda missing_dt: (datetime_to_str(missing_dt[0]),
                                                   datetime_to_str(missing_dt[1])), measures_info[5]))

    port_measures = {"measures": measures_datetime_dict, "avg_measure": avg_measures_dict,
                     "max_measure": max_measures_dict, "min_measure": min_measures_dict,
                     "port_states": port_states, "missing_datetimes": missing_records}
    return json.dumps(port_measures)


def parse_port_state_to_json(port_id: int, state: int) -> json:
    port_state = {"port_id": port_id, "port_state": state}
    return json.dumps(port_state)


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')


def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


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



