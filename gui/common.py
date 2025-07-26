# gui/common.py — Shared GUI helpers for themed windows, buttons, layout
import tkinter as tk
from tkinter import ttk

def create_themed_window(title="Window", size="1200x700"):
    root = tk.Tk()
    root.title(title)
    root.configure(bg="#1e1e1e")
    root.geometry(size)
    return root

def style_button(widget, width=30):
    widget.configure(bg="#3e3e3e", fg="white", width=width)

def make_scrollable_frame(parent):
    canvas = tk.Canvas(parent, bg="#1e1e1e", highlightthickness=0)
    frame = tk.Frame(canvas, bg="#1e1e1e")
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.create_window((0, 0), window=frame, anchor='nw')

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)
    return frame
