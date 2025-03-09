import streamlit as st

pg = st.navigation([
            st.Page("get_fcc_data.py", title="Download FCC Data", icon=":material/add_circle:"),
            #st.Page("page_2.py")
])
pg.run()
