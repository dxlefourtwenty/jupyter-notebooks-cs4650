
import re
import json

from mrjob.job import MRJob

QUALITY_RE = re.compile(r"[01459]")

class WindDirection(MRJob):

    def mapper(self, _, line):
        val = line.strip()
        (direction, temp, q) = (val[60:63], val[87:92], val[63:64])
        if (direction != "999" and re.match(QUALITY_RE, q)):
            yield direction, temp

    def reducer(self, key, values):
        count = 0
        high = None
        low = None

        for v in values:
            temp = int(v)

            count += 1

            if high is None or temp > high:
                high = temp

            if low is None or temp < low:
                low = temp

        yield int(key), {"low": low, "high": high, "count": count}

if __name__ == '__main__':
    WindDirection.run()
