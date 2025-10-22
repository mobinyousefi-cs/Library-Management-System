#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Library Management System 
File: validators.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-22 
Updated: 2025-10-22 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Small validation helpers for inputs used by the Tkinter UI.

Usage: 
from library_ms.utils.validators import is_valid_isbn

Notes: 
- These are intentionally permissive for demo purposes.

===================================================================
"""
from __future__ import annotations

import re


_ISBN10 = re.compile(r"^\d{9}[\dXx]$")
_ISBN13 = re.compile(r"^\d{13}$")


def is_valid_isbn(value: str) -> bool:
    v = (value or "").replace("-", "").strip()
    return bool(_ISBN10.match(v) or _ISBN13.match(v))
