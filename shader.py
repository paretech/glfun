import ctypes
import OpenGL.GL as gl
import OpenGL.GL.shaders
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def buffer_offset(offset):
    '''Specifies offset in OpenGL buffer to first component'''
    return ctypes.c_void_p(offset)


def create_shader_from_file(shader_type, filepath):
    with open(filepath) as f:
        return create_shader(shader_type, f.readlines())


def create_shader(shader_type, shader_source):
    """Create an OpenGL Shader"""
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, shader_source)
    # @TODO: With empty shader file, this call results in GLError on Mac but not windows
    try:
        gl.glCompileShader(shader)
    finally:
        check_shader(shader, shader_type, shader_source)

    return shader


def check_shader(shader, shader_type, shader_source):
    '''Perform various status checks on shader

    Typically run immediately after compiling a shader.
    '''
    compile_status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if compile_status != gl.GL_TRUE:
        log.warning(f'Problem compiling {shader_type!r}')

    shader_log = gl.glGetShaderInfoLog(shader)
    if shader_log:
        log.warning(f'{shader_type!r}: {shader_log.strip()}')

    if not shader_source:
        log.warning(f'{shader_type!r} source empty.')


def create_shader_program(shaders):
    '''Create shader program and attach shaders'''
    program = gl.glCreateProgram()

    attach_shaders(program, shaders)

    try:
        gl.glLinkProgram(program)
    finally:
        check_program(program)
        delete_shaders(shaders)

    return program


def attach_shaders(program, shaders):
    '''Attach shaders to the shader program'''
    for shader in shaders:
        gl.glAttachShader(program, shader)


def delete_shaders(shaders):
    '''Delete compiled shaders

    Typically performed after verify successful program linking.
    '''
    for shader in shaders:
        gl.glDeleteShader(shader)


def check_program(program):
    link_status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if link_status != gl.GL_TRUE:
        log.warning(f'Problem linking Program{program}')

    program_log = gl.glGetProgramInfoLog(program)
    if program_log:
        log.warning(f'Program{program}: {program_log.strip()}')

    attached_shaders = gl.glGetProgramiv(program, gl.GL_ATTACHED_SHADERS)
    if attached_shaders != 2:
        log.error(f'Shader program{program} has {attached_shaders} but expected only 2.')


class Program:
    def __init__(self, vertex, fragment):
        self._shaders = [
            Shader(gl.GL_VERTEX_SHADER, vertex),
            Shader(gl.GL_FRAGMENT_SHADER, fragment),
        ]

        shader_names = [shader.name for shader in self._shaders]
        self.name = create_shader_program(shader_names)

    def __repr__(self):
        return self.name


class Shader:
    def __init__(self, shader_type, filepath):
        self._shader_type = shader_type
        self._filepath = filepath
        self.name = self.create_shader()

    def create_shader(self):
        return create_shader_from_file(self._shader_type, self._filepath)

    @property
    def type(self):
        return gl.glGetShaderiv(self.name, gl.GL_SHADER_TYPE)

    @property
    def compile_status(self):
        return gl.glGetShaderiv(self.name, gl.GL_COMPILE_STATUS)

    @property
    def compile_info(self):
        return gl.glGetShaderInfoLog(self.name)


# raise ShaderCompilationError(
#     """Shader compile failure (%s): %s""" % (
#         compile_status,
#         gl.glGetShaderInfoLog(shader),
#     ),
#     source_code,
#     shader_type,
# )
class ShaderCompilationError(RuntimeError):
    """Raised when a shader compilation fails"""


class ShaderValidationError(RuntimeError):
    """Raised when a program fails to validate"""


class ShaderLinkError(RuntimeError):
    """Raised when a shader link fails"""


class ShaderAttributeError(RuntimeError):
    """Raised when a shader attribute is invalid

    Raised when the named attribute variable is not an active attribute in the
    specified shader program or if name starts with the reserved prefix "gl_"
    """
