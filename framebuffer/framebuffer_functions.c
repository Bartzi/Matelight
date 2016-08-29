#include "framebuffer_functions.h"

int framebuffer_device = -1;


int setScreenResolution(unsigned int width, unsigned int height)
{
    fb_var_screeninfo screenInfo;

    if (framebuffer_device == -1)
    {
        framebuffer_device = open("/dev/fb0", O_RDWR);
    }

    if (ioctl(framebuffer_device, FBIOGET_VSCREENINFO, &screenInfo) == -1)
    {
        printf("Can not get Screen Information");
        return 1;
    }

    screenInfo.xres = width;
    screenInfo.yres = height;

    if (ioctl(framebuffer_device, FBIOPUT_VSCREENINFO, &screenInfo) == -1)
    {
        printf("Can not set new resolution");
        return 1;
    }
    return 0;
}

void* getScreenMemory(void)
{
    fb_var_screeninfo screenInfo;
    int line_size, buffer_size;
    void * screenMemory;

    if (framebuffer_device == -1)
    {
        framebuffer_device = open("/dev/fb0", O_RDWR);
    }

    if (ioctl(framebuffer_device, FBIOGET_VSCREENINFO, &screenInfo) == -1)
    {
        printf("Can not get Screen Information");
        return NULL;
    }

    line_size = screenInfo.xres * screenInfo.bits_per_pixel / 8;
    buffer_size = line_size * screenInfo.yres;

    screenInfo.xoffset = 0;
    screenInfo.yoffset = 0;
    if (ioctl(framebuffer_device, FBIOPAN_DISPLAY, &screenInfo) == -1)
    {
        printf("Can not set offsets to 0!");
        return NULL;
    }

    screenMemory = mmap(NULL, buffer_size, PROT_READ, MAP_SHARED, framebuffer_device, 0);
    return screenMemory;
}
