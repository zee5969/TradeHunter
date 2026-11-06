import streamlit as st

st.title("Website Analyzer")
st.caption("Analyze a company website for publicly displayed business information")

with st.form("website_form"):
    url = st.text_input(
        "Company website URL *",
        placeholder="https://www.example.com",
    )
    product = st.text_input(
        "Product to match (optional)",
        placeholder="e.g. Sportswear",
        help="Used later to check whether the company is relevant to this product.",
    )
    submitted = st.form_submit_button("Analyze website", type="primary")

if submitted:
    if not url.strip():
        st.error("Please enter a website URL.")
    else:
        st.session_state["analyzer_input"] = {
            "url": url.strip(),
            "product": product.strip(),
        }

data = st.session_state.get("analyzer_input")

if data:
    st.divider()
    st.info(
        "Website fetching is not connected yet. It will be added in Phase 4. "
        "The fields below show what the analyzer will report.",
        icon=":material/info:",
    )

    st.subheader("Analysis result")
    st.write(f"**URL entered:** {data['url']}")
    st.write(f"**Product to match:** {data['product'] or 'None'}")

    NOT_ANALYZED = "Not analyzed yet"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Company")
        st.write(f"**Name:** {NOT_ANALYZED}")
        st.write(f"**Country / location:** {NOT_ANALYZED}")
        st.write(f"**Products and services:** {NOT_ANALYZED}")
        st.write(f"**Relevance to product:** {NOT_ANALYZED}")
    with col2:
        st.markdown("##### Public contact details")
        st.write(f"**Business emails:** {NOT_ANALYZED}")
        st.write(f"**Business phones:** {NOT_ANALYZED}")
        st.write(f"**Contact page:** {NOT_ANALYZED}")
        st.write(f"**About page:** {NOT_ANALYZED}")

    st.markdown("##### Business summary")
    st.write(NOT_ANALYZED)