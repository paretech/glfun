# Notes

## Resources

- [PyOpenGL Documentation](http://pyopengl.sourceforge.net/documentation/)
- [Python & OpenGL for Scientific Visualization](https://www.labri.fr/perso/nrougier/python-opengl/)
- [OpenGL with Python (youtube)](https://www.youtube.com/playlist?list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR)
- [NeHe Tutorials](https://nehe.gamedev.net/)
- [Setup linting in VS Code](https://code.visualstudio.com/docs/python/linting)
- [OpenGL Course - Create 3D and 2D Graphics With C++ (YouTube)](https://www.youtube.com/watch?v=45MIykWJ-C4)
- [OpenGL with Python (YouTube Playlist)](https://www.youtube.com/playlist?list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR)
- [Associated GitHub for "OpenGL with Python" playlist](https://github.com/amengede/getIntoGameDev)
- [Rabbid76 Stackoverflow Responses](https://stackoverflow.com/users/5577765/rabbid76)
- [NumPy Reference](https://numpy.org/devdocs/reference/index.html)
  - [Data type objects (dtype)](https://numpy.org/devdocs/reference/arrays.dtypes.html#arrays-dtypes-constructing)


## PyOpenGL Highlights

The following bullets are derrived from reading [PyOpenGL for OpenGL Programmers](http://pyopengl.sourceforge.net/documentation/opengl_diffs.html).

- Errors are raised as exceptions, rather than requiring the user to check return values and/or call glCheckError manually.
- By default, PyOpenGL will log errors to the Python logging module. 
- Supports a significant range of array-compatible data-types
- Don't use lists, tuples, and numbers for performance critical operations.
- You can set a flag to raise exception if there is excessive conversion of numpy arrays. See `OpenGL.ERROR_ON_COPY = True`. 
- Since all the memory allocation in Python is automatic there is no need for glGetPointerv function.
- PyOpenGL has support for most OpenGL extensions.
- There are some differences in how Selection Buffers work

