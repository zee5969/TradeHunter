import streamlit as st

st.title("Import/Export Research")
st.caption("Separate general business discovery from verified trade activity")

st.info(
    "This module will be built after company discovery (Phase 3) is working. "
    "Below is how evidence will be labeled.",
    icon=":material/info:",
)

st.subheader("Evidence status labels")

st.markdown(
    """
| Status | Meaning |
|---|---|
| **Not verified** | The company was found by search. Nothing shows it imports or exports. |
| **Stated on website** | The company's own page mentions importing, exporting or distribution. The source link is shown. |
| **Verified by trade records** | Confirmed by shipment or customs data from a licensed provider. |
"""
)

st.warning(
    "A company is never labeled an importer or exporter based only on its "
    "name or industry. Verified trade records require a paid trade-data "
    "provider; the free prototype cannot confirm them.",
    icon=":material/gavel:",
)