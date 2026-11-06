import streamlit as st

from ui.styles import inject_css

st.set_page_config(
    page_title="TradeHunter AI",
    page_icon="🌍",
    layout="wide",
)

inject_css()

pages = [
    st.Page("views/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
    st.Page("views/find_companies.py", title="Find Companies", icon=":material/search:"),
    st.Page("views/website_analyzer.py", title="Website Analyzer", icon=":material/language:"),
    st.Page("views/import_export.py", title="Import/Export Research", icon=":material/local_shipping:"),
    st.Page("views/saved_leads.py", title="Saved Leads", icon=":material/bookmark:"),
    st.Page("views/search_history.py", title="Search History", icon=":material/history:"),
    st.Page("views/settings.py", title="Settings", icon=":material/settings:"),
]

navigation = st.navigation(pages)
navigation.run()