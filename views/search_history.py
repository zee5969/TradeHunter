import pandas as pd
import streamlit as st

HISTORY_COLUMNS = [
    "Date",
    "Product",
    "Country",
    "Company type",
    "Keywords",
    "Results",
]

st.title("Search History")
st.caption("Review your previous company searches")

st.info(
    "Search history is not connected yet. It will be saved to the database "
    "in Phase 6.",
    icon=":material/info:",
)

history = pd.DataFrame(columns=HISTORY_COLUMNS)
st.dataframe(history, width="stretch", hide_index=True)
st.caption("No searches recorded yet.")

st.button("Clear history", disabled=True)
