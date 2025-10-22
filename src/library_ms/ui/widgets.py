#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: widgets.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Reusable Tkinter widget helpers (labeled entries, dialogs, etc.).

Usage: 
from library_ms.ui.widgets import LabeledEntry

Notes: 
- Keep widgets thin; complex flows belong in views.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional


class LabeledEntry(ttk.Frame):
    def __init__(self, master: tk.Widget, text: str, width: int = 30, **entry_kwargs) -> None:
        super().__init__(master)
        self.label = ttk.Label(self, text=text)
        self.entry = ttk.Entry(self, width=width, **entry_kwargs)
        self.label.grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.entry.grid(row=0, column=1, sticky="ew")
        self.columnconfigure(1, weight=1)

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)


def ask_confirm(title: str, message: str) -> bool:
    return messagebox.askyesno(title, message)


def alert_error(message: str, title: str = "Error") -> None:
    messagebox.showerror(title, message)


def alert_info(message: str, title: str = "Info") -> None:
    messagebox.showinfo(title, message)
