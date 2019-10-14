from basescreen import BaseScreen


class InfoScreen(BaseScreen):
    """
    Displays a static long text on the screen.
    Does not expect any interaction.
    Diamissal and / or switch of the screen is controlled
    externally.
    """
    def __init__(self, display, robot=None, title="", navigation={}, text=""):
        super(InfoScreen, self).__init__(display, robot, title, navigation)
        self.text = text
        
    def render(self, draw):
        super(InfoScreen, self).render(draw)

        size = draw.multiline_textsize(self.text, font=self.font)
        posx = (self.avail[1][0] - self.avail[0][0] - size[0]) // 2
        posy = (self.avail[1][1] - self.avail[0][1] - size[1]) // 2
        draw.multiline_text((posx, posy), self.text, fill="white", align="center", font=self.font)

    def updateText(self, text):
        self.text = text
        #self.show()


class InfoScreenButton(BaseScreen):
    """
    Displays a static long text on the screen.
    plus a "button" with a name (ex.stop)
    Diamissal and / or switch of the screen is controlled
    externally.
    """
    def __init__(self, display, title, navigation, text, button):
        super(InfoScreenButton, self).__init__(display, title, navigation)
        self.text = text
        self.button = button

    def render(self, draw):
        super(InfoScreenButton, self).render(draw)

        size = draw.multiline_textsize(self.text, font=self.font)
        buttsize = draw.textsize(self.button, font=self.font)
        posx = (self.avail[1][0] - self.avail[0][0] - size[0]) // 2
        posy = (self.avail[1][1] - self.avail[0][1] - size[1] - buttsize[1] - 4) // 2
        draw.multiline_text((posx, posy), self.text, fill="white", align="center", font=self.font)
        posx = (self.avail[1][0] - self.avail[0][0] - buttsize[0]) // 2
        posy = self.avail[1][1] - buttsize[1] - 4
        draw.rectangle((posx-2, posy-2, posx+buttsize[0]+2, posy+buttsize[1]+2), fill="black", outline="white")
        draw.rectangle((posx, posy, posx+buttsize[0], posy+buttsize[1]), fill="white", outline="white")
        draw.text((posx, posy), self.button, fill="black")

    def updateText(self, text):
        self.text = text
        self.show()