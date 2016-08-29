from Cython.Distutils import build_ext
import numpy


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('', parent_package, top_path)
    config.add_extension(
        'framebuffer_lib',
        sources=["framebuffer_lib.pyx", "framebuffer_functions.c"],
        include_dirs=[numpy.get_include(), '.']

    )
    return config

if __name__ == "__main__":
    params = configuration(top_path='').todict()
    params['cmdclass'] = dict(build_ext=build_ext)

    from numpy.distutils.core import setup
    setup(**params)