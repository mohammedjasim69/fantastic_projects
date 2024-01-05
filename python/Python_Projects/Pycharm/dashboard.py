import pandas as pd
import streamlit as st
import os
import warnings
import plotly.express as px
from pygments.lexers import go

warnings.filterwarnings("ignore")

# Setting Page Layout
st.set_page_config(page_title="FoodMart!!!", page_icon=":chart_with_upwards_trend:", layout="wide")

# Setting Page Title with Icon from Streamlit
st.title(":chart_with_upwards_trend: Foodmart Data Analysis with Python Streamlit")

# Move up Title with CSS in top of page
st.markdown("<style>div.block-container{padding-top: 1rem;}</style>", unsafe_allow_html=True)

# Upload file for analysis
fl = st.file_uploader(" :file_folder: Upload your file for analysis", type=(["csv", "xlsx", "txt", "xlx"]))

# Condition for checking file.
if fl is not None:
    fileName = fl.name
    st.write(fileName)
    df = pd.read_csv(fileName, encoding="ISO-8859-1")
else:
    # Choose directory in file explorar
    os.chdir(r"C:\Users\Md.Jasim\OneDrive\Desktop\Projects\Python_Projects\Data_Set")
    df = pd.read_csv("Sample_Superstore.csv", encoding="ISO-8859-1")

# Declare two column for date picker and save value in data frame df
col1, col2 = st.columns((2))
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Getting Min and Max date from date picker
startDate = pd.to_datetime(df["Order_Date"]).min()
endDate = pd.to_datetime(df["Order_Date"]).max()

# Using Column for start date and end date
with col1:
    # date1 for start date in date picker
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    # date2 for end date in date picker
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filter data in data frame based on start date & end date and save on df1 from df
df1 = df[(df["Order_Date"] >= date1) & (df["Order_Date"] <= date2)].copy()

# Sidebar for filter different arguments
st.sidebar.header("Choose your filter: ")

# Create filter in sidebar for Region from Data Frame DataFrame_WithDateFilter with unique values
region = st.sidebar.multiselect("Choose your region", df1["Region"].unique())

# Condition if not select any region then store data in df2 copy from df1
if not region:
    df2 = df1.copy()
# Condition if select regions then store date in DataFrame_WithRegion from DataFrame_WithDateFilter with region
# filter data
else:
    df2 = df1[df1["Region"].isin(region)]

# Create filter in sidebar for State from DataFrame_WithDateFilter with unique values
state = st.sidebar.multiselect("Choose your state: ", df2["State"].unique())

# Condition if not select any region then copy date from DataFrame_WithRegion to DataFrame_WithState
if not state:
    df3 = df2.copy()
# Condition if select any region then copy date from DataFrame_WithRegion to DataFrame_WithState with selected state
else:
    df3 = df2[df2["State"].isin(state)]

# Create filter in sidebar for City from DataFrame_WithDateFilter with unique values
city = st.sidebar.multiselect("Choose your city: ", df3["City"].unique())

# Condition if not select any city then copy data from DataFrame_WithState to DataFrame_WithCity
# if not city:
#    df4 = df3.copy()
# Condition if select any city then copy data from DataFrame_WithState to DataFrame_WithCity with selected state
# else:
#    df4 = df3[df3["City"].isin(city)]


# Filter data based on region, state, city and save it to different dataframe for analysis


if not region and not state and not city:
    filtered_df = df1
elif not state and not city:
    filtered_df = df1[df1["Region"].isin(region)]
elif not city and not region:
    filtered_df = df1[df["State"].isin(state)]
elif not region and not state:
    filtered_df = df1[df1["City"].isin(city)]
elif state and city:
    filtered_df = df3[df3["State"].isin(state) & (df3["City"].isin(city))]
elif region and city:
    filtered_df = df3[df3["Region"].isin(region) & (df3["City"].isin(city))]
elif region and state:
    filtered_df = df3[df3["Region"].isin(region) & (df3["State"].isin(state))]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city) & df3["Region"].isin(region)]


category_df = filtered_df.groupby(by = ["Category"], as_index = False )["Sales"].sum()

#category_df.reset_index(inplace = True)

with col1:
    st.subheader("Region wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)





