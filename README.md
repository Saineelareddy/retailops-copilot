# RetailOps AI Copilot (Punjab Sports Mart)

An AI-powered operational assistant engineered for **Punjab Sports Mart** store associates and managers to resolve store outages, inventory shortages, price discrepancies, vendor delays, defective products, and customer refund claims.

Built for the **HCLTech Future Ready AI Engineer Hackathon**.

---

## 🌟 Key Capabilities
- **2-Agent LangGraph Architecture:** Fast triage (category & priority P1–P4) followed by grounded policy investigation and data retrieval.
- **Strict Guardrails & Privacy:** Refuses requests for unmasked customer payment cards or CVVs (`POL-RET-2026 Section 4`).
- **Deterministic Refund Logic:** Automatically flags refunds exceeding ₹2,000 for mandatory Store Manager sign-off.
- **Offline / Grounded Reliability:** Runs in `MOCK_LLM` mode with zero external API dependencies or unexpected downtime.
- **Auditable & Cited:** Every policy decision cites exact document ID, section, and version.

---

## 📂 Project Structure

```
retailops-copilot/
├── problem_statement.md    # Hackathon problem, categories, priority SLAs & deliverables
├── PLAN_OF_ACTION.md       # Solo developer execution plan & schedule
├── app.py                  # Streamlit web interface with quick-test buttons
├── data.py                 # Grounded data engine (Pandas/CSV lookup for inventory, receipts, vendors)
├── agents.py               # LangGraph 2-agent workflow with safety filters
├── requirements.txt        # Minimal required dependencies
├── README.md               # Setup & execution instructions
├── data/                   # Store datasets
│   ├── inventory.csv       # Stock levels, reorder thresholds, shelf locations
│   ├── vendors.csv         # Vendor contact details, SLAs, lead times
│   ├── transactions.csv    # POS receipts, customer IDs, masked payment info
│   ├── support_cases.csv   # Historical support tickets with P1–P4 priorities
│   └── source_register.csv # Register of authorized store policies (Annex B)
└── knowledge_base/         # Store SOPs & policies
    ├── return_refund_policy.md   # Return windows & ₹2,000 manager sign-off threshold
    ├── pricing_policy.md         # Shelf vs POS price match customer protection rule
    ├── hardware_pos_sop.md       # P1 store outage vs P2 card reader reset SOP
    ├── vendor_sla_policy.md      # Stock reorder & defective product quarantine policy
    └── festive_circular.md       # Festive season return window extension notice
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or 3.11 installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
From the `retailops-copilot` folder:
```bash
streamlit run app.py
```
Or, if running with the local virtual environment:
```powershell
& "C:\Users\saine\OneDrive\Documents\New folder\python_env\python.exe" -m streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧪 Verified Test Scenarios

The web interface includes **Quick Test Scenario Buttons** in the sidebar to test:
1. **Critical POS Outage (P1):** All registers down $\rightarrow$ Escalates to manager, calls FastPOS emergency desk, switches to manual receipts.
2. **Single Reader Failure (P2):** Counter 2 card terminal down $\rightarrow$ Guides 10-second power cycle and reroutes customer.
3. **Inventory Shortage (P3):** Stock check on SG cricket bats $\rightarrow$ Pulls real inventory count (2 in stock), triggers reorder warning with supplier contact.
4. **Price Mismatch (P4):** Shelf price lower than barcode $\rightarrow$ Cites `POL-PRC-2026` to honor the lower price immediately.
5. **High-Value Refund (> ₹2,000):** Customer refund of ₹3,500 $\rightarrow$ Flags mandatory on-duty Store Manager sign-off.
6. **Defective Batch Complaint:** Repeated torn seams on footballs $\rightarrow$ Recommends quarantine and vendor credit claim under `POL-VEN-2026`.
7. **Payment Privacy Guardrail:** Request to reveal card number $\rightarrow$ **Blocked** by security filter under `POL-RET-2026 Section 4`.
8. **Open Incidents:** Displays live overview of open P1 and P2 cases.

---

## 🔒 Known Limitations & Next Steps
- **LLM Provider:** Currently defaults to `MOCK_LLM` mode for fast, offline, and reliable evaluation without external API keys. Local Ollama (e.g. `llama3.1:8b`) can be connected directly to `agents.py` if desired.
- **Receipt Entry:** Currently looks up receipts by ID or query text; in production, this can connect directly to an active POS SQL database.

