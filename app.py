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

        gl.glClearColor(0.1, 0.2, 0.2, 1)

        self.scene_objects = [graphics.Cube(location=[0, 0, -3], euler=[0, 0, 0])]

        self.scene_camera = graphics.Camera

        self.mvp_matrix = pyrr.matrix44.create_identity(dtype=np.float32)

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
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # @Next: fix the following line, then modify shader to add uniform
        # gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.scene_objects[0].shader.gl_name, 'mvp_matrix'), 1, gl.GL_FALSE, self.mvp_matrix)
        for object in self.scene_objects:
            object.draw()

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
