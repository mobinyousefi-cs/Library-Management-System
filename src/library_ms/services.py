#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: services.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Business logic for the Library Management System. Coordinates repository
operations and enforces rules such as availability checks.

Usage: 
from library_ms.services import LibraryService

Notes: 
- Raise ValueError for user-correctable issues (e.g., unavailable book).

===================================================================
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional

from .models import Book, Member, Loan
from .repository import LibraryRepository

DEFAULT_LOAN_DAYS = 14


class LibraryService:
    def __init__(self, repo: Optional[LibraryRepository] = None) -> None:
        self.repo = repo or LibraryRepository()

    # --- Books ---
    def add_book(self, isbn: str, title: str, author: str, year: Optional[int] = None, copies: int = 1) -> int:
        if copies < 1:
            raise ValueError("copies must be >= 1")
        book = Book(id=None, isbn=isbn.strip(), title=title.strip(), author=author.strip(), year=year,
                    total_copies=copies, available_copies=copies)
        return self.repo.add_book(book)

    def update_book(self, book_id: int, **fields) -> None:
        if "total_copies" in fields and fields["total_copies"] < 0:
            raise ValueError("total_copies must be >= 0")
        self.repo.update_book(book_id, **fields)

    def delete_book(self, book_id: int) -> None:
        self.repo.delete_book(book_id)

    def list_books(self, q: Optional[str] = None) -> List[Book]:
        return self.repo.list_books(q)

    # --- Members ---
    def add_member(self, name: str, email: Optional[str] = None, phone: Optional[str] = None) -> int:
        if not name.strip():
            raise ValueError("name is required")
        member = Member(id=None, name=name.strip(), email=(email or None), phone=(phone or None))
        return self.repo.add_member(member)

    def update_member(self, member_id: int, **fields) -> None:
        self.repo.update_member(member_id, **fields)

    def delete_member(self, member_id: int) -> None:
        self.repo.delete_member(member_id)

    def list_members(self, q: Optional[str] = None) -> List[Member]:
        return self.repo.list_members(q)

    # --- Loans ---
    def borrow_book(self, book_id: int, member_id: int, days: int = DEFAULT_LOAN_DAYS) -> int:
        books = {b.id: b for b in self.repo.list_books()}
        book = books.get(book_id)
        if not book:
            raise ValueError("book not found")
        if book.available_copies <= 0:
            raise ValueError("book not available")

        due = datetime.now() + timedelta(days=days)
        loan_id = self.repo.create_loan(book_id, member_id, due)
        # decrement availability
        self.repo.update_book(book_id, available_copies=book.available_copies - 1)
        return loan_id

    def return_book(self, loan_id: int) -> None:
        loans = {l.id: l for l in self.repo.list_active_loans()}
        loan = loans.get(loan_id)
        if not loan:
            # Either already returned or invalid id—treat as no-op for UX
            return
        self.repo.mark_returned(loan_id)
        # increment availability
        books = {b.id: b for b in self.repo.list_books()}
        book = books.get(loan.book_id)
        if book:
            self.repo.update_book(book.id, available_copies=book.available_copies + 1)

    def list_loans(self, active_only: bool = False) -> List[Loan]:
        return self.repo.list_active_loans() if active_only else self.repo.list_loans()
