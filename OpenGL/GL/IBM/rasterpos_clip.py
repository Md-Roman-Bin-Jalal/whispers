'''OpenGL extension IBM.rasterpos_clip

This module customises the behaviour of the 
OpenGL.raw.GL.IBM.rasterpos_clip to provide a more 
Python-friendly API

Overview (from the spec)
	
	IBM_rasterpos_clip extends the semantics of the RasterPos functions.  It
	provides an enable that allows a raster position that would normally be
	clipped to be treated as a valid (albeit out-of-viewport) position.
	
	This extension allows applications to specify geometry-aligned pixel
	primitives that may be partially off-screen.  These primitives are
	tested on a pixel-by-pixel basis without being rejected completely
	because of an invalid raster position.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/IBM/rasterpos_clip.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.IBM.rasterpos_clip import *
from OpenGL.raw.GL.IBM.rasterpos_clip import _EXTENSION_NAME

def glInitRasterposClipIBM():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION