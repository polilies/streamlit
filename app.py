import io
import pandas as pd #pip instal pandas openpyxl
import plotly.express as px #pip install plotly-express
import streamlit as st      #pip install streamlit

#https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", 
                   page_icon=":chart_with_upwards_trend:",
                   layout= "wide"
)

@st.cache
def get_data_from_excel():
    
    df = pd.read_excel(io='supermarkt_sales.xlsx',engine='openpyxl', sheet_name='Sales', 
                        skiprows= 3, usecols='B:R', nrows= 1000
                        )
    # Adding HOUR column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour    
    return df
    
df = get_data_from_excel()


#----SIDEBAR------
st.sidebar.header("Burada Filitreleyin")
city = st.sidebar.multiselect("Sehri Secin", 
                              options = df["City"].unique(),
                              default= df["City"].unique()
)

customer = st.sidebar.multiselect("Musteri Tipi", 
                              options = df["Customer_type"].unique(),
                              default= df["Customer_type"].unique()
)

gender = st.sidebar.multiselect("Cinsiyet", 
                              options = df["Gender"].unique(),
                              default= df["Gender"].unique()
)

selection = df.query("City == @city and Customer_type == @customer and Gender == @gender")


st.dataframe(selection)

#--MAIN_PAGE----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


#--Top KPI--

total_sales = round(selection["Total"].sum(), 2)
average_rating = round(selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 2)) #6,9 shows us 7 stars
average_sales_by_transection = round(selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader(f"Total Sales: US $ {total_sales: ,}")
    
with middle_column:
    st.subheader(f"Average Rating: {average_rating}  {star_rating}")
    
with right_column:
    st.subheader(f"Average Sales By Transaction: US $ {average_sales_by_transection}")
    
st.markdown("----")

#Sales By prodcut Line (Bar CHART)

sales_by_product_line = (selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total"))

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y = sales_by_product_line.index,
    orientation= "h",
    title= "<b> Slaes Produst Line </b>",
    color_discrete_sequence=["#008388"] * len(sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)

#Sales By HOUR [BAR CHART]

sales_by_hour = selection.groupby(by=["hour"]).sum()[["Total"]]