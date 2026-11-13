#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

latest = {}  # txn_id -> event with the latest ts

with open("payments.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        txn_id = event.get("txn_id")
        if not txn_id:
            continue
        ts = event.get("ts", "")
        # ISO timestamps compare correctly as strings
        if txn_id not in latest or ts > latest[txn_id].get("ts", ""):
            latest[txn_id] = event

total = 0.0
count = 0

for event in latest.values():
    if event.get("status") == "success":
        amount = event.get("amount", 0)
        if isinstance(amount, str):
            amount = amount.replace(",", "")
        try:
            total += float(amount)
            count += 1
        except (ValueError, TypeError):
            pass

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
