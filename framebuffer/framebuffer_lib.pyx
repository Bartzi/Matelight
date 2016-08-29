from libc.stdlib cimport free
from cpython cimport PyObject, Py_INCREF

import numpy as np
cimport numpy as np

cimport framebuffer_lib as buffer_lib

np.import_array()

cdef class ArrayWrapper:
    """
        Array Wrapper that enables us to use python refcounting and a good clean up of the data we get
        See https://gist.github.com/GaelVaroquaux/1249305 for more info
    """
    cdef void* data_ptr
    cdef int height
    cdef int width
    cdef int channels

    cdef set_data(self, int height, int width, int channels, void* data_ptr):
        self.data_ptr = data_ptr
        self.height = height
        self.width = width
        self.channels  = channels

    def __array__(self):
        cdef np.npy_intp shape[3]
        shape[0] = <np.npy_intp> self.height
        shape[1] = <np.npy_intp> self.width
        shape[2] = <np.npy_intp> self.channels

        ndarray = np.PyArray_SimpleNewFromData(3, shape, np.NPY_INT, self.data_ptr)
        return ndarray

    def __dealloc__(self):
        free(<void*>self.data_ptr)


cdef class Framebuffer:
    cdef void * screenMemory;

    cpdef void set_screen_size(self, int width, int height):
        buffer_lib.setScreenResolution(width, height)

    cpdef void map_screen_memory(self):
        self.screenMemory = buffer_lib.getScreenMemory()
        pass

    cdef void* read_screen_memory(self):
        return self.screenMemory


def read_screen(int screen_width, int screen_height, Framebuffer framebuffer):
    cdef void* array
    cdef np.ndarray ndarray

    array = framebuffer.read_screen_memory()
    array_wrapper = ArrayWrapper()
    array_wrapper.set_data(screen_height, screen_width, 3, <void*> array)
    ndarray = np.array(array_wrapper, copy=False)
    ndarray.base = <PyObject*> array_wrapper
    Py_INCREF(array_wrapper)

    return ndarray
