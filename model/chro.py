import time
import threading
from gi.repository import GObject


class Stopwatch(object):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timer_thread = None

        # points of connection with the ui
        self.toggle = None
        self.label = None

    def count(self):
        self.s = time.time()
        self.timer_thread = threading.Thread(target=self.end_change)
        self.timer_thread.start()

    def end_change(self):
        i = 0
        while 1:
            time.sleep(0.01)
            GObject.idle_add(self.change)
            i = i + 1
            if self.toggle.get_active() == 0:
                break

    def change(self):
        show = time.time() - self.s
        hour = show / 3600
        minutes = (show % 3600) / 60
        seconds = show - (int(hour) * 3600) - (int(minutes) * 60)

        hour_str = str(int(hour))
        min_str = str(int(minutes))

        if int(hour) > 0:
            string = '%s:%s:%0.2f' % (hour_str, min_str, seconds)
        string = '%s:%0.2f' % (min_str, seconds)

        self.label.set_text(string)
