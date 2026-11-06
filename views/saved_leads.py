import pandas as pd
import streamlit as st

COMPANY_TYPES = [
    "All",
    "Importer",
    "Exporter",
    "Wholesaler",
    "Distributor",
    "Retailer",
    "Manufacturer",
]

LEAD_COLUMNS = [
    "Company",
    "Website",
    "Country",
    "Type",
    "Email",
    "Phone",
    "Relevance score",
    "Contacted",
    "Notes",
    "Source URL",
]

st.title("Saved Leads")
st.caption("Manage the companies you have saved")

st.info(
    "Lead storage is not connected yet. It will be added in Phase 6 "
    "(SQLite database). The controls below show how lead management "
    "will work.",
    icon=":material/info:",
)

# --- Filters ---
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
col1.text_input("Search saved leads", placeholder="Company name or website")
col2.selectbox("Country", ["All countries"])
col3.selectbox("Company type", COMPANY_TYPES)
col4.selectbox("Status", ["All", "Contacted", "Not contacted"])

st.divider()

# --- Leads table (empty until the database exists) ---
leads = pd.DataFrame(columns=LEAD_COLUMNS)
st.dataframe(leads, width="stretch", hide_index=True)
st.caption("No saved leads yet.")

# --- Actions preview (disabled) ---
st.subheader("Lead actions")
act1, act2, act3 = st.columns(3)
act1.button("Mark as contacted", disabled=True, width="stretch")
act2.button("Remove lead", disabled=True, width="stretch")
act3.button("Export saved leads", disabled=True, width="stretch")

st.text_area(
    "Notes",
    placeholder="Select a lead to add notes (available in Phase 6).",
    disabled=True,
)