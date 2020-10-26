#! /usr/bin/env python3

"""
Sometimes you'll hear people talking about memory leaks and memory efficient programs. 
How is memory connected to program runtime? There is data in a program. Numbers, 
lists, objects, et cetera. These are stored in the computer memory, known as the heap. 
Every time we create a new object, we need to allocate storage for it and this 
operation takes time. This is one reason for why we care about memory allocation. 

Another reason is that accessing memory in modern computers is done in layers. We have 
the CPU, and then we have L1 and L2 caches. Then we have the memory. And the access 
times are very different. Accessing layer 1 cache is about 0.5 ns, while accessing the 
main memory is 100 ns. Every time we try to access a piece of data, the CPU will first 
try to fetch from the cache, then from main memory. Difference, also known as latency, 
is huge. If we keep our data small, there's a good chance it will fit inside the cache 
line, and then it will be much faster to access.

Sometimes algorithms that seem faster on paper are much slower than dumb cache friendly 
or sometimes known as cache oblivious algorithms. 

The last reason is that modern operating systems give us the appearance of having 
infinite memory. The computer I use right now has 16 GB of memory, but programs can 
use much more than that. This is done by swapping some section of memory into the 
hard drive. When we try to access the section memory that is currently swapped to 
disk, the operating system will pick another section of memory, will write to the 
disk, and then load the section memory we require into actual memory. 

This is also known as a page fault, and it's very costly operation. Hardware latency, 
even solid-state one, is order of magnitude slower than memory. All of this means we'd 
like to keep our memory small so we don't cause page faults. 

I hope you're convinced that you need to profile and monitor your memory as well. 
Tracemalloc is a library that was added in Python 3.4 as a tool to understand memory 
allocations. 

"""

import tracemalloc
from tempfile import NamedTemporaryFile
from datetime import datetime
from collections import namedtuple
from itertools import cycle, islice

Event = namedtuple("Event", ["type", "time", "user", "url", "site"])


class EncodeError(Exception):
    pass


class Encoder:
    """Event encoder"""

    def __init__(self, stream):
        self.stream = stream
        self._fields = {
            "click": ["time", "user"],
            "view": ["time", "user", "url"],
            "enter": ["user", "url", "site"],
        }

    def encode(self, event):
        """Encode event to stream"""
        fields = self._fields.get(event.type)

        # If the fields is None/Empty => evaluates to not (False)
        # raise and Exception
        if not fields:
            raise EncodeError("unknown event type: {}".format(event.type))

        self.stream.write("{}".format(len(fields)))
        for field in fields:
            value = getattr(event, field)
            if isinstance(value, datetime):
                value = value.isoformat()
            self.stream.write("|{}={}".format(field, value))
        stream.write("\n")


def encode_event(event, stream):
    """Encode event to stream"""
    enc = Encoder(stream)
    return enc.encode(event)


if __name__ == "__main__":
    # Generate test cases
    events = []
    for typ in ("click", "view", "enter"):
        events.append(Event(typ, datetime.now(), "bugs", "/buy/carrot", "acme.com"))

    # https://docs.python.org/3.9/library/itertools.html
    # https://docs.python.org/3.9/library/itertools.html#itertools.cycle
    # https://docs.python.org/3.9/library/itertools.html#itertools.islice
    # cycle generates and infinite generator and islice extracts the
    # first 1000 events from the infinite generator
    events = islice(cycle(events), 10)

    # # https://docs.python.org/3/library/tempfile.html
    # # https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
    stream = NamedTemporaryFile(mode="wt", delete=False)
    print("encoding to {}".format(stream.name))

    # https://docs.python.org/3/library/tracemalloc.html
    tracemalloc.start()

    for event in events:
        encode_event(event, stream)

    # https://docs.python.org/3/library/tracemalloc.html#tracemalloc.take_snapshot
    snapshot = tracemalloc.take_snapshot()

    # https://docs.python.org/3/library/tracemalloc.html#tracemalloc.take_snapshot
    for stat in snapshot.statistics("lineno")[:10]:
        print(stat)

