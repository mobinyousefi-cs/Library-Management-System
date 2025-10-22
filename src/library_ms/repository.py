#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: repository.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Repository layer encapsulating CRUD operations for books, members, and loans.

Usage: 
from library_ms.repository import LibraryRepository

Notes: 
- Uses parameterized queries to prevent SQL injection.

===================================================================
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, List, Optional, Tuple

from .db import get_connection
from .models import Book, Member, Loan


class LibraryRepository:
    """Thin CRUD wrapper around sqlite.

    Keep it simple so higher layers (services) can be unit-tested via this API.
    """

    # --- Books ---
    def add_book(self, book: Book) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO books(isbn, title, author, year, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (book.isbn, book.title, book.author, book.year, book.total_copies, book.available_copies),
            )
            return int(cur.lastrowid)

    def update_book(self, book_id: int, **fields: Any) -> None:
        if not fields:
            return
        cols = ", ".join(f"{k}=?" for k in fields)
        values = list(fields.values())
        values.append(book_id)
        with get_connection() as conn:
            conn.execute(f"UPDATE books SET {cols}, updated_at=datetime('now') WHERE id=?", values)

    def delete_book(self, book_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM books WHERE id=?", (book_id,))

    def get_book(self, book_id: int) -> Optional[Book]:
        with get_connection() as conn:
            cur = conn.execute(
                "SELECT id, isbn, title, author, year, total_copies, available_copies FROM books WHERE id=?",
                (book_id,),
            )
            row = cur.fetchone()
        return Book(*row) if row else None

    def list_books(self, q: Optional[str] = None) -> List[Book]:
        sql = "SELECT id, isbn, title, author, year, total_copies, available_copies FROM books"
        params: Tuple[Any, ...] = ()
        if q:
            sql += " WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?"
            params = (f"%{q}%", f"%{q}%", f"%{q}%")
        sql += " ORDER BY title COLLATE NOCASE"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Book(*r) for r in rows]

    # --- Members ---
    def add_member(self, member: Member) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO members(name, email, phone) VALUES(?, ?, ?)",
                (member.name, member.email, member.phone),
            )
            return int(cur.lastrowid)

    def update_member(self, member_id: int, **fields: Any) -> None:
        if not fields:
            return
        cols = ", ".join(f"{k}=?" for k in fields)
        values = list(fields.values())
        values.append(member_id)
        with get_connection() as conn:
            conn.execute(f"UPDATE members SET {cols}, updated_at=datetime('now') WHERE id=?", values)

    def delete_member(self, member_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM members WHERE id=?", (member_id,))

    def get_member(self, member_id: int) -> Optional[Member]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, name, email, phone FROM members WHERE id=?",
                (member_id,),
            ).fetchone()
        return Member(*row) if row else None

    def list_members(self, q: Optional[str] = None) -> List[Member]:
        sql = "SELECT id, name, email, phone FROM members"
        params: Tuple[Any, ...] = ()
        if q:
            sql += " WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?"
            params = (f"%{q}%", f"%{q}%", f"%{q}%")
        sql += " ORDER BY name COLLATE NOCASE"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Member(*r) for r in rows]

    # --- Loans ---
    def create_loan(self, book_id: int, member_id: int, due_at: datetime) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO loans(book_id, member_id, due_at) VALUES(?, ?, ?)",
                (book_id, member_id, due_at.isoformat(timespec="seconds")),
            )
            return int(cur.lastrowid)

    def mark_returned(self, loan_id: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE loans SET returned_at=datetime('now') WHERE id=? AND returned_at IS NULL",
                (loan_id,),
            )

    def list_active_loans(self) -> List[Loan]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, book_id, member_id, loaned_at, due_at, returned_at
                FROM loans
                WHERE returned_at IS NULL
                ORDER BY loaned_at DESC
                """
            ).fetchall()
        return [self._row_to_loan(r) for r in rows]

    def list_loans(self) -> List[Loan]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, book_id, member_id, loaned_at, due_at, returned_at FROM loans ORDER BY loaned_at DESC"
            ).fetchall()
        return [self._row_to_loan(r) for r in rows]

    @staticmethod
    def _row_to_loan(r: Iterable) -> Loan:
        id_, book_id, member_id, loaned_at, due_at, returned_at = r
        return Loan(
            id=id_,
            book_id=book_id,
            member_id=member_id,
            loaned_at=datetime.fromisoformat(loaned_at),
            due_at=datetime.fromisoformat(due_at),
            returned_at=datetime.fromisoformat(returned_at) if returned_at else None,
        )
