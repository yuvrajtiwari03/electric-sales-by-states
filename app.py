import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="EV Sales Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Header style */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #0D47A1;
        text-align: center;
        padding: 10px;
    }
    /* KPI Card Styling */
    [data-testid="stMetric"] {
        background-color:#FF9800;;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    [data-testid="stMetric"]:hover {
        background-color: #E6E6FA ;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-title">⚡ Electric Vehicle Sales Dashboard</div>', unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("electric_sales.csv")  # make sure your csv file name same as it in github file folder 
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2d/Electric_car_icon.png", width=100)
st.sidebar.header("🔍 Filters")

year_filter = st.sidebar.multiselect("Select Year", sorted(df["Year"].unique()))
state_filter = st.sidebar.multiselect("Select State", sorted(df["State"].unique()))

df_filtered = df.copy()
if year_filter:
    df_filtered = df_filtered[df_filtered["Year"].isin(year_filter)]
if state_filter:
    df_filtered = df_filtered[df_filtered["State"].isin(state_filter)]

# --- KPI CALCULATIONS ---
total_sales = df_filtered["EV_Sales"].sum()
top_state = df_filtered.groupby("State")["EV_Sales"].sum().idxmax()
#growth = ((total_sales - df["EV_Sales"].sum()) / df["EV_Sales"].sum()) * 100

# --- Growth Calculation (Year-on-Year) ---
sales_by_year = df_filtered.groupby("Year")["EV_Sales"].sum().reset_index()
if len(sales_by_year) > 1:
    growth = ((sales_by_year.iloc[-1]["EV_Sales"] - sales_by_year.iloc[-2]["EV_Sales"]) / 
               sales_by_year.iloc[-2]["EV_Sales"]) * 100
else:
    growth = 0

# --- KPI CARDS ---

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total EV Sales", value=f"{total_sales:,.0f}")
with col2:
    st.metric(label="Top State", value=top_state)
with col3:
    st.metric(label="Growth %", value=f"{growth:.2f}%", delta=f"{growth:.2f}%")


# --- CHARTS ---
col4, col5 = st.columns(2)

with col4:
    sales_trend = df_filtered.groupby("Year")["EV_Sales"].sum().reset_index()
    fig_trend = px.line(sales_trend, x="Year", y="EV_Sales", 
                        title="📈 Sales Trend Over Years", markers=True, 
                        template="plotly_dark", color_discrete_sequence=["#FFA726"])
    st.plotly_chart(fig_trend, use_container_width=True)

with col5:
    category_data = df_filtered.groupby("Vehicle_Category")["EV_Sales"].sum().reset_index()
    fig_pie = px.pie(category_data, names="Vehicle_Category", values="EV_Sales", 
                     title="🚗 Sales by Vehicle Category", hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("📊 Electric Vehicle Sales Dashboard | Created by [YUVRAJ TIWARI] | Powered by Streamlit")




















