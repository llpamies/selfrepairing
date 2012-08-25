cimport numpy
from jerasure cimport *
from cpython cimport bool

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void free(void* ptr)

class HSRCMode:
    MATRIX = 1
    BITMATRIX = 2
    SCHDULE = 3

class HSRCUndecodableException(Exception):
    pass

cdef class HSRC:
    cdef int k
    cdef int w
    cdef int n
    cdef int packetsize
    cdef bool decoder
    cdef int** schedule
    cdef int* bitmatrix
    cdef int* matrix
    cdef int mode

    def __cinit__(self, *args, **kwargs):
        self.schedule = NULL
        self.bitmatrix = NULL
        self.matrix = NULL
        self.decoder = False

    def __init__(self, int k, numpy.ndarray[numpy.uint32_t, ndim=1] points not None, int w=32,\
                 int packetsize=sizeof(long), bool decoder=False, int mode=3):
        cdef int i, j, e, n
        cdef int *imatrix

        if packetsize%sizeof(long)!=0:
            raise ValueError("packetsize should be multiple of %d"%(sizeof(long)))

        if decoder and len(points)!=k:
            raise ValueError("when decoding len(points) should be equal to k")

        self.k = k
        self.w = w
        self.n = len(points)
        self.packetsize = packetsize
        self.decoder = decoder
        self.mode = mode
      
        self.matrix = <int*> malloc(self.k*self.n*sizeof(int))
        for i in range(self.n):
            e = points[i]
            self.matrix[i*k] = e
            for j in range(1, k):
                e = galois_single_multiply(e, e, self.w)
                self.matrix[i*k+j] = e
               
        if decoder:
            imatrix = <int*> malloc(self.k*self.n*sizeof(int))
            if jerasure_invert_matrix(self.matrix, imatrix, self.k, self.w)!=0:
                free(imatrix)
                raise HSRCUndecodableException("cannot decode with these points")
            free(self.matrix)
            self.matrix = imatrix
        
        self.bitmatrix = jerasure_matrix_to_bitmatrix(self.k, self.n, self.w, self.matrix)
        self.schedule = jerasure_smart_bitmatrix_to_schedule(self.k, self.n, self.w, self.bitmatrix)
        
    def __dealloc__(self):
        if self.schedule!=NULL:
            jerasure_free_schedule(self.schedule)
        if self.bitmatrix!=NULL:
            free(self.bitmatrix)
        if self.matrix!=NULL:
            free(self.matrix)

    def print_matrix(self):
        jerasure_print_matrix(self.matrix, self.k, self.n, self.w)

    def decode(self, *args, **kwargs):
        if not self.decoder:
            raise Exception("encoding mode")

        return self.__encode(*args, **kwargs)

    def encode(self, *args, **kwargs):
        if self.decoder:
            raise Exception("decoding mode")
    
        return self.__encode(*args, **kwargs)

    def __encode(self, raw_data not None, encoded_data not None):
        cdef int i, size
        cdef char **raw_ptrs
        cdef char **encoded_ptrs

        size = len(raw_data[0])

        if any(len(raw_data[i])!=size for i in range(len(raw_data))):
            raise ValueError("all vectors should have the same size")
        
        if any(len(encoded_data[i])!=size for i in range(len(encoded_data))):
            raise ValueError("all vectors should have the same size")

        if size%(self.w*self.packetsize)!=0:
            raise ValueError("the size of data vectors should be multiple of w*packetsize (%d)"%(self.w*self.packetsize))

        raw_ptrs = <char**>malloc(self.k*sizeof(char*))
        if raw_ptrs==NULL:
            raise Exception("malloc error: raw_ptrs")
        for i in range(self.k):
            raw_ptrs[i] = numpy.PyArray_BYTES(raw_data[i])

        encoded_ptrs = <char**>malloc(self.n*sizeof(char*))
        if encoded_ptrs==NULL:
            free(raw_ptrs)
            raise Exception("malloc error: encoded_ptrs")
        for i in range(self.n):
            encoded_ptrs[i] = numpy.PyArray_BYTES(encoded_data[i])
      
        if self.mode==3:
            jerasure_schedule_encode(self.k, self.n, self.w, self.schedule, raw_ptrs, encoded_ptrs, size, self.packetsize) 
        elif self.mode==2:
            jerasure_bitmatrix_encode(self.k, self.n, self.w, self.bitmatrix, raw_ptrs, encoded_ptrs, size, self.packetsize)
        elif self.mode==1:
            jerasure_matrix_encode(self.k, self.n, self.w, self.matrix, raw_ptrs, encoded_ptrs, size)
        else:
            assert False

        free(raw_ptrs)
        free(encoded_ptrs)
