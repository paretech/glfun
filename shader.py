import OpenGL.GL as gl
import OpenGL.GL.shaders
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())




def create_shader_from_file(shader_type, filepath):
    try:
        with open(filepath) as f:
            return create_shader(shader_type, f.readlines())
    except Exception as e:
        log.error(e)
        raise e


def create_shader(shader_type, source_code):
    """Create an OpenGL Shader"""
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, source_code)
    gl.glCompileShader(shader)

    compile_status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if compile_status != gl.GL_TRUE:
        raise ShaderCompilationError(
            """Shader compile failure (%s): %s"""%(
                compile_status,
                glGetShaderInfoLog( shader ),
            ),
            source,
            shaderType,
        )
    return shader


def create_shader_program(shaders):
    program = gl.glCreateProgram()

    for shader in shaders:
        gl.glAttachShader(program, shader)

    gl.glLinkProgram(program)

    # @TODO: Check link status and logs

    return program


class Program:
    def __init__(self, vertex, fragment):
        self._shaders = [
            Shader(gl.GL_VERTEX_SHADER, vertex),
            Shader(gl.GL_FRAGMENT_SHADER, fragment),
        ]
        self.name = gl.glCreateProgram()


class Shader:
    def __init__(self, shader_type, filepath):
        self._shader_type = shader_type
        self._filepath = filepath
        self.name = self.create_shader()

    def create_shader(self):
        shader = create_shader_from_file(self._shader_type, self._filepath)

        # if self.compile_status != gl.GL_TRUE:

        return shader

    @property
    def type(self):
        import OpenGL
        a = OpenGL.GL.shaders.compileProgram()
        return gl.glGetShaderiv(self.name, gl.GL_SHADER_TYPE)

    @property
    def compile_status(self):
        return gl.glGetShaderiv(self.name, gl.GL_COMPILE_STATUS)

    @property
    def compile_info(self):
        return gl.glGetShaderInfoLog(self.name)


class ShaderCompilationError(RuntimeError):
    """Raised when a shader compilation fails"""


class ShaderValidationError(RuntimeError):
    """Raised when a program fails to validate"""


class ShaderLinkError(RuntimeError):
    """Raised when a shader link fails"""