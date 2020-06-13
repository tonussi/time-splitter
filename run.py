from gi.repository import Gtk
from view.ui import App

builder = Gtk.Builder()
builder.add_from_file("splitui.glade")

app = App(builder)

window = builder.get_object("app")
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
