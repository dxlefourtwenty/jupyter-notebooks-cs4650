
import re
from mrjob.job import MRJob

PUNC_RE = re.compile(r"[^a-z]")

class word_length_count(MRJob):

    def mapper(self, _, line):
        thelist = line.split()
        for x in thelist:
            y = x.lower()
            z = re.sub(PUNC_RE, '', y)
            if len(z) <= 3:
                continue
            yield len(z), z

    def reducer(self, key, values):
        count = 0
        example = ""
        for word in values:
            if len(example) <= 0:
                example = word
            count += 1
        yield key, {"example":example, "count":count}

if __name__ == '__main__':
    word_length_count.run()
