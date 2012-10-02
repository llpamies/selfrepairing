import numpy
import sys

a = bytearray(open(sys.argv[1], 'rb').read())
b = bytearray(open(sys.argv[2], 'rb').read())

aa = numpy.ndarray(shape=(len(a),), dtype=numpy.uint8, buffer=a)
bb = numpy.ndarray(shape=(len(b),), dtype=numpy.uint8, buffer=b)
aa ^= bb

f = open(sys.argv[3], 'wb')
f.write(aa.data)
f.close()
