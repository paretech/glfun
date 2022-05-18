# Copyright 2022 - Pare Technologies
"""Main Application

The main application contains functionality related to managing the application,
creating window, OpenGL Context.
"""
import OpenGL
OpenGL.ERROR_ON_COPY = True
OpenGL.FULL_LOGGING = False
OpenGL.ERROR_CHECKING = True
import OpenGL.GL as gl
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg
import graphics
import pyrr
import numpy as np

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class App:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_icon(pg.image.load(r'gfx/logo.png'))
        pg.display.set_caption('PyOpenGL Cube Spin', 'App Icon Title')

        display_flags = pg.OPENGL | pg.DOUBLEBUF
        pg.display.set_mode((640, 480), display_flags)

        self.clock = pg.time.Clock()

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.1, 0.2, 0.2, 1)

        self.scene_cube = graphics.Cube(position=[0, 0, -3], eulers=[0, 0, 0])

        self.scene_camera = graphics.Camera

        self.view_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640/480, 
            near=0.1, far=10, dtype=np.float32
        )

        self.main_event_loop()

    def main_event_loop(self):
        while True:
            self.event_handler()
            self.display()

    def event_handler(self):
        for event in pg.event.get():
            log.debug(f'Detected event {event.type}')
            if (event.type == pg.QUIT):
                raise SystemExit

    def display(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        # @Next: fix the following line, then modify shader to add uniform
        self.scene_cube.draw(self.projection_transform)

        pg.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARN,
        # for debug consider adding %(filename)s:%(lineno)s %(funcName)s()
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                filename=f'{__file__}.log',
                mode='w'
                ),
            logging.StreamHandler()
        ]
    )

    myApp = App()
