import OpenGL.GL as gl
import shader
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Cube:
    """Cube Object in 3D Space

    This object is used to represent a cube object in 3D space.

    Input Parameters
        location: Array like object containing the three coordinates
            representing object location in three dimensional Euclidean space.

        eulers: Array like object containing the three coordinates
            representing object orientation using Euler angles.

    Returns a cube object that can be used for subsequent resource management,
    transformation and drawing via OpenGL API.
    """
    def __init__(self, location, euler):
        self.location = location
        self.euler = euler

        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)

        self.shader = shader.Program(
                            vertex=r'./shaders/shader.vert',
                            fragment=r'./shaders/shader.frag',
                        )

        

    def draw(self):
        # raise NotImplementedError
        pass
