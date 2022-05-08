# Copyright 2022 - Pare Technologies
import logging
import OpenGL
OpenGL.ERROR_ON_COPY = True
OpenGL.FULL_LOGGING = True
OpenGL.ERROR_CHECKING = True
import OpenGL.GL as gl
import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame as pg

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class App:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_icon(pg.image.load('gfx\logo.png'))
        pg.display.set_caption('App Title', 'App Icon Title')

        display_flags = pg.OPENGL | pg.DOUBLEBUF
        pg.display.set_mode((640, 480), display_flags)

        self.clock = pg.time.Clock()

        gl.glClearColor(0.1, 0.2, 0.2, 1)

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
        pg.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
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
