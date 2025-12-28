#!/usr/bin/env python3
"""
Форматирует JSON с поддержкой Unicode
"""
import json
import sys

data = json.load(sys.stdin)
print(json.dumps(data, ensure_ascii=False, indent=2))
