#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: theme.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Tiny theming helpers for Tkinter widgets.

Usage: 
from library_ms.ui.theme import apply_base_theme

Notes: 
- Keep visuals minimal and readable; extend as needed.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def apply_base_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    # Try default theme; fall back if unavailable
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TButton", padding=(8, 6))
    style.configure("TEntry", padding=(4, 4))
    style.configure("Treeview", rowheight=24)
    style.configure("TLabel", padding=(2, 2))
