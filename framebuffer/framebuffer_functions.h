#pragma once

#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdio.h>

typedef struct fb_var_screeninfo fb_var_screeninfo;

int setScreenResolution(unsigned int width, unsigned int height);
void* getScreenMemory(void);