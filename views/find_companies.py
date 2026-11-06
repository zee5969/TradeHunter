import pandas as pd
import streamlit as st

from services.search_service import SearchError, search_companies

COMPANY_TYPES = [
    "All relevant companies",
    "Importer",
    "Exporter",
    "Wholesaler",
    "Distributor",
    "Retailer",
    "Manufacturer",
]

COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Germany", "France",
    "Italy", "Spain", "Netherlands", "Belgium", "Sweden", "Poland",
    "Turkey", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait",
    "Australia", "New Zealand", "Japan", "South Korea", "China",
    "India", "Bangladesh", "Brazil", "Mexico", "South Africa",
    "Nigeria", "Kenya", "Egypt", "Other (type in keywords)",
]

MAX_RESULTS = 20  # kept low for free API quotas

st.title("Find Companies")
st.caption("Discover potential buyers, importers, wholesalers and distributors")

with st.form("company_search_form"):
    product = st.text_input(
        "Product or industry *",
        placeholder="e.g. Sportswear, T-shirts, Football kits",
    )

    col1, col2 = st.columns(2)
    country = col1.selectbox("Target country *", COUNTRIES)
    company_type = col2.selectbox("Company type", COMPANY_TYPES)

    keywords = st.text_input(
        "Optional keywords",
        placeholder="e.g. private label, bulk orders, OEM",
    )

    num_results = st.slider(
        "Number of results",
        min_value=5,
        max_value=MAX_RESULTS,
        value=10,
        step=5,
        help="Each search uses 1 free search credit.",
    )

    submitted = st.form_submit_button("Search companies", type="primary")

if submitted:
    if not product.strip():
        st.error("Please enter a product or industry.")
    else:
        try:
            with st.spinner("Searching..."):
                st.session_state["search_output"] = search_companies(
                    product.strip(),
                    country,
                    company_type,
                    keywords.strip(),
                    num_results,
                )
        except SearchError as err:
            st.session_state.pop("search_output", None)
            st.error(str(err))

output = st.session_state.get("search_output")

if output:
    rows = output["rows"]
    st.divider()
    st.subheader("Search results")
    st.caption(f"Query sent to the search API: {output['query']}")

    if not rows:
        st.warning("No results were returned. Try different words.")
    else:
        st.info(
            "These are web search results, not verified importers. "
            "Directory and social pages are lead sources, not companies. "
            "Import/export activity is not confirmed for any result.",
            icon=":material/info:",
        )
        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Source URL": st.column_config.LinkColumn("Source URL"),
            },
        )
        st.caption(f"{len(rows)} unique results shown.")