
import json

from mrjob.job import MRJob

class partOne(MRJob):

    def mapper(self, _, line):
        val = line.strip()
        (column, row, value) = (val[:1], val[2:3], val[4:])
        yield ("COL", column), value
        yield ("ROW", row), value

    def reducer(self, key, values):
        kind, label = key        

        if kind == "COL":
            yield label, int(max(values))
        else:
            yield label, int(min(values))

if __name__ == '__main__':
    partOne.run()
