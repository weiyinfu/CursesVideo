from typing import List

from curses_video import framework, char_image
import cv2


class CursesVideo(framework.Game):
    def is_over(self) -> bool:
        return not self.has

    def update(self):
        self.has, self.data = self.video.read()
        framework.log('updating', self.has, self.data.shape)

    def on_cmd(self, cmd: int):
        pass

    def tos(self) -> List[List[str]]:
        framework.log(self.data.shape)
        s = char_image.char_image_array(self.data, rows=self.rows, cols=self.cols).split('\n')
        return [list(i) for i in s]

    def init(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

    def __init__(self, filepath: str):
        self.video = cv2.VideoCapture(filepath)
        self.has, self.data = self.video.read()
        framework.log(self.has)


def play(filepath: str):
    framework.CursesGame(CursesVideo(filepath)).main()
