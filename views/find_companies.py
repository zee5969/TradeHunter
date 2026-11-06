import pandas as pd
import streamlit as st

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
        help="Limited to protect free search-API quotas.",
    )

    submitted = st.form_submit_button("Search companies", type="primary")

if submitted:
    if not product.strip():
        st.error("Please enter a product or industry.")
    else:
        st.session_state["last_search"] = {
            "product": product.strip(),
            "country": country,
            "company_type": company_type,
            "keywords": keywords.strip(),
            "num_results": num_results,
        }

search = st.session_state.get("last_search")

if search:
    st.divider()
    st.subheader("Search summary")
    st.write(
        f"**Product:** {search['product']}  \n"
        f"**Country:** {search['country']}  \n"
        f"**Company type:** {search['company_type']}  \n"
        f"**Keywords:** {search['keywords'] or 'None'}  \n"
        f"**Results requested:** {search['num_results']}"
    )

    st.info(
        "Live company discovery is not connected yet. It will be added in "
        "Phase 3. The table below is a layout preview with placeholder rows.",
        icon=":material/info:",
    )

    preview = pd.DataFrame(
        {
            "Company": ["Placeholder company 1", "Placeholder company 2"],
            "Website": ["example.com", "example.com"],
            "Country": [search["country"], search["country"]],
            "Type": [search["company_type"], search["company_type"]],
            "Email": ["Not found", "Not found"],
            "Import/export evidence": ["Not verified", "Not verified"],
            "Source URL": ["Placeholder", "Placeholder"],
        }
    )
    st.dataframe(preview, width="stretch", hide_index=True)