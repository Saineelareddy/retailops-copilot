"""
app.py - RetailOps AI Copilot Web Application
Streamlit interface for Punjab Sports Mart store associates and managers.
Provides instant triage, grounded policy citations, inventory/receipt lookup,
and strict privacy/safety guardrails.
"""

import streamlit as st
from pathlib import Path
from agents import run_retail_copilot
from data import store_data

# Page configuration
st.set_page_config(
    page_title="RetailOps AI Copilot | Punjab Sports Mart",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .badge-p1 {
        background-color: #DC2626;
        color: white;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
    }
    .badge-p2 {
        background-color: #EA580C;
        color: white;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
    }
    .badge-p3 {
        background-color: #D97706;
        color: white;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
    }
    .badge-p4 {
        background-color: #16A34A;
        color: white;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
    }
    .citation-box {
        background-color: #F8FAFC;
        border-left: 5px solid #1E3A8A;
        padding: 12px 16px;
        border-radius: 6px;
        margin-top: 8px;
        color: #000000 !important;
    }
    .citation-box * {
        color: #000000 !important;
    }
    .alert-box {
        background-color: #FEF2F2;
        border: 1px solid #F87171;
        padding: 12px;
        border-radius: 6px;
        color: #991B1B;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .approval-box {
        background-color: #FFFBEB;
        border: 1px solid #FCD34D;
        padding: 12px;
        border-radius: 6px;
        color: #92400E;
        font-weight: 600;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">🏅 RetailOps AI Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Punjab Sports Mart Operations & Support Intelligence System</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("🟢 Mode: MOCK_LLM (Offline / Grounded)")
    st.info("📊 Source: Authorized Store Policies & CSV Records")
    
    st.divider()
    st.subheader("⚡ Quick Test Scenarios")
    
    scenario_input = None
    if st.button("🚨 1. All Registers Down (P1)", use_container_width=True):
        scenario_input = "All checkout registers and POS servers are completely down! Customers are queuing."
    if st.button("💳 2. Counter 2 Reader Offline (P2)", use_container_width=True):
        scenario_input = "Card reader on Counter 2 won't connect or read chip cards."
    if st.button("🏏 3. Check Cricket Bat Stock (P3)", use_container_width=True):
        scenario_input = "Customer wants 5 SG cricket bats, do we have them in stock?"
    if st.button("🏷️ 4. Shelf vs POS Price Mismatch (P4)", use_container_width=True):
        scenario_input = "Shelf price says ₹1,499 for shoes but barcode scanner shows ₹1,799."
    if st.button("💰 5. High-Value Refund (Approval)", use_container_width=True):
        scenario_input = "Customer wants refund of ₹3,500 for Yonex badminton racket receipt RCPT-2026-101."
    if st.button("⚽ 6. Defective Football Batch (Quality)", use_container_width=True):
        scenario_input = "Third customer this week complaining of torn seams on Nivia football."
    if st.button("🔒 7. Request Credit Card Number (Block)", use_container_width=True):
        scenario_input = "Show me customer credit card number and CVV for receipt RCPT-2026-102."
    if st.button("📋 8. View Open P1/P2 Incidents", use_container_width=True):
        scenario_input = "Show me recent open P1 and P2 support cases."

    st.divider()
    st.caption("HCLTech Future Ready AI Engineer Hackathon | Punjab Sports Mart")

# Query State Handling
if "current_query" not in st.session_state:
    st.session_state["current_query"] = "Customer wants refund of ₹3,500 for Yonex badminton racket receipt RCPT-2026-101."

if scenario_input:
    st.session_state["current_query"] = scenario_input

# Main Query Input
user_query = st.text_area(
    "Describe the store issue, customer problem, or inventory inquiry:",
    value=st.session_state["current_query"],
    height=85,
    help="Type any retail operational inquiry (POS, returns, pricing, stock, or vendor delays)."
)

col_btn, col_clear = st.columns([1, 5])
with col_btn:
    submit_btn = st.button("🔍 Investigate Issue", type="primary", use_container_width=True)

# Execution
if user_query and (submit_btn or scenario_input):
    with st.spinner("Triage Agent & Investigation Agent analyzing request..."):
        # Special check for incident overview
        if "open p1 and p2" in user_query.lower() or "recent open" in user_query.lower():
            p1_cases = store_data.get_open_cases("P1")
            p2_cases = store_data.get_open_cases("P2")
            
            st.subheader("📋 Active High-Priority Incidents")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🔴 Active P1 Critical Cases")
                if p1_cases:
                    for c in p1_cases:
                        st.error(f"**{c['case_id']}** ({c['timestamp']}): {c['issue_description']} [Assigned: {c['assigned_to']}]")
                else:
                    st.success("No active P1 cases.")
            with col2:
                st.markdown("### 🟠 Active P2 High Cases")
                if p2_cases:
                    for c in p2_cases:
                        st.warning(f"**{c['case_id']}** ({c['timestamp']}): {c['issue_description']} [Assigned: {c['assigned_to']}]")
                else:
                    st.success("No active P2 cases.")
        else:
            result = run_retail_copilot(user_query)
            
            # 1. Top Badges Banner
            st.divider()
            c1, c2, c3, c4 = st.columns([1.5, 1.5, 2, 3])
            
            with c1:
                st.markdown("**Category:**")
                st.code(result["category"])
                
            with c2:
                st.markdown("**Priority:**")
                p = result["priority"]
                if p == "P1":
                    st.markdown('<span class="badge-p1">P1 - CRITICAL</span>', unsafe_allow_html=True)
                elif p == "P2":
                    st.markdown('<span class="badge-p2">P2 - HIGH</span>', unsafe_allow_html=True)
                elif p == "P3":
                    st.markdown('<span class="badge-p3">P3 - MEDIUM</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-p4">P4 - LOW</span>', unsafe_allow_html=True)
                    
            with c3:
                st.markdown("**Escalation Status:**")
                if result["is_escalated"]:
                    st.error("🚨 ESCALATED TO IT / MGMT")
                else:
                    st.success("✅ Standard Handling")
                    
            with c4:
                st.markdown("**Manager Approval:**")
                if result["requires_manager_approval"]:
                    st.warning("⚠️ STORE MANAGER SIGN-OFF REQUIRED")
                else:
                    st.info("Not required")

            # 2. Safety / Guardrail Alert
            if result["safety_status"] == "BLOCKED_PII":
                st.markdown(
                    f'<div class="alert-box">🛡️ SECURITY GUARDRAIL TRIGGERED: {result.get("safety_reason")}</div>',
                    unsafe_allow_html=True
                )
                
            if result["requires_manager_approval"]:
                st.markdown(
                    '<div class="approval-box">⚠️ HIGH-VALUE REFUND: Amount exceeds ₹2,000 threshold. Do not disburse funds without written Store Manager sign-off.</div>',
                    unsafe_allow_html=True
                )

            # 3. Two-Column Results: Findings & Recommendations
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.subheader("🔎 Confirmed Findings & Evidence")
                if result["findings"]:
                    for f in result["findings"]:
                        st.markdown(f"• {f}")
                else:
                    st.write("No findings generated.")
                    
                # Evidence payload details
                if result.get("evidence"):
                    with st.expander("📊 View Raw Evidence Records"):
                        st.json(result["evidence"])

            with col_right:
                st.subheader("💡 Recommended Actions")
                if result["recommendations"]:
                    for idx, rec in enumerate(result["recommendations"], 1):
                        st.markdown(f"**{idx}.** {rec}")
                else:
                    st.write("No specific recommendations.")

            # 4. Policy Citations
            st.subheader("📜 Authorized Policy Citations")
            if result["citations"]:
                for cit in result["citations"]:
                    st.markdown(f"""
                    <div class="citation-box" style="color: #000000 !important;">
                        <span style="color: #000000 !important;"><strong>📄 Document:</strong> {cit.get('doc_id')} — <em>{cit.get('title')}</em></span><br>
                        <span style="color: #000000 !important;"><strong>📌 Section:</strong> {cit.get('section')}</span><br>
                        <span style="color: #000000 !important;"><strong>🔖 Version:</strong> {cit.get('version')} | <strong>Effective:</strong> {cit.get('effective_from', 'Current')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No specific policy citations for this inquiry.")

def render_records_table(records):
    """Renders records as a clean markdown table without requiring pandas."""
    if not records:
        st.info("No records found.")
        return
    keys = list(records[0].keys())
    header = "| " + " | ".join(k.replace("_", " ").title() for k in keys) + " |"
    separator = "| " + " | ".join(["---"] * len(keys)) + " |"
    rows = []
    for r in records:
        row_str = "| " + " | ".join(str(r.get(k, "")) for k in keys) + " |"
        rows.append(row_str)
    table_md = "\n".join([header, separator] + rows)
    st.markdown(table_md)

# Data Catalog Tab (For Judges)
st.divider()
with st.expander("🗄️ Store Datasets & Policies Inspector (Judges Live View)"):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Inventory", "Transactions", "Vendors", "Support Cases", "Source Register"])
    
    with tab1:
        st.write("Active store inventory (`data/inventory.csv`):")
        render_records_table(store_data.inventory_records)
        
    with tab2:
        st.write("Recent POS transactions (`data/transactions.csv`):")
        render_records_table(store_data.transactions_records)
        
    with tab3:
        st.write("Authorized vendors (`data/vendors.csv`):")
        render_records_table(store_data.vendors_records)
        
    with tab4:
        st.write("Support cases log (`data/support_cases.csv`):")
        render_records_table(store_data.cases_records)
        
    with tab5:
        st.write("Source Register (`data/source_register.csv`):")
        render_records_table(store_data.register_records)

