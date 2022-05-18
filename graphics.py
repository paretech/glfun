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
    def __init__(self, position, eulers):
        self.position = position
        self.eulers = eulers

        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)

        self.shader = shader.Program(
                            vertex=r'./shaders/shader.vert',
                            fragment=r'./shaders/shader.frag',
                        )

        self.transform_location = gl.glGetUniformLocation(self.shader.gl_name, 'mvp_matrix')

        self.vertex_data = self._load_vertex_data()

        self.config_shader()

    @property
    def model_transform(self):
        # return pyrr.matrix44.multiply(
        #     m1=pyrr.matrix44.create_from_eulers(
        #         eulers=np.radians(self.eulers), dtype=np.float32
        #     ),
        #     m2=pyrr.matrix44.create_from_translation(
        #         vec=np.array(self.position), dtype=np.float32
        #     ),
        # )
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        """
            pitch: rotation around x axis
            roll:rotation around z axis
            yaw: rotation around y axis
        """
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_eulers(
                eulers=np.radians(self.eulers), dtype=np.float32
            )
        )
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.position),dtype=np.float32
            )
        )

        return model_transform

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

    def draw(self, transform_matrix, mode=gl.GL_TRIANGLE_STRIP):
        mvp_matrix = pyrr.matrix44.multiply(
            m1=self.model_transform,
            m2=transform_matrix
        )
        gl.glBindVertexArray(self.vbo)
        gl.glUseProgram(self.shader.gl_name)
        gl.glUniformMatrix4fv(self.transform_location, 1, gl.GL_FALSE, mvp_matrix)
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

