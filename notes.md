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

## Next Steps (5/1/2022)
Create a triangle on canvas, there is a YouTube video linked below should you need it. Rather than just copying the code from the video I really want you to try to build it yourself from scratch...

What do you need to do? From memory of reading books and watching videos, this is what I recall.

1. Define vertex and fragment shader source
2. Create shader reference for each shader
3. Link shader reference to source
4. Compile shader
5. Create program
6. link shaders to program
7. delete no longer needed shader resources
8. Define triangle vertices
9. Define vertex array object (VAO)
10. Bind vertex array object
11. Define vertex buffer object (VBO)
12. Bind VBO
13. Load VBO data
14. Clear screen
15. Draw verteces
16. Flip display
17. Increment clock


https://www.youtube.com/watch?v=45MIykWJ-C4 (17:01 - 29:08)