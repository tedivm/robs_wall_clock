import time

import rtc
from adafruit_datetime import datetime, timedelta
from utils.memory import gc_decorator

def _datetime_to_timestruct(dt):
    return time.struct_time(
        (
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.weekday(),
            dt.timetuple().tm_yday,
            -1,
        )
    )

def _timestruct_to_datetime(ts):
    return datetime(
        ts.tm_year,
        ts.tm_mon,
        ts.tm_mday,
        ts.tm_hour,
        ts.tm_min,
        ts.tm_sec,
    )


class InternetTime:
    def __init__(
        self,
        network,
        timezone_name="America/Chicago",
        seconds_between_updates=300,
        debug=False,
    ):
        self.timezone_name = timezone_name
        self.seconds_between_updates = seconds_between_updates
        self.network = network
        self.debug = debug
        self.utc_offset_hours = 0
        self.utc_offset_minutes = 0

    @gc_decorator
    def get_time(self):
        if not hasattr(self, "last_system_update"):
            self._update_system_time()

        try:
            now = _timestruct_to_datetime(rtc.RTC().datetime)
            if now - self.last_system_update_attempt > timedelta(
                seconds=self.seconds_between_updates
            ):
                self._update_system_time()
        except Exception as e:
            print(e)
            print("InternetTime: Could not update system time")

        utc = _timestruct_to_datetime(rtc.RTC().datetime)
        adjusted_time = utc + timedelta(
            hours=self.utc_offset_hours, minutes=self.utc_offset_minutes
        )

        return adjusted_time

    def time_string(self, format="24"):
        current_time = self.get_time()
        return f"{current_time.hour:02}:{current_time.minute:02}"

    def _update_timezone_data(self):
        if self.debug:
            print("InternetTime: Fetching new time from server.")

        try:
            response = self.network.fetch(
                f"http://worldtimeapi.org/api/timezone/{self.timezone_name}"
            )
        except:
            print("InternetTime Error: Could not fetch time from server.")
            raise

        data = response.json()

        self.timestamp_retrieved = self._get_ticks()
        self.start_timestamp = data["unixtime"]
        self.utc_offset = data["utc_offset"]
        self.utc_offset_sign = "-" if self.utc_offset[0] == "-" else ""

        split_offset = self.utc_offset.split(":")
        self.utc_offset_hours = int(f"{split_offset[0]}")
        self.utc_offset_minutes = int(f"{self.utc_offset_sign}{split_offset[1]}")

        return True

    def _update_system_time(self):
        # If the update fails we use the current clock to record the update attempt.
        self.last_system_update_attempt = _timestruct_to_datetime(rtc.RTC().datetime)

        if self.debug:
            print("Updating from Internet.")
        rtc.RTC().datetime = self._get_internet_time()

        self.last_system_update = _timestruct_to_datetime(rtc.RTC().datetime)

        # Since the update did not fail, and the clock may have shifted, update the attempt time.
        self.last_system_update_attempt = self.last_system_update

    def _get_internet_time(self):
        if not hasattr(self, "start_timestamp"):
            if not self._update_timezone_data():
                raise Exception("InternetTime: Could not update timezone data.")

        current_tick = self._get_ticks()
        tick_diff = current_tick - self.timestamp_retrieved

        if self.debug:
            print(f"InternetTime: Tick diff: {tick_diff}")
            print(f"InternetTime: retrieved tick: {self.timestamp_retrieved}")
            print(f"InternetTime: current_tick: {current_tick}")
            print(f"InternetTime: Timestamp retrieved: {self.timestamp_retrieved}")

        if tick_diff > self.seconds_between_updates:
            self._update_timezone_data()
            tick_diff = int(current_tick - self.timestamp_retrieved)

        # Start with the internet loaded time.
        formatted_time = datetime.fromtimestamp(self.start_timestamp)
        # Add the difference in seconds to the internet loaded time.
        tick_adjusted = formatted_time + timedelta(seconds=int(tick_diff))

        return _datetime_to_timestruct(tick_adjusted)

    def _get_ticks(self):
        return time.time()
