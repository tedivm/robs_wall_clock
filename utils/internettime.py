import time

import rtc

from utils.memory import gc_decorator


def _timestruct_to_seconds(ts):
    seconds = 0
    seconds += ts.tm_sec
    seconds += ts.tm_min * 60
    seconds += ts.tm_hour * 3600
    seconds += ts.tm_mday * 86400
    seconds += ts.tm_mon * 2592000
    seconds += (ts.tm_year - 1970) * 31536000
    return seconds


class InternetTime:
    def __init__(
        self,
        network,
        timezone_name="America/Chicago",
        seconds_between_updates=300,
        disable_internet=False,
        debug=False,
    ):
        self.timezone_name = timezone_name
        self.seconds_between_updates = seconds_between_updates
        self.network = network
        self.debug = debug
        self.utc_offset_hours = 0
        self.utc_offset_minutes = 0
        self.disable_internet = disable_internet

    @gc_decorator
    def get_time(self):

        try:
            if not hasattr(self, "_last_update_attempt"):
                self._update_time_data_rate_limited()

            now = _timestruct_to_seconds(rtc.RTC().datetime)
            if now - self._last_update_attempt > self.seconds_between_updates:
                self._update_time_data_rate_limited()
        except Exception as e:
            print(e)
            print("InternetTime: Could not update system time")

        ts = rtc.RTC().datetime
        current_hour = ts.tm_hour + self.utc_offset_hours
        current_min = ts.tm_min + self.utc_offset_minutes
        if current_min >= 60:
            current_hour += 1
            current_min -= 60
        current_hour = current_hour % 24

        return time.struct_time(
            (
                ts.tm_year,
                ts.tm_mon,
                ts.tm_mday,
                current_hour,
                current_min % 60,
                ts.tm_sec,
                ts.tm_wday,
                ts.tm_yday,
                -1,
            )
        )

    def time_string(self, format="12"):
        current_time = self.get_time()
        if format == "24":
            hour = f"{current_time.tm_hour:02}"
        else:
            hour = f"{current_time.tm_hour % 12:02}"

        return f"{hour:02}:{current_time.tm_min:02}"

    def _update_time_data_rate_limited(self):
        now = _timestruct_to_seconds(rtc.RTC().datetime)
        if hasattr(self, "_last_update_attempt"):
            if now - self._last_update_attempt > 300:
                return

        self._last_update_attempt = now
        self._update_time_data()
        now = _timestruct_to_seconds(rtc.RTC().datetime)
        self._last_update_attempt = now
        self._last_successful_update = now

    def _update_time_data(self):
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

        self.start_timestamp = data["unixtime"]
        self.utc_offset = data["utc_offset"]
        self.utc_offset_sign = "-" if self.utc_offset[0] == "-" else ""

        split_offset = self.utc_offset.split(":")
        self.utc_offset_hours = int(f"{split_offset[0]}")
        self.utc_offset_minutes = int(f"{self.utc_offset_sign}{split_offset[1]}")

        now = time.localtime(data["unixtime"])
        self.timestamp_retrieved = now
        rtc.RTC().datetime = now

        return True
