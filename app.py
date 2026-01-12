import streamlit as st

st.set_page_config(
    page_title="Country Data Dashboard",
    layout="wide"
    )

# Sidebar Navigation Pane
st.sidebar.markdown("## 📋 Navigation page :")
page = st.sidebar.radio(
    "Choose a page :",
    options=["About Dataset", "Dashboards", "Machine Learning", "Prediction App", "Contact Me"],
    index=0
)

# Route to selected page
if page == "About Dataset":
    import about
    about.about_dataset()
elif page == "Dashboards":
    import visualisasi
    visualisasi.chart()
elif page == "Machine Learning":
    import machine_learning
    machine_learning.ml_model()
elif page == "Prediction App":
    import prediction
    prediction.prediction_app()
elif page == "Contact Me":
    import kontak
    kontak.contact_me()

#a. background color dashboard
st.markdown(
        """
        <style>
        .stApp {
            background-color: #181818;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
#b. background color sidebar + style navigation radio buttons
st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #282828 !important;
        }
        /* Sidebar text color */
        [data-testid="stSidebar"] {
            color: #FFFFFF !important;
        }
        /* Style radio button container */
        [data-testid="stSidebar"] .stRadio {
            background-color: transparent;
        }
        /* Style radio buttons with button-like appearance */
        [data-testid="stSidebar"] .stRadio > label {
            color: #FFFFFF !important;
            display: inline-block;
            padding: 10px 16px;
            margin: 4px 0;
            background-color: #1e1e1e;
            border: 2px solid #75b9bf;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            font-weight: 500;
        }
        /* Hover effect for radio buttons */
        [data-testid="stSidebar"] .stRadio > label:hover {
            background-color: #75b9bf;
            color: #213448 !important;
        }
        /* Style radio button container and text */
        [data-testid="stSidebar"] [role="radiogroup"] {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] [role="radio"] {
            accent-color: #75b9bf !important;
        }
        /* Selected radio button styling */
        [data-testid="stSidebar"] input[type="radio"]:checked + label {
            background-color: #75b9bf !important;
            color: #213448 !important;
        }
        /* Radio label text styling */
        [data-testid="stSidebar"] .stRadio > label > div {
            color: inherit !important;
        }
        </style>
        """,
        unsafe_allow_html=True
        )