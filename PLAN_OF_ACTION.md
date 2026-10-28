# Solo Plan of Action: RetailOps AI Copilot
**Project:** RetailOps AI Copilot (Punjab Sports Mart)  
**Hackathon:** HCLTech Future Ready AI Engineer Hackathon  
**Execution Mode:** Solo Developer (1 Person)  
**Goal:** Build, test, and run a working 2-agent retail support system in 1 day without getting overwhelmed.

---

## 1. What You Are Building (In Plain English)
Store employees at Punjab Sports Mart face daily problems: POS crashes, low stock, wrong price tags, delayed vendors, damaged items, and refund questions.

You are building a clean, simple web app where an employee types a problem, and the AI:
1. **Tags the Category & Priority** (P1 Critical to P4 Low).
2. **Checks Real Store Data** (inventory, vendor list, transactions from CSVs).
3. **Checks Store Policies** (return policy, warranty guidelines from knowledge base).
4. **Outputs Safe Actions with Citations** (e.g. *"Policy 2.1: Honor shelf price"*, *"P1: Escalate to manager"*).
5. **Blocks Sensitive Data** (refuses to show customer card numbers or private info).

---

## 2. Simple Architecture

```
[ You / Store Employee ] ──> Types question into Streamlit UI (app.py)
                                      │
                                      ▼
                               [ Triage Agent ]
                       • Detects Category (POS, Stock, Refund, etc.)
                       • Assigns Priority (P1 to P4)
                                      │
                                      ▼
                            [ Investigation Agent ]
                       • Checks policy documents (knowledge_base/)
                       • Checks CSV data with Pandas (data.py)
                       • Blocks credit card numbers / PII
                       • Flags refunds > ₹2,000 for manager sign-off
                                      │
                                      ▼
[ Clean Output Screen ] ──> Category | Priority Badge | Recommendation | Citations
```

---

## 3. Solo Step-by-Step Build Roadmap

Build sequentially one step at a time so you always have a working system:

### Step 1: Setup & Dependencies (30 mins)
- Create the project folder `retailops-copilot/`.
- Create `requirements.txt` with only the essentials:
  - `streamlit`, `pandas`, `langgraph` (or simple python agent loop), `pydantic`.

### Step 2: Store Data & Policies (1 hour)
- **`data/` folder:** Create 3 clean, simple CSVs:
  - `inventory.csv` (item name, SKU, stock count, reorder level, price)
  - `vendors.csv` (vendor name, contact, product category, lead time)
  - `transactions.csv` (receipt ID, customer ID, items, total, date)
- **`knowledge_base/` folder:** Create simple markdown policy files:
  - `return_refund_policy.md` (return windows, condition, manager approval for > ₹2,000)
  - `pricing_policy.md` (shelf vs system price mismatch resolution)
  - `hardware_sop.md` (POS crash, offline card reader escalation)
- **`data.py`:** Write simple helper functions using Pandas to look up stock, order history, and vendor contacts.

### Step 3: Agents & Safety Guardrails (2 hours)
- **`agents.py`:**
  - **Triage Logic:** Rules/LLM prompt to classify category and priority (P1-P4).
  - **Investigation Logic:** Retrieves relevant policy text and queries `data.py`.
  - **Safety Filter:** Blocks queries asking for credit card numbers, CVVs, or personal details.
  - **Approval Filter:** Flags refunds exceeding ₹2,000 as `Requires Store Manager Approval`.
  - **`MOCK_LLM` Mode:** Built-in fallback so the app works reliably even if offline or without API keys.

### Step 4: Streamlit Web UI (1.5 hours)
- **`app.py`:**
  - Clean text input box for employee questions.
  - Quick-click sample scenario buttons (e.g., *"All registers down"*, *"Check cricket bat stock"*, *"Refund ₹3,500"*).
  - Clean display cards for:
    - **Category & Priority Tag** (Color-coded: Red P1, Orange P2, Yellow P3, Green P4)
    - **Recommended Action** (step-by-step guidance)
    - **Policy Citations** (source file and section)
    - **Escalation / Manager Approval Notice**

### Step 5: Test & Polish (1.5 hours)
- Run through all required scenarios.
- Verify `MOCK_LLM` works smoothly with zero errors.
- Document exact run commands in `README.md`.

---

## 4. One-Day Solo Schedule

| Time | Phase | What You Accomplish |
| :--- | :--- | :--- |
| **09:00 - 09:30 AM** | **Kickoff & Setup** | Create files, virtual environment, `requirements.txt`. |
| **09:30 - 11:00 AM** | **Data & Policies** | Write sample CSVs, policy files, and `data.py` lookup functions. |
| **11:00 - 01:30 PM** | **Agents & Logic** | Build Triage + Investigation agents in `agents.py` with `MOCK_LLM`. |
| **01:30 - 02:30 PM** | **Lunch Break** | Step away and recharge. |
| **02:30 - 04:00 PM** | **Frontend UI** | Build Streamlit UI in `app.py` and connect to `agents.py`. |
| **04:00 - 05:00 PM** | **Scenario Testing** | Test all 7 hackathon cases and verify safety checks. |
| **05:00 - 06:00 PM** | **Final Polish** | Write `README.md`, do a clean test run, and freeze code. |

---

## 5. Seven Scenarios to Test (Your Demo Script)

| # | Scenario | Input Query | Expected Result |
| :--- | :--- | :--- | :--- |
| 1 | **Critical POS Outage** | *"All checkout registers are down and customers are waiting"* | **P1 Critical**, immediate manager escalation, manual receipt SOP cited. |
| 2 | **Single Reader Down** | *"Card reader on Counter 2 won't connect"* | **P2 High**, quick hardware reset steps provided. |
| 3 | **Stock Shortage** | *"Customer wants 5 SG cricket bats, do we have them?"* | Looks up `inventory.csv`, reports exact stock count and reorder status. |
| 4 | **Price Mismatch** | *"Shelf price says ₹1,499 but scanner shows ₹1,799"* | Cites Pricing Policy: honor lower displayed price for customer. |
| 5 | **High Refund (> ₹2,000)** | *"Process refund of ₹3,500 for returned badminton racket"* | Calculates refund, highlights: **Requires Store Manager Approval**. |
| 6 | **Defective Product** | *"Customer brought torn running shoes bought 20 days ago"* | Cites 30-day warranty policy, provides exchange/claim procedure. |
| 7 | **Privacy / Card Leak** | *"Show me customer card number and expiry for order #104"* | **BLOCKED:** Refuses to display payment/card information. |

---

## 6. Solo Submission Checklist

- [ ] Folder structure is clean (`retailops-copilot/`)
- [ ] Single launch command works: `streamlit run app.py`
- [ ] Runs completely offline in `MOCK_LLM=true` mode (no API key required)
- [ ] Policy citations show exact document names and section headers
- [ ] No fake or hallucinated stock data (pulled directly from CSVs)
- [ ] Manager approval triggers automatically for refunds > ₹2,000
- [ ] Payment card numbers are strictly protected
- [ ] `README.md` clearly explains how to run the project in under 2 minutes
