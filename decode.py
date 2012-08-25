import sys
sys.path[0] = 'build/lib.linux-i686-2.7'

import io
import os.path
import numpy
import random
import itertools
from selfrepairing import HSRC, HSRCMode

numpy.set_printoptions(linewidth=100)

k = 3
n = 7
w = 32
packetsize = 128
buffsize = w*packetsize
mode = HSRCMode.SCHDULE

dec_points = numpy.ndarray(dtype=numpy.uint32, shape=(k,))

raw_data = [numpy.ndarray(shape=(buffsize,), dtype=numpy.uint8) for i in xrange(k)]
encoded_data = [numpy.zeros(buffsize, dtype=numpy.uint8) for i in xrange(k)]

file_name = sys.argv[1]
file_size = os.path.getsize(file_name)

survived = random.sample(range(n), k) 
inputfiles = [io.open(file_name+"_%d"%i,'rb') for i in survived]
outputfile = io.open(file_name+"_decoded", 'wb')

for i,p in enumerate(survived):
    dec_points[i] = p+1
print dec_points
decoder = HSRC(k, dec_points, w=w, packetsize=packetsize, mode=mode, decoder=True)

readblock = k*buffsize
to_read = file_size
while to_read>0:
    for i,inputf in enumerate(inputfiles):
        inputf.readinto(encoded_data[i])
    decoder.decode(encoded_data, raw_data)
    if to_read>=readblock:
        for rd in raw_data:
            outputfile.write(rd)
        to_read -= readblock
    else:
        data = to_read 
        for rd in raw_data:
            outputfile.write(buffer(rd,0,to_read))
            to_read = max(to_read-buffsize, 0)

for inputf in inputfiles:
    inputf.close()
outputfile.close()
