cdef extern from "framebuffer_functions.h":
    ctypedef struct fb_var_screeninfo:
        pass
    int setScreenResolution(unsigned int width, unsigned int height)
    void* getScreenMemory()


