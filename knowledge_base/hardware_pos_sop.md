# Punjab Sports Mart: POS Hardware & Outage Standard Operating Procedure (SOP)
**Document ID:** SOP-HW-2026  
**Version:** 2.0  
**Effective Date:** 2026-02-15  
**Authority:** Store IT & Infrastructure  

## Section 1: System-Wide Outage (Priority 1 - Critical)
**Condition:** ALL registers are down, store network is offline, or the central POS server crashes.
1. **Immediate Escalation:** Trigger **P1 Critical**. Immediately inform the Store Manager.
2. **Vendor Contact:** Contact FastPOS Emergency Helpdesk at `+91-9876543299` (Vendor ID: VEND-999).
3. **Store Continuity:** Activate offline manual carbon-copy receipt books. Do NOT stop customers from billing offline.
4. **Broadcast:** Display temporary polite notices at queue entrances.

## Section 2: Single Counter / Card Terminal Issue (Priority 2 - High)
**Condition:** A single card reader or receipt printer at one counter fails while other counters remain operational.
1. **Priority Level:** Classified as **P2 High**.
2. **Troubleshooting Steps:**
   - Power cycle the EDC card reader (hold power button for 10 seconds).
   - Verify Ethernet/Wi-Fi connection indicator light is steady green.
   - Redirect waiting customers to the adjacent operational counter.
   - Log an internal ticket (`CASE-HW-xxx`) with IT support.

