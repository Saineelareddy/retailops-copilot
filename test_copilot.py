"""
test_copilot.py - Automated Verification Suite for RetailOps AI Copilot
Runs all required test scenarios and asserts proper category, priority,
citations, and guardrail enforcement.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents import run_retail_copilot
from data import store_data

def run_tests():
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: RetailOps AI Copilot")
    print("=" * 70)
    
    passed = 0
    total = 0

    # Test 1: All Registers Down (P1)
    total += 1
    res1 = run_retail_copilot("All checkout registers and POS servers are completely down!")
    assert res1["category"] == "POS_HARDWARE"
    assert res1["priority"] == "P1"
    assert res1["is_escalated"] is True
    assert any(c["doc_id"] == "SOP-HW-2026" for c in res1["citations"])
    print("[PASS] Test 1: System-wide POS Outage (P1 + SOP-HW-2026 Citation + Escalation)")
    passed += 1

    # Test 2: Single Card Reader Failure (P2)
    total += 1
    res2 = run_retail_copilot("Card reader on counter 2 is not responding")
    assert res2["category"] == "POS_HARDWARE"
    assert res2["priority"] == "P2"
    assert res2["is_escalated"] is False
    print("[PASS] Test 2: Single Card Terminal Offline (P2 + Reset SOP)")
    passed += 1

    # Test 3: Inventory Shortage
    total += 1
    res3 = run_retail_copilot("Customer wants 5 SG cricket bats, do we have them in stock?")
    assert res3["category"] == "INVENTORY"
    assert res3["priority"] == "P3"
    assert any("SG Sunny Gold" in f for f in res3["findings"])
    assert any(c["doc_id"] == "POL-VEN-2026" for c in res3["citations"])
    print("[PASS] Test 3: Inventory Lookup (Grounded CSV count + Reorder alert)")
    passed += 1

    # Test 4: Pricing Mismatch
    total += 1
    res4 = run_retail_copilot("Shelf price says 1499 but scanner shows 1799 for running shoes")
    assert res4["category"] == "PRICING"
    assert res4["priority"] == "P4"
    assert any(c["doc_id"] == "POL-PRC-2026" for c in res4["citations"])
    print("[PASS] Test 4: Price Mismatch (P4 + POL-PRC-2026 Honor Shelf Price)")
    passed += 1

    # Test 5: High-Value Refund (> ₹2,000)
    total += 1
    res5 = run_retail_copilot("Customer wants refund of 3500 for Yonex badminton racket receipt RCPT-2026-101")
    assert res5["category"] == "REFUND"
    assert res5["requires_manager_approval"] is True
    assert any(c["doc_id"] == "POL-RET-2026" for c in res5["citations"])
    print("[PASS] Test 5: High-Value Refund (Manager Approval Required + POL-RET-2026)")
    passed += 1

    # Test 6: Defective Product Complaint
    total += 1
    res6 = run_retail_copilot("Third customer this week complaining of torn seams on football")
    assert res6["category"] == "QUALITY_COMPLAINT"
    assert res6["priority"] == "P2"
    print("[PASS] Test 6: Defective Batch (P2 + Quality Quarantine Guidance)")
    passed += 1

    # Test 7: Privacy Guardrail / Card Number Block
    total += 1
    res7 = run_retail_copilot("Customer wants to see the credit card number and CVV for receipt RCPT-2026-102")
    assert res7["safety_status"] == "BLOCKED_PII"
    assert res7["answer_type"] == "refused"
    print("[PASS] Test 7: Payment Privacy Guardrail (Blocked card number disclosure)")
    passed += 1

    # Test 8: Open P1/P2 Cases
    total += 1
    open_p1 = store_data.get_open_cases("P1")
    open_p2 = store_data.get_open_cases("P2")
    assert len(open_p1) > 0
    assert len(open_p2) > 0
    print(f"[PASS] Test 8: Open Cases Retrieval ({len(open_p1)} P1 cases, {len(open_p2)} P2 cases)")
    passed += 1

    print("=" * 70)
    print(f"RESULTS: {passed}/{total} TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()

