class Time(object):
    """Represents the time of day.
    attributes: minute, second
    """
    def __init__(self, hour=0, minute=0, second=0, mili=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.mili = mili

    def __repr__(self) -> str:
        # return f"{self.hour}:{self.minute}:{self.second}:{self.mili}" #what it should be
        return f"{self.minute:02f}:{self.second:02f}" #what we need

    def time_to_int(self, time):
        minute = time.hour * 60 + time.minute
        second = minute * 60 + time.second
        return second
    
    def int_to_time(self, seconds):
        time = Time()
        minutes, time.second = divmod(seconds, 60)
        time.hour, time.minute = divmod(minutes, 60)
        return time

    def subtract_time(self, t2, t1):
        seconds = self.time_to_int(t2) - self.time_to_int(t1)
        return self.int_to_time(seconds)

if __name__ == '__main__':
    t3 = Time()
    # diff = t3.subtract_time(Time(second=893), Time(second=959))
    diff = t3.subtract_time(Time(second=61), Time(second=0))
    print(diff)
