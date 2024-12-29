'''OpenGL extension NV.DX_interop2

This module customises the behaviour of the 
OpenGL.raw.WGL.NV.DX_interop2 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/DX_interop2.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.WGL import _types, _glgets
from OpenGL.raw.WGL.NV.DX_interop2 import *
from OpenGL.raw.WGL.NV.DX_interop2 import _EXTENSION_NAME

def glInitDxInterop2NV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION