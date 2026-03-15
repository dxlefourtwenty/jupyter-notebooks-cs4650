import json

from mrjob.job import MRJob

class partTwo(MRJob):

    def mapper(self, _, line):
        val = line.strip()
        (column, row, value) = (val[:1], val[2:3], val[4:]) 
        yield ("COL", column), {"row":row, "val":int(value)}
        yield ("ROW", row), {"column":column, "val":int(value)}

    def reducer(self, key, values):
        kind, label = key

        best_value = None
        best_location = None

        for v in values:
            value = v["val"]

            if best_value is None:
                best_value = value
                best_location = v.get("row") or v.get("column")

            else:
                if kind == "COL" and value > best_value:
                    best_value = value
                    best_location = v.get("row") or v.get("column")
                elif kind == "ROW" and value < best_value: 
                    best_value = value
                    best_location = v.get("row") or v.get("column")
        
        yield label, {"value": best_value, "example": best_location}


if __name__ == '__main__':
    partTwo.run()
