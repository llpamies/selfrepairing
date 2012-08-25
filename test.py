import sys
sys.path[0] = 'build/lib.linux-i686-2.7'

import io
import sys
import numpy
import random
from selfrepairing import HSRC, HSRCMode

numpy.set_printoptions(linewidth=100)

k = 3
n = 7
w = 8
packetsize = 4
size = 32
mode = HSRCMode.SCHDULE

enc_points = numpy.ndarray(dtype=numpy.uint32, shape=(n,))
dec_points = numpy.ndarray(dtype=numpy.uint32, shape=(k,))

raw_data = [numpy.ndarray(shape=(size,), dtype=numpy.uint8) for i in xrange(k)]
for i,buff in enumerate(raw_data):
    buff.fill(i)
encoded_data = [numpy.zeros(size, dtype=numpy.uint8) for i in xrange(n)]

for i,p in enumerate([1,2,3,4,5,6,7]):
    enc_points[i] = p

encoder = HSRC(k, enc_points, w=w, packetsize=packetsize, mode=mode)
print "Encoding matrix:"
encoder.print_matrix()

print "Raw data:"
for i,d in enumerate(raw_data):
    print i,d

encoder.encode(raw_data, encoded_data)

print "Encoded data:"
for i,d in enumerate(encoded_data):
    print i,enc_points[i],d

survived = random.sample(range(n), k)
#survived = [0,1,2]
encoded_data = [encoded_data[i] for i in survived]

print "Survived data:"
for i,(j,d) in enumerate(zip(survived,encoded_data)):
    dec_points[i] = enc_points[j]
    print j,enc_points[j],d

decoder = HSRC(k, dec_points, w=w, packetsize=packetsize, decoder=True, mode=mode)

print "Decoding matrix:"
decoder.print_matrix()

decoder.decode(encoded_data, raw_data)

print "Decoded data:"
for i,d in enumerate(raw_data):
    print i,d
