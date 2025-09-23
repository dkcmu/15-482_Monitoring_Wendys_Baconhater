from monitor import *
from terrabot_utils import clock_time

class LoggingMonitor(Monitor):

    def __init__(self, period=10):
        super(LoggingMonitor, self).__init__("LoggingMonitor", period)
        # Put any iniitialization code here
        # BEGIN STUDENT CODE
        self.normal_sensors = ['unix_time',
            'light', 'temp', 'humid', 'weight',
            'smoist', 'level', 'level_raw']
        self.array_sensors = ['light_raw', 'temp_raw', 'humid_raw', 'weight_raw' ,'smoist_raw']
        self.actuators = ['fan', 'wpump', 'led', 'camera']

        self.file_name = "monitoring_hw_log.csv"
        headings = self.normal_sensors + [
            'light_raw_1', 'light_raw_2',
            'temp_raw_1', 'temp_raw_2',
            'humid_raw_1', 'humid_raw_2',
            'weight_raw_1', 'weight_raw_2',
            'smoist_raw_1', 'smoist_raw_2'
        ] + self.actuators

        # Open new Log File
        with open(self.file_name, "w") as file:
            file.write(",".join(headings) + '\n')
        # END STUDENT CODE

    def perceive(self):
        # BEGIN STUDENT CODE
        self.normal_sensor_data = {sensor:self.sensordata[sensor] for sensor in self.normal_sensors}
        self.array_sensor_data = {sensor:self.sensordata[sensor] for sensor in self.array_sensors}
        # END STUDENT CODE
        pass

    def monitor(self):
        # Use self.sensorData and self.actuator_state to log the sensor and
        #  actuator data, preferably as a comma-separated line of values.
        #  Make sure to timestamp the line of data
        # BEGIN STUDENT CODE
        print(f"Current Time: {clock_time(self.normal_sensor_data['unix_time'])}")

        sensor_log_data = [str(value) for value in self.normal_sensor_data.values()]
        for data in self.array_sensor_data.values():
            sensor_log_data.append(str(data[0]))
            sensor_log_data.append(str(data[1]))

        actuator_log_data = [str(self.actuator_state[actuator]) for actuator in self.actuators]

        # Write to existing log file
        with open(self.file_name, "a") as file:
            file.write(",".join(sensor_log_data + actuator_log_data) + '\n')
        # END STUDENT CODE
        pass

