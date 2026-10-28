"""
data.py - RetailOps AI Copilot Data Access & Analytics Engine
Loads and analyzes store CSV datasets using Pandas / standard csv reader with deterministic verification.
Clearly labeled demo data for Punjab Sports Mart.
"""

import os
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Directory setup
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Optional pandas with graceful standard library fallback
try:
    import pandas as pd
    HAS_PANDAS = True
except (Exception, ImportError, BaseException):
    pd = None
    HAS_PANDAS = False


def _read_csv_records(file_path: Path) -> List[Dict[str, Any]]:
    """Helper to read CSV files while ignoring comment lines."""
    records = []
    if not file_path.exists():
        return records
    
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        lines = [line for line in f if not line.strip().startswith("#")]
        if not lines:
            return records
        reader = csv.DictReader(lines)
        for row in reader:
            records.append({k.strip(): v.strip() for k, v in row.items() if k is not None})
    return records


class RetailDataStore:
    """Provides validated and grounded access to store data files."""
    
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.inventory_records: List[Dict[str, Any]] = []
        self.vendors_records: List[Dict[str, Any]] = []
        self.transactions_records: List[Dict[str, Any]] = []
        self.cases_records: List[Dict[str, Any]] = []
        self.register_records: List[Dict[str, Any]] = []
        self.load_all()
        
    def load_all(self):
        """Loads all CSV datasets into memory."""
        # 1. Inventory
        raw_inv = _read_csv_records(self.data_dir / "inventory.csv")
        self.inventory_records = []
        for r in raw_inv:
            item = dict(r)
            item["stock_quantity"] = int(r.get("stock_quantity", 0))
            item["reorder_threshold"] = int(r.get("reorder_threshold", 0))
            item["list_price"] = float(r.get("list_price", 0.0))
            item["is_low_stock"] = item["stock_quantity"] <= item["reorder_threshold"]
            self.inventory_records.append(item)
            
        # 2. Vendors
        raw_ven = _read_csv_records(self.data_dir / "vendors.csv")
        self.vendors_records = []
        for r in raw_ven:
            item = dict(r)
            item["lead_time_days"] = int(r.get("lead_time_days", 0))
            item["sla_rating"] = float(r.get("sla_rating", 0.0))
            self.vendors_records.append(item)
            
        # 3. Transactions & Receipts
        raw_tx = _read_csv_records(self.data_dir / "transactions.csv")
        self.transactions_records = []
        for r in raw_tx:
            item = dict(r)
            item["qty"] = int(r.get("qty", 1))
            item["net_unit_price"] = float(r.get("net_unit_price", 0.0))
            item["total_amount"] = float(r.get("total_amount", 0.0))
            self.transactions_records.append(item)
            
        # 4. Support Cases
        self.cases_records = _read_csv_records(self.data_dir / "support_cases.csv")
        
        # 5. Source Register
        self.register_records = _read_csv_records(self.data_dir / "source_register.csv")

    def search_inventory(self, query: str = "") -> List[Dict[str, Any]]:
        """Search inventory by product name, SKU, or category."""
        q = query.strip().lower()
        if not q:
            return list(self.inventory_records)
        
        results = []
        for item in self.inventory_records:
            if (q in item["name"].lower() or 
                q in item["sku"].lower() or 
                q in item["category"].lower()):
                results.append(item)
        return results

    def get_product_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """Exact lookup by SKU."""
        cleaned = sku.strip().upper()
        for item in self.inventory_records:
            if item["sku"].upper() == cleaned:
                return item
        return None

    def get_vendor_for_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """Find the supplier information for a given SKU."""
        product = self.get_product_by_sku(sku)
        if not product or "supplier_id" not in product:
            return None
        
        supplier_id = product["supplier_id"]
        for v in self.vendors_records:
            if v["vendor_id"] == supplier_id:
                return v
        return None

    def get_emergency_pos_vendor(self) -> Optional[Dict[str, Any]]:
        """Emergency contact for POS hardware failure."""
        for v in self.vendors_records:
            if v["vendor_id"] == "VEND-999":
                return v
        return None

    def get_receipt(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Lookup order or receipt by ID, ensuring payment card details are masked."""
        cleaned_id = identifier.strip().upper()
        for tx in self.transactions_records:
            if tx.get("receipt_id", "").upper() == cleaned_id or tx.get("order_id", "").upper() == cleaned_id:
                data = dict(tx)
                # Strict Privacy Check: Never expose raw payment details
                pm = str(data.get("payment_method", ""))
                if "CARD" in pm and not pm.startswith("CARD-****-"):
                    data["payment_method"] = "CARD-****-" + pm[-4:]
                return data
        return None

    def calculate_refund(self, receipt_id: str, return_date: str = "2026-10-28") -> Dict[str, Any]:
        """
        Calculates refund amount deterministically and checks policy approval thresholds.
        Manager sign-off threshold is ₹2,000.00.
        """
        receipt = self.get_receipt(receipt_id)
        if not receipt:
            return {
                "success": False,
                "error": f"Receipt/Order ID '{receipt_id}' not found in records."
            }
        
        total_amount = float(receipt.get("total_amount", 0.0))
        
        # Calculate days elapsed
        try:
            p_dt = datetime.strptime(receipt["purchase_date"], "%Y-%m-%d")
            r_dt = datetime.strptime(return_date, "%Y-%m-%d")
            days_elapsed = (r_dt - p_dt).days
        except Exception:
            days_elapsed = 0
            
        requires_manager_approval = bool(total_amount > 2000.00)
        
        return {
            "success": True,
            "receipt_id": receipt["receipt_id"],
            "order_id": receipt["order_id"],
            "sku": receipt["sku"],
            "item_name": receipt["item_name"],
            "purchase_date": receipt["purchase_date"],
            "days_elapsed": days_elapsed,
            "gross_amount": total_amount,
            "net_refund_amount": total_amount,
            "requires_manager_approval": requires_manager_approval,
            "approval_threshold": 2000.00,
            "policy_rule_id": "POL-RET-2026-SEC-3"
        }

    def get_open_cases(self, priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve recent support cases, optionally filtered by priority (P1/P2/P3/P4)."""
        if not priority:
            return list(self.cases_records)
        
        p = priority.strip().upper()
        return [c for c in self.cases_records if c.get("priority", "").upper() == p]

    def get_quality_complaints_count(self, sku_or_item: str) -> int:
        """Count quality complaints for a given item or SKU."""
        q = sku_or_item.strip().lower()
        count = 0
        for c in self.cases_records:
            if (c.get("category", "").upper() == "QUALITY_COMPLAINT" and
                q in c.get("issue_description", "").lower()):
                count += 1
        return count

    def get_source_register(self) -> List[Dict[str, Any]]:
        """Return the source register metadata."""
        return list(self.register_records)

# Singleton instance
store_data = RetailDataStore()
