#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: views_loans.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Loans management view: list active loans, borrow and return.

Usage: 
Used inside the main Tkinter Notebook.

Notes: 
- Uses services for business rules.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import ttk

from ..services import LibraryService, DEFAULT_LOAN_DAYS
from .widgets import LabeledEntry, alert_error


class LoansView(ttk.Frame):
    def __init__(self, master: tk.Widget, service: LibraryService) -> None:
        super().__init__(master)
        self.service = service
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        # Borrow form
        form = ttk.LabelFrame(self, text="Borrow Book")
        self.e_book_id = LabeledEntry(form, "Book ID:", width=12)
        self.e_member_id = LabeledEntry(form, "Member ID:", width=12)
        self.e_days = LabeledEntry(form, "Days:", width=6)
        self.e_days.set(str(DEFAULT_LOAN_DAYS))
        self.e_book_id.grid(row=0, column=0, padx=8, pady=4, sticky="ew")
        self.e_member_id.grid(row=0, column=1, padx=8, pady=4, sticky="ew")
        self.e_days.grid(row=0, column=2, padx=8, pady=4, sticky="ew")
        ttk.Button(form, text="Borrow", command=self._borrow).grid(row=0, column=3, padx=8)
        form.pack(fill=tk.X, pady=(0, 8))

        # Active loans table
        self.tree = ttk.Treeview(self, columns=("loan_id", "book_id", "member_id", "loaned_at", "due_at"), show="headings")
        for col, text in (
            ("loan_id", "Loan ID"),
            ("book_id", "Book ID"),
            ("member_id", "Member ID"),
            ("loaned_at", "Loaned At"),
            ("due_at", "Due At"),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=100, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self, text="Return Selected", command=self._return_selected).pack(anchor="e", pady=(8, 0))

    def refresh(self) -> None:
        loans = self.service.list_loans(active_only=True)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for l in loans:
            self.tree.insert("", tk.END, iid=str(l.id), values=(l.id, l.book_id, l.member_id, l.loaned_at.strftime("%Y-%m-%d %H:%M"), l.due_at.strftime("%Y-%m-%d")))

    def _borrow(self) -> None:
        try:
            book_id = int(self.e_book_id.get())
            member_id = int(self.e_member_id.get())
            days = int(self.e_days.get())
            self.service.borrow_book(book_id, member_id, days)
            self.refresh()
        except ValueError as ex:
            alert_error(str(ex))

    def _return_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        loan_id = int(sel[0])
        self.service.return_book(loan_id)
        self.refresh()
