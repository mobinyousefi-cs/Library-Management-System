#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: views_books.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Books management view: list/search/add/edit/delete books.

Usage: 
Used inside the main Tkinter Notebook.

Notes: 
- Validates ISBN lightly via utils.validators.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..services import LibraryService
from ..utils.validators import is_valid_isbn
from .widgets import LabeledEntry, ask_confirm, alert_error


class BooksView(ttk.Frame):
    def __init__(self, master: tk.Widget, service: LibraryService) -> None:
        super().__init__(master)
        self.service = service
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        # Search bar
        top = ttk.Frame(self)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        btn_search = ttk.Button(top, text="Search", command=self.refresh)
        btn_add = ttk.Button(top, text="Add", command=self._open_add)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        btn_search.pack(side=tk.LEFT, padx=(0, 8))
        btn_add.pack(side=tk.LEFT)
        top.pack(fill=tk.X, pady=(0, 8))

        # Table
        self.tree = ttk.Treeview(self, columns=("isbn", "title", "author", "year", "copies", "avail"), show="headings")
        for col, text in (
            ("isbn", "ISBN"),
            ("title", "Title"),
            ("author", "Author"),
            ("year", "Year"),
            ("copies", "Total"),
            ("avail", "Available"),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=100, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Actions
        btns = ttk.Frame(self)
        ttk.Button(btns, text="Edit", command=self._open_edit).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Delete", command=self._delete_selected).pack(side=tk.LEFT)
        btns.pack(anchor="e", pady=(8, 0))

    def refresh(self) -> None:
        q = self.search_var.get().strip() or None
        books = self.service.list_books(q)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for b in books:
            self.tree.insert("", tk.END, iid=str(b.id), values=(b.isbn, b.title, b.author, b.year or "", b.total_copies, b.available_copies))

    # --- Dialogs ---
    def _open_add(self) -> None:
        BookDialog(self, self.service, on_saved=self.refresh)

    def _open_edit(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        book_id = int(sel[0])
        BookDialog(self, self.service, book_id=book_id, on_saved=self.refresh)

    def _delete_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        book_id = int(sel[0])
        if ask_confirm("Delete Book", "Are you sure you want to delete this book?"):
            self.service.delete_book(book_id)
            self.refresh()


class BookDialog(tk.Toplevel):
    def __init__(self, master: tk.Widget, service: LibraryService, book_id: int | None = None, on_saved=None) -> None:
        super().__init__(master)
        self.service = service
        self.book_id = book_id
        self.on_saved = on_saved
        self.title("Add Book" if not book_id else "Edit Book")
        self.resizable(False, False)

        self.e_isbn = LabeledEntry(self, "ISBN:")
        self.e_title = LabeledEntry(self, "Title:")
        self.e_author = LabeledEntry(self, "Author:")
        self.e_year = LabeledEntry(self, "Year:")
        self.e_copies = LabeledEntry(self, "Copies:")
        for i, w in enumerate((self.e_isbn, self.e_title, self.e_author, self.e_year, self.e_copies)):
            w.grid(row=i, column=0, sticky="ew", padx=12, pady=4)

        btns = ttk.Frame(self)
        ttk.Button(btns, text="Save", command=self._save).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side=tk.LEFT)
        btns.grid(row=10, column=0, sticky="e", padx=12, pady=8)

        if book_id is not None:
            # Pre-fill from repo
            book = next((b for b in self.service.list_books() if b.id == book_id), None)
            if book:
                self.e_isbn.set(book.isbn)
                self.e_title.set(book.title)
                self.e_author.set(book.author)
                self.e_year.set(str(book.year or ""))
                self.e_copies.set(str(book.total_copies))

    def _save(self) -> None:
        isbn = self.e_isbn.get().strip()
        if not is_valid_isbn(isbn):
            alert_error("Please enter a valid ISBN-10 or ISBN-13.")
            return
        title = self.e_title.get().strip()
        author = self.e_author.get().strip()
        year = self.e_year.get().strip()
        copies = self.e_copies.get().strip()

        try:
            y = int(year) if year else None
            c = int(copies) if copies else 1
            if self.book_id is None:
                self.service.add_book(isbn=isbn, title=title, author=author, year=y, copies=c)
            else:
                self.service.update_book(self.book_id, isbn=isbn, title=title, author=author, year=y, total_copies=c)
            if callable(self.on_saved):
                self.on_saved()
            self.destroy()
        except ValueError as ex:
            alert_error(str(ex))
