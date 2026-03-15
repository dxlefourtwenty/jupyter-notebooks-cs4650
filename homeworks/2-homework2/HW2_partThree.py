
import json

from mrjob.job import MRJob

class partThree(MRJob):

    def mapper(self, _, line):
        val = line.strip()
        (column, row, value) = (val[:1], val[2:3], val[4:]) 
        yield ("COL", column), {"row": row, "val": value}
        yield ("ROW", row), {"col": column, "val": value}

    def reducer(self, key, values):
        kind, label = key

        best_value = None
        best_locations = []

        for v in values:
            value = int(v["val"]) # initialize value
            location = v.get("row") or v.get("col")

            if best_value is None:
                best_value = value
                best_locations = [location]

            else:
                if kind == "COL":
                    if value > best_value:
                        best_value = value
                        best_locations = [location]
                    elif value == best_value:
                        best_locations.append(location) # append if they have the same value

                else:
                    if value < best_value:
                        best_value = value
                        best_locations = [location]
                    elif value == best_value:
                        best_locations.append(location) # append if they have the same value

        yield label, {"value": best_value, "examples": best_locations}

if __name__ == '__main__':
    partThree.run()
