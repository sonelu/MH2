from basescreen import BaseScreen
from luma.core.render import canvas
import psutil
import numpy as np
from itertools import repeat
import NetworkManager
import time


class StatusScreen(BaseScreen):

    def __init__(self, display, robot, title, navigation):
        super(StatusScreen, self).__init__(display, robot, title, navigation)

    def _drawHBar(self, canvas, y, perc, ltext, rtext):
        """ Draws a horizontal bar with text on the left (4 chars) and
        text on the right (4-5 chars)
        """
        b = 60    # bar length
        h = 9     # bar height
        l = 30    # left align bar
        g = 4     # gap on the right after bar

        canvas.text((2, y), ltext, fill="white", font=self.font) # text on left of bar
        bar = int(perc*b)
        canvas.rectangle((l, y, l+bar, y+h), outline="black", fill="white")
        canvas.text((b+l+g, y), rtext, fill="white", font=self.font)

    def render(self, draw):
        super(StatusScreen, self).render(draw)

        f = self.avail[0][1]    # position for first line
        d = 10    # spacing between lines
        pos = f
        # cpu
        cpu, _, _ = psutil.getloadavg()
        cpus = psutil.cpu_count()
        perc = min(cpu, cpus)/cpus
        self._drawHBar(draw, pos, perc, "CPU:", '{:.2f}'.format(cpu))
        pos += d
        # cpu freq
        freq = psutil.cpu_freq()
        perc = (freq.current - freq.min)/(freq.max - freq.min)
        self._drawHBar(draw, pos, perc, "Frq:", '{:.2f}'.format(freq.current/1000.0))
        pos += d
        # governor
        with open('/sys/devices/system/cpu/cpufreq/policy0/scaling_governor', 'r') as f:
            gov = f.readline()
        draw.text((2, pos), "Gov: {}".format(gov), fill="white", font=self.font)
        pos += d
        # cpu temp
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        self._drawHBar(draw, pos, temp/100.0, "Tem:", '{:.1f}'.format(temp))
        pos += d
        # mem
        perc = psutil.virtual_memory().percent
        self._drawHBar(draw, pos, perc/100.0, "Mem:", '{}%'.format(perc))
        pos += d
        # disk
        disk = psutil.disk_usage('/home').percent
        self._drawHBar(draw, pos, disk/100.0, "Dsk:", '{:.1f}%'.format(disk))
        pos += d
        # dotted line
        draw.point(zip(range(0,128,2), repeat(pos+1)), fill="white")
        pos += 3
        # battery
        volts = np.mean([m.present_voltage for m in self.robot.motors])
        max_v = 8.0            # max voltage to represent (100%)
        min_v = 6.0            # min voltage to represent (0%)
        volts = min(volts, max_v)     # in case there is above max_v
        perc = (volts - min_v)/(max_v - min_v)
        self._drawHBar(draw, pos, perc, "Bat:", '{:.1f}'.format(volts))
        pos += d
        # uptime
        uptime = time.time() - psutil.boot_time()
        uptimestr = "UpT: {:2.0f}h:{:2.0f}m:{:2.0f}s".format(uptime//3600, uptime%3600//60, uptime%60)
        draw.text((2, pos), uptimestr, fill="white", font=self.font)
        pos += d
        # dotted line
        draw.point(zip(range(0,128,2), repeat(pos+1)), fill="white")
        pos += 3
        # wifi
        wifi_state = "no connection"
        wifi_ip = "N/A"
        wifi_strength = 0
        try:
            for dev in NetworkManager.NetworkManager.GetDevices():
                if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
                    state = NetworkManager.const('device_state', dev.State)
                    ssid = dev.ActiveAccessPoint.Ssid
                    wifi_strength = float(dev.ActiveAccessPoint.Strength)/100.0
                    wifi_state = ssid
                    wifi_ip = dev.Ip4Config.Addresses[0][0]
        except:
            pass
        draw.text((2, pos), "WFi: {}".format(wifi_state), fill="white", font=self.font)
        pos += d
        self._drawHBar(draw, pos, wifi_strength, "WFi:", "{:.0f}%".format(wifi_strength*100))
        pos += d
        draw.text((2, pos), "IP4: {}".format(wifi_ip), fill="white", font=self.font)
        pos += d

class HistoScreen(BaseScreen):

    def __init__(self, display, robot, navigation, parameter, v_min, v_max, title):
        super(HistoScreen, self).__init__(display, robot, title, navigation)
        self.param = parameter
        self.v_min = v_min
        self.v_max = v_max
        self.title = title

    def render(self, draw):
        super(HistoScreen, self).render(draw)
        values = dict([(m.id, abs(getattr(m, self.param))) for m in self.robot.motors])
        bw = 4                # bar width
        bbot = 110            # lower edge of the bar
        btop = 20             # upper edge of the bar
        bh = bbot - btop      # bar height

        order = [[54, 43, 52, 51],
                 [16, 15, 14, 13, 12, 11],
                 [36, 37],
                 [21, 22, 23, 24, 25, 26],
                 [41, 42, 43, 44]]

        hpos = 0        # start horizontal position

        # dotted line
        if self.v_max > 1.0:
            form = '{:.0f}'
        else:
            form = '{:.1f}'
        draw.point(zip(range(0,128,2), repeat(btop)), fill="white")
        strval = form.format(self.v_max)
        size = draw.textsize(strval)
        draw.text((127-size[0], btop+1), strval, fill="white", font=self.font)
        mid = (bbot + btop) // 2
        draw.point(zip(range(0,128,2), repeat(mid)), fill="white")
        strval = form.format(((self.v_max+self.v_min)/2.0))
        size = draw.textsize(strval)
        draw.text((127-size[0], mid+1), strval, fill="white", font=self.font)
        draw.point(zip(range(0,128,2), repeat(bbot)), fill="white")
        strval = form.format(self.v_min)
        size = draw.textsize(strval)
        draw.text((127-size[0], bbot+1), strval, fill="white", font=self.font)


        for group in order:
            for id in group:
                value = values[id]
                # correct outliers
                value = max(self.v_min, value)
                value = min(self.v_max, value)
                bar = (value - self.v_min)/(self.v_max - self.v_min)*bh
                bar = int(round(bar))
                # draw the bar
                draw.rectangle((hpos,bbot,hpos+bw-1,bbot-bar), outline="white", fill="white")
                hpos += bw+1
            # between groups show a line
            #if hpos < 120:
            #    draw.line((hpos,top,hpos,63), fill="white")
            hpos += 2


class TemperatureScreen(HistoScreen):

    def __init__(self, display, robot, title, navigation):
        super(TemperatureScreen, self).__init__(display, robot, navigation, 'present_temperature', 20.0, 65.0, title)


class TorqueLoadScreen(HistoScreen):

    def __init__(self, display, robot, title):
        super(TorqueLoadScreen, self).__init__(display, robot, navigation, 'present_load', 0.0, 1.0, title)


class PositionScreen(BaseScreen):

    def __init__(self, display, robot, title, navigation):
        super(PositionScreen, self).__init__(display, robot, title, navigation)

    def render(self, draw):
        super(PositionScreen, self).render(draw)

        order = [[36,54,53,52,51,11,12,13,14,15,16],
                 [37,44,43,42,41,21,22,23,24,25,26]]

        codes = ['hd','ey','az','sx','sy','hz','hx','hy', 'ky','ay','ax']

        vsp = 25
        current = dict([(m.id, (m.present_position, m.goal_position)) for m in self.robot.motors])
        draw.text((5, 15), "    ACT(R)DES ACT(L)DES", fill="white", font=self.font9)
        for i in range(len(order[0])):
            vpos = i*9 + 25
            id1 = order[0][i]
            id2 = order[1][i]
            ftext = "{}  {:4.0f} {:4.0f} {:4.0f} {:4.0f}".format(codes[i], current[id1][0], current[id1][1], current[id2][0], current[id2][1])
            draw.text((5, vpos), ftext, fill="white", font=self.font9)
