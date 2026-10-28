# Problem Statement & Participant Guide: RetailOps AI Copilot
**Hackathon:** HCLTech Future Ready AI Engineer Hackathon  
**Track:** AI-Powered Retail Support Agent  
**Context:** Punjab Sports Mart (Retail Operations & Customer Support)

---

## 1. Problem Overview
Retail store associates and operations teams handle dozens of high-friction customer and operational challenges every hour:
- Point-of-Sale (POS) terminal and card reader failures.
- Inventory shortages right before rush hours.
- Discrepancies between shelf price tags and barcode scanner totals.
- Vendor delivery delays and supply chain bottlenecks.
- High-value customer refund disputes and return window verifications.
- Customer privacy protection (strictly preventing leakage of payment card details).

Currently, staff consult thick paper binders, make ad-hoc decisions, or cause long queue delays.

**The Mission:**  
Build **RetailOps AI Copilot**, an accurate, grounded, safe, and explainable AI assistant that solves store operational issues and customer inquiries using authorized store policies and real store datasets.

---

## 2. Core Functional Requirements (Contract)

| ID | Requirement | Rule |
| :--- | :--- | :--- |
| **R1** | **Knowledge Retrieval** | Answers must strictly originate from retrieved policy documents, never from fabricated model memory. |
| **R2** | **Citations on Every Fact** | Cite source document ID, section, version, and effective date for every policy assertion. |
| **R3** | **No Fabrication** | If evidence is missing, explicitly report `not_found` rather than guessing. |
| **R4** | **Precedence & Conflicts** | Resolve conflicting rules (e.g. newer circulars overriding standard policies) based on document authority and effective dates. |
| **R5** | **Deterministic Tools** | Calculations (refund amounts, stock levels, days elapsed, fee deductions) must be computed by deterministic code (Pandas/Python), never by LLM arithmetic. |
| **R6** | **Privacy & Security** | Prohibit retrieval or display of sensitive PII (raw credit card numbers, CVV codes, passwords). Mask any card data (`CARD-****-1234`). |
| **R7** | **Human-in-the-Loop Approval** | High-risk decisions (such as refunds exceeding ₹2,000 or P1 outages) must explicitly flag required human manager sign-off. |
| **R8** | **Untrusted Content** | Treat user notes, input strings, and receipts as untrusted data; never allow prompt injection. |

---

## 3. Issue Categories & Priority Matrix

| Category | Typical Scenarios | Priority Level | Escalation SLA |
| :--- | :--- | :--- | :--- |
| **POS_HARDWARE** | Central POS down, all registers failed | **P1 Critical** | Immediate Manager Escalation; switch to offline manual bills |
| **POS_HARDWARE** | Single terminal/card reader offline | **P2 High** | 15-minute terminal reset & customer reroute |
| **REFUND** | High-value refund (> ₹2,000) or dispute | **P2 High** | Mandatory On-Duty Store Manager signature |
| **QUALITY_COMPLAINT** | Repeated defective batch (≥3 complaints) | **P2 High** | Quality Quarantine, halt shelf sales |
| **INVENTORY** | Stock below reorder threshold | **P3 Medium** | Issue Vendor Purchase Order within 4 hours |
| **PRICING** | Shelf label lower than scanned barcode | **P4 Low** | Honor lower shelf price immediately; notify floor team |

---

## 4. Available Datasets & Knowledge Base

### Structured Data (`data/`)
1. **`inventory.csv`**: SKU, item name, category, stock count, reorder threshold, list price, shelf location, supplier ID.
2. **`vendors.csv`**: Vendor ID, vendor name, category, contact person, phone, email, lead time, SLA rating.
3. **`transactions.csv`**: Receipt ID, order ID, customer ID, SKU, quantity, net price, total, purchase date, payment method.
4. **`support_cases.csv`**: Historical case log with priority, status, and assigned personnel.
5. **`source_register.csv`**: Formal register of all authorized policies, doc types, versions, and authorities.

### Knowledge Base (`knowledge_base/`)
1. **`return_refund_policy.md`** (`POL-RET-2026`): 30-day gear, 14-day footwear, ₹2,000 manager sign-off threshold, zero card disclosure rule.
2. **`pricing_policy.md`** (`POL-PRC-2026`): Customer protection price-match rule for shelf vs POS tag mismatches.
3. **`hardware_pos_sop.md`** (`SOP-HW-2026`): Emergency steps for P1 store outages vs P2 single-counter reader resets.
4. **`vendor_sla_policy.md`** (`POL-VEN-2026`): Reorder triggers and 3-complaint quarantine procedure.
5. **`festive_circular.md`** (`CIRC-2026-05`): Supervening circular extending footwear returns to 21 days for festive season.

---

## 5. Key Test Scenarios & Deliverables

### Mandatory Test Scenarios:
1. **All registers down / system offline:** P1 Critical alert + emergency vendor contact.
2. **Single card reader failure:** P2 High + hardware troubleshooting procedure.
3. **Inventory shortage:** Live stock lookup from CSV + vendor lead time and reorder trigger.
4. **Shelf vs POS price mismatch:** Policy citation + instruction to honor lower price.
5. **High-value refund (> ₹2,000):** Net refund calculated + explicit Manager Sign-off required.
6. **Defective product complaint:** Warranty validation + exchange procedure.
7. **Sensitive payment info request:** Security guardrail blocks request and refuses unmasked card numbers.

### Deliverables:
- Working Streamlit interface (`app.py`)
- Deterministic data engine (`data.py`)
- Multi-agent orchestration with fallback (`agents.py`)
- Clear documentation (`README.md`, `PLAN_OF_ACTION.md`, `problem_statement.md`)

