#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: views_members.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Members management view: list/search/add/edit/delete members.

Usage: 
Used inside the main Tkinter Notebook.

Notes: 
- Minimal validation (name required). Extend as needed.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..services import LibraryService
from .widgets import LabeledEntry, ask_confirm, alert_error


class MembersView(ttk.Frame):
    def __init__(self, master: tk.Widget, service: LibraryService) -> None:
        super().__init__(master)
        self.service = service
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        top = ttk.Frame(self)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        btn_search = ttk.Button(top, text="Search", command=self.refresh)
        btn_add = ttk.Button(top, text="Add", command=self._open_add)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        btn_search.pack(side=tk.LEFT, padx=(0, 8))
        btn_add.pack(side=tk.LEFT)
        top.pack(fill=tk.X, pady=(0, 8))

        self.tree = ttk.Treeview(self, columns=("name", "email", "phone"), show="headings")
        for col, text in (("name", "Name"), ("email", "Email"), ("phone", "Phone")):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=160, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btns = ttk.Frame(self)
        ttk.Button(btns, text="Edit", command=self._open_edit).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Delete", command=self._delete_selected).pack(side=tk.LEFT)
        btns.pack(anchor="e", pady=(8, 0))

    def refresh(self) -> None:
        q = self.search_var.get().strip() or None
        members = self.service.list_members(q)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in members:
            self.tree.insert("", tk.END, iid=str(m.id), values=(m.name, m.email or "", m.phone or ""))

    def _open_add(self) -> None:
        MemberDialog(self, self.service, on_saved=self.refresh)

    def _open_edit(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        member_id = int(sel[0])
        MemberDialog(self, self.service, member_id=member_id, on_saved=self.refresh)

    def _delete_selected(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        member_id = int(sel[0])
        if ask_confirm("Delete Member", "Are you sure you want to delete this member?"):
            self.service.delete_member(member_id)
            self.refresh()


class MemberDialog(tk.Toplevel):
    def __init__(self, master: tk.Widget, service: LibraryService, member_id: int | None = None, on_saved=None) -> None:
        super().__init__(master)
        self.service = service
        self.member_id = member_id
        self.on_saved = on_saved
        self.title("Add Member" if not member_id else "Edit Member")
        self.resizable(False, False)

        self.e_name = LabeledEntry(self, "Name:")
        self.e_email = LabeledEntry(self, "Email:")
        self.e_phone = LabeledEntry(self, "Phone:")
        for i, w in enumerate((self.e_name, self.e_email, self.e_phone)):
            w.grid(row=i, column=0, sticky="ew", padx=12, pady=4)

        btns = ttk.Frame(self)
        ttk.Button(btns, text="Save", command=self._save).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side=tk.LEFT)
        btns.grid(row=10, column=0, sticky="e", padx=12, pady=8)

        if member_id is not None:
            member = next((m for m in self.service.list_members() if m.id == member_id), None)
            if member:
                self.e_name.set(member.name)
                self.e_email.set(member.email or "")
                self.e_phone.set(member.phone or "")

    def _save(self) -> None:
        name = self.e_name.get().strip()
        email = self.e_email.get().strip() or None
        phone = self.e_phone.get().strip() or None
        try:
            if not name:
                raise ValueError("name is required")
            if self.member_id is None:
                self.service.add_member(name=name, email=email, phone=phone)
            else:
                self.service.update_member(self.member_id, name=name, email=email, phone=phone)
            if callable(self.on_saved):
                self.on_saved()
            self.destroy()
        except ValueError as ex:
            alert_error(str(ex))
