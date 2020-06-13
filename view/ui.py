#!/usr/bin/env python
import gi
import cairo
import time
import threading

from datetime import datetime
from model.chro import Stopwatch
from gi.repository import Gtk, GObject, Gdk

from control.chro import StopwatchController

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
Gdk.threads_init()


class App(object):
    def __init__(self, builder):
        # get glade objects
        self.toggle_timer_btn = builder.get_object("toggle_timer_btn")
        self.split_time_btn = builder.get_object("split_timer_btn")
        self.show_timer_window_btn = builder.get_object("show_timer_window_btn")
        self.show_split_segments_viewer_btn = builder.get_object("show_split_segments_viewer_btn")
        self.set_timer_title_btn = builder.get_object("set_timer_title_btn")
        self.title_above_chro_entry = builder.get_object("title_above_chro_entry")
        self.toggle_timer_decorator_btn = builder.get_object("toggle_timer_decorator_btn")
        self.timer_output = builder.get_object("timer_output")
        self.timer_window = builder.get_object("timer_window")
        self.split_segments_window = builder.get_object("split_segments_window")

        # prepare transparent window
        screen = self.timer_window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.timer_window.set_visual(visual)
        self.timer_window.set_app_paintable(True)

        # connect everything
        self.connect_main_app_buttons()
        self.stop_watch = Stopwatch()
        self.stop_watch_controller = StopwatchController()

        self.stop_watch.toggle = self.toggle_timer_btn
        self.stop_watch.label = self.timer_output

    def connect_main_app_buttons(self):
        self.toggle_timer_btn.connect("clicked", self.toggle_timer)
        self.split_time_btn.connect("clicked", self.split_timer)
        self.show_timer_window_btn.connect("clicked", self.show_timer_window)
        self.show_split_segments_viewer_btn.connect("clicked", self.show_split_segments_viewer)
        self.set_timer_title_btn.connect("clicked", self.set_timer_title)
        self.toggle_timer_decorator_btn.connect("clicked", self.toggle_timer_decorator)
        self.timer_window.connect("destroy", self.close_window)
        self.split_segments_window.connect("destroy", self.close_window)
        self.timer_window.connect('draw', self.draw)

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, 0)
        #!supress-warning
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        #!supress-warning
        context.set_operator(cairo.OPERATOR_OVER)

    def close_window(self, window):
        window.destroy()

    def set_timer_title(self, button):
        self.timer_window.set_title(self.title_above_chro_entry.get_text())

    def toggle_timer_decorator(self, button):
        self.timer_window.set_decorated(not self.timer_window.get_decorated())

    def toggle_timer(self, button):
        print(button)
        if button.get_active():
            self.stop_watch.count()
            button.set_label('Toggle Chronometer [Stop]')
        else:
            button.set_label('Toggle Chronometer [Start]')

    def split_timer(self, button):
        print(button)

    def show_timer_window(self, button):
        print(button)
        self.timer_window.show_all()

    def show_split_segments_viewer(self, button):
        print(button)
        self.split_segments_window.show_all()
