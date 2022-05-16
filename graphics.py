import OpenGL.GL as gl
import numpy as np
import shader
import logging
import vertices
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

        self.vertices = self.load_vertices()

    def load_vertices(self):
        colors = np.array([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]], dtype=np.float32)

        data_types = np.dtype([
            ('position', np.float32, vertices.cube.shape[1]),
            ('color',    np.float32, colors.shape[1]),
        ])

        vertex_data = np.zeros(vertices.cube.shape[0], dtype=data_types)
        vertex_data['position'] = vertices.cube
        vertex_data['color'] = np.repeat(np.array(colors, dtype=np.float32), repeats=3*2*2, axis=0)

        return vertex_data

    def config_shader(self):
        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

    def draw(self, mode=gl.GL_TRIANGLE_STRIP):
        gl.glBindVertexArray(self.vbo)
        gl.glUseProgram(self.shader.name)
        gl.glDrawArrays(mode, 0, self.vertices.size)
