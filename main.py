import streamlit as st

# Configure the app (Move this to the top)
st.set_page_config(
    page_title='Stress Level Detector',
    page_icon='heavy_exclamation_mark',
    layout='wide',
    initial_sidebar_state='auto'
)

# Import necessary functions and modules
from web_functions import load_data
from Tabs import home, data, predict, visualise

# Dictionary for pages
Tabs = {
    "Home": home,
    "Data Info": data,
    "Prediction": predict,
    "Visualisation": visualise
}

# Create a sidebar
st.sidebar.title("Navigation")

# Create radio option to select the page
page = st.sidebar.radio("Pages", list(Tabs.keys()))

# Loading the dataset.
df, X, y = load_data()

# Call the app function of the selected page
if page in ["Prediction", "Visualisation"]:
    Tabs[page].app(df, X, y)
elif page == "Data Info":
    Tabs[page].app(df)
else:
    Tabs[page].app()
