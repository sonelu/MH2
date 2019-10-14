from basescreen import BaseScreen

class MenuScreen(BaseScreen):

    def __init__(self, display, robot, title, navigation, options, actions):
        super(MenuScreen, self).__init__(display, robot, title, navigation)
        self.cursel = 0
        self.options = options
        self.actions = actions

    def render(self, draw):
        super(MenuScreen, self).render(draw)
        # options
        xsize, ysize = draw.textsize('A', font=self.font)
        ysize += 2 # add some spacing
        for index, line in enumerate(self.options):
            ypos = ysize + 5 + index * ysize
            if index == self.cursel:
                draw.rectangle((0, ypos, 127, ypos+ysize-1), fill="white", outline="white")
                draw.text((0, ypos), line, fill="black", font=self.font)
            else:
                draw.text((0, ypos), line, fill="white", font=self.font)

    def navUp(self):
        noptions = len(self.options)
        self.cursel = (self.cursel - 1) % noptions

    def navDown(self):
        noptions = len(self.options)
        self.cursel = (self.cursel + 1) % noptions

