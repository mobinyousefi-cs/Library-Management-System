#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: models.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Dataclasses for domain entities: Book, Member, Loan.

Usage: 
from library_ms.models import Book, Member, Loan

Notes: 
- These are simple carriers; business rules live in services.py

===================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Book:
    id: Optional[int]
    isbn: str
    title: str
    author: str
    year: Optional[int] = None
    total_copies: int = 1
    available_copies: int = 1


@dataclass(slots=True)
class Member:
    id: Optional[int]
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


@dataclass(slots=True)
class Loan:
    id: Optional[int]
    book_id: int
    member_id: int
    loaned_at: datetime
    due_at: datetime
    returned_at: Optional[datetime] = None
