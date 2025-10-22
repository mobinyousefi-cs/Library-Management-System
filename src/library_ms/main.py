#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Tkinter entrypoint. Wires UI to services and repository; ensures database
migrations run before the UI is presented.

Usage: 
python -m library_ms
# or
library-ms

Notes: 
- Keep root window simple; main content lives in tabbed views.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .db import migrate
from .services import LibraryService
from .ui.theme import apply_base_theme
from .ui.views_books import BooksView
from .ui.views_members import MembersView
from .ui.views_loans import LoansView


class App(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master.title("Library Management System")
        self.master.geometry("960x600")
        self.pack(fill=tk.BOTH, expand=True)

        self.service = LibraryService()

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.books_view = BooksView(notebook, self.service)
        self.members_view = MembersView(notebook, self.service)
        self.loans_view = LoansView(notebook, self.service)

        notebook.add(self.books_view, text="Books")
        notebook.add(self.members_view, text="Members")
        notebook.add(self.loans_view, text="Loans")


def main() -> None:
    migrate()  # ensure tables exist
    root = tk.Tk()
    apply_base_theme(root)
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
