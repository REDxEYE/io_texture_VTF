
import time
from libc.stdlib cimport malloc, free
from cpython.array cimport array, clone
# cpdef split = lambda A, n=3: [A[i:i + n] for i in range(0, len(A), n)]

cpdef list split(bytes A,int n):

    cdef int i;
    cdef int b;
    cdef list pixel_array = []
    b = len(A)
    for i in range(0,b,n):
        pixel_array.append(A[i:i + n])
    return pixel_array
cpdef list flip(data, int x, int y, int chan):
    cpdef bytes row;

    # cpdef array[bytes] dataarray = data;
    cdef bytes dataarray = data
    cdef list buff =[]
    for row in split(dataarray,x * chan)[::-1]:
        buff.extend(row)
    return buff

    # return [inner for outer in split(list(data), (x * chan))[::-1] for inner in outer]
cpdef list convert_pixels(data):
    cdef int i;
    cdef int b = len(data);
    cdef list pixel_array = [];
    for i in range(b):
        pixel_array.append(data[i]/256)
    return pixel_array
