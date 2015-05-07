# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from itertools import cycle
import cocos
from pyglet import clock
import random

from cocos.actions import (
    MoveBy, MoveTo, RotateBy, RotateTo, ScaleBy, ScaleTo
)

HOP = ScaleBy(0.5, 0.15) + ScaleTo(1.0, 0.15)


class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        self.left = cocos.sprite.Sprite('foot.png', (300, 100))
        self.right = cocos.sprite.Sprite('footr.png', (375, 100))

        self.add(self.left)
        self.add(self.right)

        self.steps = cycle([
            random.choice([
                self.hop_left,
                self.hop_right,
                self.wait,
                self.step_left,
                self.step_right,
                self.wiggle,
                self.reset,
                self.reset,
            ]) for _ in range(7)] + [self.reset]
        )

        clock.schedule_interval(self.next_step, 0.5)

    def next_step(self, dt):
        next(self.steps)()

    def hop_right(self):
        move = cocos.actions.MoveBy((100, 100), 0.3) | HOP
        self.left.do(move)
        self.right.do(move)

    def hop_left(self):
        move = cocos.actions.MoveBy((-100, 100), 0.3) | HOP
        self.left.do(move)
        self.right.do(move)

    def step_left(self):
        self.left.do(
            MoveBy((-50, 100), 0.3) |
            RotateBy(-40, 0.3) | HOP
        )

    def step_right(self):
        self.right.do(
            MoveBy((50, 100), 0.3) |
            RotateBy(40, 0.3) | HOP
        )

    def wiggle(self):
        foot = random.choice([self.left, self.right])
        foot.do(
            (RotateBy(-10, 0.1) + RotateBy(10, 0.1)) * 3
        )

    def reset(self):
        leftReset = cocos.actions.MoveTo((300, 100), 0.3) | RotateTo(0, 0.1) | HOP
        rightReset = cocos.actions.MoveTo((375, 100), 0.3) | RotateTo(0, 0.1) | HOP
        self.left.do(leftReset)
        self.right.do(rightReset)

    def wait(self):
        pass


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    # We create a new layer, an instance of HelloWorld
    hello_layer = HelloWorld()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(hello_layer)


    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
