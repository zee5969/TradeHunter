import pandas as pd
import streamlit as st

st.title("Dashboard")
st.caption("Overview of your lead discovery activity")

st.warning(
    "Sample data only. These numbers are placeholders until the database "
    "is connected in a later phase.",
    icon=":material/info:",
)

# --- Placeholder numbers (replaced by real database queries later) ---
SAMPLE_STATS = {
    "companies": 0,
    "saved": 0,
    "emails": 0,
    "phones": 0,
    "countries": 0,
}

SAMPLE_SEARCHES = pd.DataFrame(
    {
        "Product": ["Sportswear", "Football kits", "Cotton T-shirts"],
        "Country": ["United States", "Germany", "United Kingdom"],
        "Company type": ["Importer", "Wholesaler", "Distributor"],
        "Results": [0, 0, 0],
        "Date": ["Sample", "Sample", "Sample"],
    }
)

# --- Metric cards ---
col1, col2, col3 = st.columns(3)
col1.metric("Companies discovered", SAMPLE_STATS["companies"])
col2.metric("Saved leads", SAMPLE_STATS["saved"])
col3.metric("Countries searched", SAMPLE_STATS["countries"])

col4, col5, _ = st.columns(3)
col4.metric("Business emails found", SAMPLE_STATS["emails"])
col5.metric("Business phones found", SAMPLE_STATS["phones"])

st.divider()

# --- Recent searches ---
st.subheader("Recent searches")
st.dataframe(SAMPLE_SEARCHES, width="stretch", hide_index=True)