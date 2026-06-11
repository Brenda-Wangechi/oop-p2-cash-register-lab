#!/usr/bin/env python3
"""Top-level compatibility module.

Tests import `cash_register` (module name). The real implementation
is in `lib/cash_register.py`. Re-export `CashRegister` here so imports
like `from cash_register import CashRegister` work regardless of
PYTHONPATH differences.
"""
from lib.cash_register import CashRegister

__all__ = ["CashRegister"]
