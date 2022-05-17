from abc import ABCMeta, abstractmethod
import OpenGL.GL as gl
import numpy as np
import shader
import logging
import vertices
import pyrr
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SceneObject(metaclass=ABCMeta):
    def __init__(self):
        raise NotImplementedError


class Cube():
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

        self.vertex_data = self._load_vertex_data()

        self.config_shader()

    def _load_vertex_data(self):
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

        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data, gl.GL_STATIC_DRAW)

        stride = self.vertex_data.strides[0]

        for field in self.vertex_data.dtype.names:
            location = gl.glGetAttribLocation(self.shader.gl_name, field)

            if location < 0:
                log.warning(f'Unable to find attribute "{field}" in vertex shader.')
                raise shader.ShaderAttributeError()

            size = self.vertex_data[field].shape[1]
            offset = self.vertex_data.dtype.fields[field][1]
            gl.glEnableVertexAttribArray(location)
            gl.glVertexAttribPointer(location, size, gl.GL_FLOAT, gl.GL_FALSE, stride, shader.buffer_offset(offset))

    def draw(self, mode=gl.GL_TRIANGLE_STRIP):
        gl.glBindVertexArray(self.vbo)
        gl.glUseProgram(self.shader.gl_name)
        gl.glDrawArrays(mode, 0, self.vertex_data.size)


class Camera:
    def __init__(self, position, target, up=(0, 1, 0)):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)

        self.view_transform = self.config_view_transform()

    def config_view_transform(self):
        view_transform = pyrr.matrix44.create_look_at(
            eye=self.position,
            target=self.target,
            up=self.up, 
            dtype=np.float32,
        )
        

    @property
    def transform(self):
        return None

