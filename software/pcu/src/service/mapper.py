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
        self.missing_dt_records = []
        self.period_seconds, self.record_current, self.record_voltage, self.missing_records = 0, 0, 0, 0

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

    def __verify_port_state_change(self, index):
        if self.record_port_states[index] != self.period_port_states[-1][1]:
            self.period_port_states.append((self.record_datetime[index], self.record_port_states[index]))

    def __append_periodic_measures(self, index):
        self.period_datetimes.append(self.record_datetime[index - self.period_seconds + 1])
        self.currents.append(self.record_current / self.period_seconds)
        self.voltages.append(self.record_voltage / self.period_seconds)
        self.period_seconds, self.record_current, self.record_voltage = 0, 0, 0

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
        measure_records = [self.period_datetimes, self.currents, self.voltages, self.period_port_states,
                           self.missing_dt_records]
        return measure_records


def parse_record_to_json(measures_info: list) -> json:
    datetimes = list(map(lambda dt: datetime_to_str(dt), measures_info[0]))
    currents = measures_info[1]
    voltages = measures_info[2]
    powers = [current * voltage for current, voltage in zip(currents, voltages)]
    port_states = list(map(lambda ps: (datetime_to_str(ps[0]), ps[1]), measures_info[3]))
    missing_records = list(map(lambda missing_dt: (datetime_to_str(missing_dt[0]),
                                                   datetime_to_str(missing_dt[1])), measures_info[4]))

    port_measures = {"datetime": datetimes, "current": currents, "voltage": voltages,
                     "power": powers, "port_states": port_states, "missing_datetime": missing_records}

    return json.dumps(port_measures)


def parse_port_state_to_json(port_id: int, state: int) -> json:
    port_state = {"port_id": port_id, "port_state": state}
    return json.dumps(port_state)


def str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
