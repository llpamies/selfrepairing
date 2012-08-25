import sys
sys.path[0] = 'build/lib.linux-i686-2.7'

import io
import os.path
import numpy
import itertools
from selfrepairing import HSRC, HSRCMode

numpy.set_printoptions(linewidth=100)

k = 3
n = 7
w = 32
packetsize = 128
buffsize = w*packetsize
mode = HSRCMode.SCHDULE

enc_points = numpy.ndarray(dtype=numpy.uint32, shape=(n,))

for i,p in enumerate([1,2,3,4,5,6,7]):
    enc_points[i] = p

raw_data = [numpy.ndarray(shape=(buffsize,), dtype=numpy.uint8) for i in xrange(k)]
encoded_data = [numpy.zeros(buffsize, dtype=numpy.uint8) for i in xrange(n)]

encoder = HSRC(k, enc_points, w=w, packetsize=packetsize, mode=mode)

file_name = sys.argv[1]
file_size = os.path.getsize(file_name)

inputfile = io.open(file_name, 'rb')
outputfiles = [io.open(file_name+"_%d"%i,'wb') for i in xrange(n)]

read_block = k*buffsize
to_read = file_size
while to_read>0:
    for i in xrange(k):
        data_read = inputfile.readinto(raw_data[i])
        to_read -= data_read
    encoder.encode(raw_data, encoded_data)
    for ed,of in itertools.izip(encoded_data, outputfiles):
        of.write(ed)

for of in outputfiles:
    of.close()
inputfile.close()
