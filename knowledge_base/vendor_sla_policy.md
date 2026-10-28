# Punjab Sports Mart: Vendor SLA & Inventory Quality Policy
**Document ID:** POL-VEN-2026  
**Version:** 1.1  
**Effective Date:** 2026-03-01  
**Authority:** Supply Chain & Procurement  

## Section 1: Inventory Depletion & Reordering
1. When stock for any SKU reaches or drops below its `reorder_threshold`, the system flags a **P3 Medium** reorder alert.
2. The inventory manager must issue a Purchase Order to the designated primary vendor within 4 business hours.
3. If vendor lead time exceeds 3 days and current stock is less than 3 units, flag for expedited courier dispatch.

## Section 2: Defective Batch & Quality Escalation
1. If 3 or more complaints regarding product damage or seam splitting are registered within a rolling 7-day period for the same SKU/batch:
   - Mark as **P2 High** quality complaint.
   - Quarantine remaining inventory in the stockroom immediately.
   - Issue formal defect report to the vendor for credit note / batch replacement.

