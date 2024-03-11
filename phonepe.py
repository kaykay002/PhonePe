import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
#--------------------------------------------------------------------------------------------------
#------------------------DATA FRAMES--------------------------------------------------------------

#DataFrame Creation

#SQL connection:

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      password=12345,
                      database="Phonepe_database",
                      port=5432)

cursor=mydb.cursor()


#1.Aggregate Insurance df-------------------------------------->>>>>>

cursor.execute("Select * from aggregate_insurance")
mydb.commit()
T1= cursor.fetchall()
Aggregated_Insurance=pd.DataFrame(T1,columns=("State", "Year","Quarter","Transaction_Type", "Transaction_Count","Transaction_Amount"))

#2.Aggregate Transaction df----------------------------------->>>>>>>>

cursor.execute("Select * from aggregate_transaction")
mydb.commit()
T2= cursor.fetchall()
Aggregated_Transaction=pd.DataFrame(T2,columns=("State", "Year","Quarter","Transaction_Type", "Transaction_Count","Transaction_Amount"))

#3.Aggregate User df-------------------------------------------->>>>>>>>>

cursor.execute("Select * from aggregate_user")
mydb.commit()
T3= cursor.fetchall()
Aggregated_User=pd.DataFrame(T3,columns=("State", "Year","Quarter","Brand", "Transaction_Count","Percentage"))


#4.Map Insurance df-------------------------------------------------->>>>

cursor.execute("Select * from map_transaction")
mydb.commit()
T4= cursor.fetchall()
Map_Insurance=pd.DataFrame(T4,columns=("State", "Year","Quarter","District", "Transaction_Count","Transaction_Amount"))


#5.Map Transaction df-------------------------------------------------->>>>

cursor.execute("Select * from map_transaction")
mydb.commit()
T5= cursor.fetchall()
Map_Transaction=pd.DataFrame(T5,columns=("State", "Year","Quarter","District", "Transaction_Count","Transaction_Amount"))

#6.Map User df-------------------------------------------------->>>>

cursor.execute("Select * from map_user")
mydb.commit()
T6= cursor.fetchall()
Map_User=pd.DataFrame(T6,columns=("State", "Year","Quarter","District", "Registered_Users","App_Opens"))

#7.Top Insurance df-------------------------------------------------->>>>

cursor.execute("Select * from top_insurance")
mydb.commit()
T7= cursor.fetchall()
Top_Insurance=pd.DataFrame(T7,columns=("State", "Year","Quarter","Pincode", "Transaction_Count","Transaction_Amount"))

#8.Top Transaction df-------------------------------------------------->>>>

cursor.execute("Select * from top_transaction")
mydb.commit()
T8= cursor.fetchall()
Top_Transaction=pd.DataFrame(T8,columns=("State", "Year","Quarter","Pincode", "Transaction_Count","Transaction_Amount"))

#9.Top Users df-------------------------------------------------->>>>

cursor.execute("Select * from top_user")
mydb.commit()
T9= cursor.fetchall()
Top_User=pd.DataFrame(T9,columns=("State", "Year","Quarter","Pincode", "Registered_Users"))
#-------------------------------------------------------------------------------------------------

def transactions_yearwise(df,year):
    transy=df[df["Year"]==year]
    transy.reset_index(drop=True, inplace=True)

    transyg=transy.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum()
    transyg.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_map=json.loads(response.content)
    state_name=[]
    for feature in data_map["features"]:
        state_name.append(feature["properties"]["ST_NM"])
    state_name.sort()

#Transaction_amount
    amount_fig=px.bar(transyg, x="State", y="Transaction_Amount",title=f"Transaction Amount of {year}", color_discrete_sequence=px.colors.diverging.Spectral,height=570, width=650)
    
       
    india_map1=px.choropleth(transyg, geojson=data_map, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_Amount", color_continuous_scale="thermal",
                            range_color=(transyg["Transaction_Amount"].min(),transyg["Transaction_Amount"].max()),
                            hover_name="State", fitbounds="locations",
                            height=600, width=600 )
    india_map1.update_geos(visible=False)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(amount_fig)     
    with col2:
        st.plotly_chart(india_map1)

#Transaction_count
    count_fig=px.bar(transyg, x="State", y="Transaction_Count",title=f"Transaction Count of {year}",color_discrete_sequence=px.colors.qualitative.Prism, height=570, width=650)
    
    india_map2=px.choropleth(transyg, geojson=data_map, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_Count", color_continuous_scale="thermal",
                            range_color=(transyg["Transaction_Count"].min(),transyg["Transaction_Count"].max()),
                            hover_name="State", fitbounds="locations",
                            height=600, width=600 )
    india_map2.update_geos(visible=False)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(count_fig)
    with col2:
        st.plotly_chart(india_map2)

    return transy
#------------------------------------------------------------------------------------------------
def transactions_yearwise_quarter(df,quarter):
    transy=df[df["Quarter"]==quarter]
    transy.reset_index(drop=True, inplace=True)

    transyg=transy.groupby("State")[["Transaction_Count", "Transaction_Amount"]].sum()
    transyg.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data_map=json.loads(response.content)
    state_name=[]
    for feature in data_map["features"]:
        state_name.append(feature["properties"]["ST_NM"])
    state_name.sort()

#Transaction_amount
    amount_fig=px.bar(transyg, x="State", y="Transaction_Amount",title=f"Transaction Amount of Year {transy['Year'].min()} : Quarter {quarter}", color_discrete_sequence=px.colors.diverging.Spectral,height=400, width=550)
    
       
    india_map1=px.choropleth(transyg, geojson=data_map, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_Amount", color_continuous_scale="thermal",
                            range_color=(transyg["Transaction_Amount"].min(),transyg["Transaction_Amount"].max()),
                            hover_name="State", title=f"Transaction Amount of Year {transy['Year'].min()} : Quarter {quarter}", fitbounds="locations",
                            height=600, width=650 )
    india_map1.update_geos(visible=False)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(amount_fig)
    with col2:
        st.plotly_chart(india_map1)

#Transaction_count
    count_fig=px.bar(transyg, x="State", y="Transaction_Count",title=f"Transaction Count of Year {transy['Year'].min()} : Quarter {quarter}",color_discrete_sequence=px.colors.qualitative.Prism, height=400, width=650)
    
    india_map2=px.choropleth(transyg, geojson=data_map, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_Count", color_continuous_scale="thermal",
                            range_color=(transyg["Transaction_Count"].min(),transyg["Transaction_Count"].max()),
                            hover_name="State", title=f"Transaction Count of Year {transy['Year'].min()} : Quarter {quarter}", fitbounds="locations",
                            height=600, width=600 )
    india_map2.update_geos(visible=False)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(count_fig)
    with col2:
        st.plotly_chart(india_map2)
#-----------------------------------------------------------------------------------------------
def Agg_Analysis_Transaction(df, state):

    transy=df[df["State"]==state]
    transy.reset_index(drop=True, inplace=True)

    transyg=transy.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    transyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    
    fig_pie1=px.pie(data_frame=transyg, names="Transaction_Type", values="Transaction_Amount",
                    width=500, title=f"{state}'s {year} Transaction Amount", hole=0.4, color_discrete_sequence=px.colors.qualitative.Prism)
    with col1:
        st.plotly_chart(fig_pie1)

    fig_pie2=px.pie(data_frame=transyg, names="Transaction_Type", values="Transaction_Count",
                    width=500, title=f"{state}'s {year} Transaction Count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Prism)

    
    with col2:
        st.plotly_chart(fig_pie2) 
#--------------------------------------------------------------------------------------------------
#aggregated user analysis 1
def Agg_user_brand_plot(df, year):
    agguser=df[df["Year"]==year]
    agguser.reset_index(drop=True, inplace=True)

    agguserg=pd.DataFrame(agguser.groupby("Brand")["Transaction_Count"].sum())
    agguserg.reset_index(inplace=True)


    fig_bar_brand=px.bar(agguserg, x="Brand", y="Transaction_Count",title=f"Brand's {year} Transaction Graph for {year}",
                            width=800, height=400,color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_bar_brand)

    return agguser

#-----------------------------------------------------------------------------------------------------
#aggregated user analysis 2
def Agg_user_brand_plot2(df, quarter):
    agguserq=df[df["Quarter"]==quarter]
    agguserq.reset_index(drop=True, inplace=True)

    agguserqg=pd.DataFrame(agguserq.groupby("Brand")["Transaction_Count"].sum())
    agguserqg.reset_index(inplace=True)

    fig_bar_brand2=px.bar(agguserqg, x="Brand", y="Transaction_Count",title=f"Brand's quarter:{quarter} Transaction Graph",
                                width=800, height=400,color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_bar_brand2)

    return agguserq
#-----------------------------------------------------------------------------------------------------
def Agg_user_brand_plot3(df, state):
    aggus=df[df["State"]==state]
    aggus.reset_index(drop=True, inplace=True)


    fig_line1=px.line(aggus, x="Brand", y="Transaction_Count", hover_data="Percentage", title=f"{state}'s Brands's Transaction Count & Percentage", width=1000,color_discrete_sequence=px.colors.qualitative.Prism, markers=True)
    st.plotly_chart(fig_line1)

    return aggus
#-----------------------------------------------------------------------------------------------------
def Map_insurance_district(df, state):

    mapi=df[df["State"]==state]
    mapi.reset_index(drop=True, inplace=True)

    mapig=mapi.groupby("District")[["Transaction_Count", "Transaction_Amount"]].sum()
    mapig.reset_index(inplace=True)
    
    fig_bar_map=px.bar(mapig, y="District", x="Transaction_Amount",orientation='h' , height=750,
                     title=f"{state}'s Districtwise  Transaction Amount", color_discrete_sequence=px.colors.diverging.Spectral)
    
    st.plotly_chart(fig_bar_map)

    fig_bar_map2=px.bar(mapig, y="District", x="Transaction_Count",orientation='h', height=750,
                    title=f"{state}'s Districtwise Transaction Count",color_discrete_sequence=px.colors.qualitative.Prism)
    
    st.plotly_chart(fig_bar_map2) 
    
    return mapi
#---------------------------------------------------------------------------------------------------
#Map_user_plot1
def map_user_line_graph(df,year):
    mapuser=df[df["Year"]==year]
    mapuser.reset_index(drop=True, inplace=True)

    mapuserg=pd.DataFrame(mapuser.groupby("State")[["Registered_Users", "App_Opens"]].sum())
    mapuserg.reset_index(inplace=True)
    fig_line2=px.line(mapuserg, x="State", y=["Registered_Users", "App_Opens"], 
                    title=f"Registered_Users & App_Opens for {year}", 
                    width=1100,height=700,color_discrete_sequence=px.colors.qualitative.Prism, markers=True)
    st.plotly_chart(fig_line2)   

    return mapuser
#------------------------------------------------------------------------------------------------
#Map_user_plot2
def Map_user_quarter_plot(df, quarter):
    mapuserq=df[df["Quarter"]==quarter]
    mapuserq.reset_index(drop=True, inplace=True)

    mapuserqg=pd.DataFrame(mapuserq.groupby("State")[["Registered_Users", "App_Opens"]].sum())
    mapuserqg.reset_index(inplace=True)
    fig_line3=px.line(mapuserqg, x="State", y=["Registered_Users", "App_Opens"], 
                    title=f"Registered_Users & App_Opens for {year} : Quarter {quarter}", 
                    width=1100,height=700,color_discrete_sequence=px.colors.diverging.Spectral_r, markers=True)
    st.plotly_chart(fig_line3)   

    return mapuserq
#--------------------------------------------------------------------------------------------------
def map_user_quarter(df, state):
    mapuq = df[df["State"] == state]
    mapuqg = mapuq.groupby("State")[["Registered_Users", "App_Opens"]].sum()
    mapuqg.reset_index(inplace=True)

    mapuqgd = mapuq.groupby("District")[["Registered_Users", "App_Opens"]].sum()
    mapuqgd.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data_map = json.loads(response.content)

    amount_fig = px.bar(mapuqgd, y="District", x="Registered_Users",
                        title=f"Registered_Users in {state} for {year}",
                        color_discrete_sequence=px.colors.diverging.Spectral, height=400, width=550)

    india_map1 = px.choropleth(mapuqg, geojson=data_map, locations="State", featureidkey="properties.ST_NM",
                               hover_data={"App_Opens": True, "Registered_Users": True},hover_name="State",
                               title=f"Registered Users in {state} - Year: Quarter", fitbounds="locations",
                               height=600, width=650)
    india_map1.update_geos(visible=False)

    count_fig = px.bar(mapuqgd, y="District", x="App_Opens",
                       title=f"App_Opens in {state} for {year}",
                       color_discrete_sequence=px.colors.qualitative.Prism, height=400, width=650)

    col1, col2=st.columns(2)
    with col1:
        st.plotly_chart(amount_fig)
    with col2:
        st.plotly_chart(count_fig)
    st.plotly_chart(india_map1)
#---------------------------------------------------------------------------------------------------
def Top_insurance_district(df, state):

    Tmapi=df[df["State"]==state]
    Tmapi.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    
    fig_bar_map=px.bar(Tmapi, y="Quarter", x="Transaction_Amount",orientation='h' , hover_data='Pincode',
                     title=f"{state}'s Quarter-Pincode wise Transaction Amount", color_discrete_sequence=px.colors.diverging.Spectral)
    with col1:
        st.plotly_chart(fig_bar_map)

    fig_bar_map2=px.bar(Tmapi, y="Quarter", x="Transaction_Count",orientation='h',hover_data='Pincode',
                    title=f"{state}'s Quarter-Pincode wise Transaction Count",color_discrete_sequence=px.colors.diverging.Spectral_r)

    
    with col2:
        st.plotly_chart(fig_bar_map2)
#----------------------------------------------------------------------------------------------------
def Top_user_plot(df,year):
    topuser=df[df["Year"]==year]
    topuser.reset_index(drop=True, inplace=True)

    topuserg=pd.DataFrame(topuser.groupby(["State","Quarter"])["Registered_Users"].sum())
    topuserg.reset_index(inplace=True)

    plot=px.bar(topuserg, x="State", y="Registered_Users",color= "Quarter",height=800, width=800,
                title=f"Statewise Registered Users as per quarter in year {year}",
                color_continuous_scale="Purpor"
                )

    st.plotly_chart(plot)
    return topuser
#--------------------------------------------------------------------------------------------------
#Top user 2
def Top_user_plot2(df,state):
    topusers=df[df["State"]==state]
    topusers.reset_index(drop=True, inplace=True)

    topusersg=pd.DataFrame(topusers.groupby(["State","Quarter"])["Registered_Users"].sum())
    topusersg.reset_index(inplace=True)

    plot2=px.pie(data_frame=topusersg, names="Quarter", values="Registered_Users",color= "Quarter",height=500, width=600,
                title=f"Registered Users in {state} in year {year}",
                hole=0.4, color_discrete_sequence=px.colors.qualitative.Prism
                
                )

    st.plotly_chart(plot2)
    

        

#----------------Streamlit User Interface-----------------#

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.image("1.png", width=100)

with col2:
    st.title("PhonePe Pulse Dashboard")
    


#----------------------------------------MAIN MENU------------------------------------------------------
SELECT = option_menu(
    menu_title = None,
    options = ["About","Maps & Charts","FAQs"],
    icons =["phone","bar-chart","book"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"medium", "width": "100%"},
        "icon": {"color": "white", "font-size": "15px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "none"},
        "nav-link-selected": {"background-color": "#4E049C"}})
#----------------------------------------------ABOUT-------------------------------------------------------
if SELECT == "About":
    col1, col2 = st.columns(2)

    with col1:
        st.image("2.jpg", width=500)
    with col2:    
        st.markdown('<div style="text-align: justify;">The Phonepe Pulse Dashboard is a dynamic visualization platform meticulously crafted to delve into the extensive data reservoir of the Phonepe Pulse Github repository. Boasting seamless data extraction, processing, and visualization capabilities, this dashboard offers an immersive experience, unveiling insights and trends through interactive geo-visualizations. With a user-friendly interface enriched by dropdown options, users can effortlessly tailor their analysis to extract meaningful insights. Powered by continuous updates and efficient MySQL database integration, the dashboard ensures users are equipped with the latest information for informed decision-making. Experience the fusion of innovation and usability, driving data-driven excellence with the Phonepe Pulse Dashboard.</div>', unsafe_allow_html=True)
                
    st.markdown('<div style="text-align: justify;">PhonePe is a digital payment platform and financial technology company based in India. It allows users to make digital transactions, including payments, mobile recharge, bill payments, and more using their smartphones. PhonePe was founded in 2015 and has since grown to become one of the leading digital payment platforms in India. The platform offers various payment services such as Unified Payments Interface (UPI), which enables users to transfer funds directly between bank accounts using their mobile phones. Additionally, PhonePe allows users to link their bank accounts, debit cards, and credit cards to facilitate seamless transactions. PhonePe has also expanded its services to include features such as bill splitting, online shopping,insurance services, and investment options. It has gained popularity due to its user-friendly interface, secure transactions, and wide acceptance across merchants in India.</div>', unsafe_allow_html=True)


#----------------------------------------------ANALYSIS---------------------------------------------------------
if SELECT == "Maps & Charts":
    with st.sidebar:
        SELECT = st.selectbox("Select Analysis of", ["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    if SELECT == "Aggregated Analysis":
        with st.sidebar:
            method = st.radio("Select the Aggregated Analysis category, By:-", ["Insurance", "Transaction", "User"])

        if method == "Insurance":
            year = st.slider("Select the year", Aggregated_Insurance["Year"].min(), Aggregated_Insurance["Year"].max(), Aggregated_Insurance["Year"].min())
            transyear = transactions_yearwise(Aggregated_Insurance, year)

            with st.sidebar:
                quarter = st.slider("Select the quarter", transyear["Quarter"].min(), transyear["Quarter"].max(), transyear["Quarter"].min())
            transactions_yearwise_quarter(transyear, quarter)

        elif method == "Transaction":
            year = st.slider("Select the year", Aggregated_Transaction["Year"].min(), Aggregated_Transaction["Year"].max(), Aggregated_Transaction["Year"].min())
            Agg_trans_yearly = transactions_yearwise(Aggregated_Transaction, year)

            quarter = st.slider("Select the quarter", Agg_trans_yearly["Quarter"].min(), Agg_trans_yearly["Quarter"].max(), Agg_trans_yearly["Quarter"].min())
            transactions_yearwise_quarter(Agg_trans_yearly, quarter)

            states = st.selectbox("Select State", Agg_trans_yearly["State"].unique())
            Agg_Analysis_Transaction(Agg_trans_yearly, states)

        elif method == "User":
            year = st.slider("Select the year", Aggregated_User["Year"].min(), Aggregated_User["Year"].max(), Aggregated_User["Year"].min())
            Agg_user_year = Agg_user_brand_plot(Aggregated_User, year)

            quarter = st.slider("Select the quarter", Agg_user_year["Quarter"].min(), Agg_user_year["Quarter"].max(), Agg_user_year["Quarter"].min())
            Agg_user_year_quarter = Agg_user_brand_plot2(Agg_user_year, quarter)

            states = st.selectbox("Select State", Agg_user_year_quarter["State"].unique())
            Agg_user_brand_plot3(Agg_user_year_quarter, states)

    elif SELECT == "Map Analysis":
        with st.sidebar:
            method2 = st.radio("Select the Map Analysis category, By:-", ["Insurance", "Transaction", "User"])

        if method2 == "Insurance":
            year = st.slider("Select the year", Map_Insurance["Year"].min(), Map_Insurance["Year"].max(), Map_Insurance["Year"].min())
            Map_insurance_yearly = transactions_yearwise(Map_Insurance, year)

            states = st.selectbox("Select State", Map_insurance_yearly["State"].unique())
            Map_insurance_district(Map_insurance_yearly, states)

            quarter = st.slider("Select the quarter", Map_insurance_yearly["Quarter"].min(), Map_insurance_yearly["Quarter"].max(), Map_insurance_yearly["Quarter"].min())
            Map_insurance_quarter=transactions_yearwise_quarter(Map_insurance_yearly,quarter)



        elif method2 == "Transaction":
            year = st.slider("Select the year", Map_Transaction["Year"].min(), Map_Transaction["Year"].max(), Map_Transaction["Year"].min())
            Map_transaction_yearly=transactions_yearwise(Map_Transaction, year)

            states = st.selectbox("Select State", Map_Transaction["State"].unique())
            Map_insurance_district(Map_Transaction, states)

            quarter = st.slider("Select the quarter", Map_Transaction["Quarter"].min(), Map_Transaction["Quarter"].max(), Map_Transaction["Quarter"].min())
            Map_transaction_quarter=transactions_yearwise_quarter(Map_transaction_yearly,quarter)


        elif method2 == "User":
            year = st.slider("Select the year", Map_User["Year"].min(), Map_User["Year"].max(), Map_User["Year"].min())
            Map_user_yearly=map_user_line_graph(Map_User,year)

            quarter = st.slider("Select the quarter", Map_User["Quarter"].min(), Map_User["Quarter"].max(), Map_User["Quarter"].min())
            Map_user_quarterly=Map_user_quarter_plot(Map_user_yearly, quarter)

            states = st.selectbox("Select State", Map_User["State"].unique())
            map_user_quarter(Map_User, states)


    elif SELECT == "Top Analysis":
        with st.sidebar:
            method3=st.radio("Select the Top Analysis category, By:-",["Insurance","Transaction","User"])

        if method3=="Insurance":
            year = st.slider("Select the year", Top_Insurance["Year"].min(), Top_Insurance["Year"].max(), Top_Insurance["Year"].min())
            Top_insurance_yearly=transactions_yearwise(Top_Insurance, year)  

            states = st.selectbox("Select State", Top_Insurance["State"].unique())
            Top_insurance_district(Top_insurance_yearly, states)
            
        elif method3=="Transaction":
            year = st.slider("Select the year", Top_Transaction["Year"].min(), Top_Transaction["Year"].max(), Top_Transaction["Year"].min())
            Top_transaction_yearly=transactions_yearwise(Top_Transaction, year)

            states = st.selectbox("Select State", Top_Transaction["State"].unique())
            Top_insurance_district(Top_transaction_yearly, states)

        elif method3=="User":
            year = st.slider("Select the year", Top_User["Year"].min(), Top_User["Year"].max(), Top_User["Year"].min())
            Top_user_yearly=Top_user_plot(Top_User,year)

            states = st.selectbox("Select State", Top_User["State"].unique())
            Top_user_plot2(Top_user_yearly, states)


#---------------------------------------------FAQS----------------------------------------------------------
if SELECT == "FAQs":
    options = ["SELECT",
               "1. Top 10 states based on highest transaction amount",
               "2. List 10 states based on most no. of transaction",
               "3. Top 5 Transaction Type based on Transaction Amount",
               "4. Top 10 States and District based on Registered-users ",
               "5. Top 10 Districts based on Count of transaction",
               "6. List 10 Districts based on lowest amount of transaction",
               "7. List 10 Districts based on lowest Transaction Count",
               "8. Top 10 States and District based on App Opens",
               "9. Top 10 Brands in India with highest registered users",
               "10. Top 10 States in India with highest insurance users",
               "11. Top 5 Brands in Rajasthan with highest registered users",
               "12. Top 5 Districts of Rajasthan with highest transaction amount",
               "13. Top 5 Rajasthan Districts with Insurance users"
               ]

    #1
               
    select = st.selectbox("Select the option",options)
    if select=="1. Top 10 states based on highest transaction amount":
        cursor.execute('''SELECT DISTINCT State, Year, 
                       SUM(Transaction_Amount) AS Transaction_Amount FROM 
                       top_transaction GROUP BY State, Year ORDER BY 
                       Transaction_Amount DESC LIMIT 10''')
        
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Year', 'Transaction_Amount'])
        
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 10 states with highest transaction amount")
            st.bar_chart(data=df,x="Transaction_Amount",y="States",color='#46039C')
            
            #2

    elif select=="2. List 10 states based on most no. of transaction":
        cursor.execute('''SELECT DISTINCT State, SUM(Transaction_Count) as Total FROM 
                       top_transaction GROUP BY State ORDER BY Total DESC LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Total_Transaction'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("States with most no. of transactions")
            st.bar_chart(data=df,x="Total_Transaction",y="State",color='#46039C')
            
            #3
            
    elif select == "3. Top 5 Transaction Type based on Transaction Amount":
        cursor.execute('''SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Amount 
                       FROM aggregate_transaction GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("Top 5 Transaction Type based on Transaction Amount")
            st.scatter_chart(data=df, y="Transaction_Type", x="Transaction_Amount",color='#46039C')

            #4
            
    elif select=="4. Top 10 States and District based on Registered-users ":
        cursor.execute('''SELECT DISTINCT State, District, SUM(Registered_Users) AS Users 
                       FROM map_user GROUP BY State, District ORDER BY Users DESC LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Registered_Users'])
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 10 States and District based on Registered-users")
            st.bar_chart(data=df,y="State",x="Registered_Users",color='#46039C')
            
            #5
            
    elif select=="5. Top 10 Districts based on Count of transaction":
        cursor.execute('''SELECT DISTINCT State,District,SUM(Transaction_Count) AS Counts 
                       FROM map_transaction GROUP BY State,District ORDER BY Counts DESC LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("Top 10 Districts based on Count of transaction")
            st.bar_chart(data=df,y="State",x="Transaction_Count",color='#46039C')
            
            #6
            
    elif select=="6. List 10 Districts based on lowest amount of transaction":
        cursor.execute('''SELECT DISTINCT State,District,Year,SUM(Transaction_Amount) 
                       AS Amount FROM map_transaction GROUP BY State, District, Year ORDER BY 
                       Amount asc LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Year','Transaction_Amount'])
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("10 Districts with least amount of transaction")
            st.bar_chart(data=df,y="State",x="Transaction_Amount",color='#46039C')
            
            #7
            
    elif select=="7. List 10 Districts based on lowest Transaction Count":
        cursor.execute('''SELECT DISTINCT State, District, SUM(Transaction_Count) AS 
                       Counts FROM map_transaction GROUP BY State,District ORDER BY Counts ASC LIMIT 10''');
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("Districts and states with lowest number of Transactions")
            st.bar_chart(data=df,y="State",x="Transaction_Count",color='#46039C')
            
     #8
             
    elif select=="8. Top 10 States and District based on App Opens":
        cursor.execute('''SELECT DISTINCT State,District, SUM(App_Opens) AS Users 
                       FROM map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10''');
        df = pd.DataFrame(cursor.fetchall(),columns = ['State','District','App_Opens'])
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 10 States and District based on App_Opens")
            st.bar_chart(data=df,y="State",x="App_Opens",color='#46039C')


    #9
    
    elif select=="9. Top 10 Brands in India with highest registered users":
        cursor.execute('''SELECT Brand, sum(transaction_count) AS Total_Users
                  FROM aggregate_user  GROUP BY Brand
                  ORDER BY Total_Users DESC LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users'])
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 10 Brands in India")
            st.bar_chart(data=df, x='Total_Users', y='Brand',color='#46039C')
    
    #10
    
    elif select=="10. Top 10 States in India with highest insurance users":
        cursor.execute('''SELECT state, sum(transaction_count) AS Total_Insurance
                  FROM aggregate_insurance  GROUP BY State
                  ORDER BY Total_Insurance DESC LIMIT 10''')
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("Top 10 State in India")
            st.bar_chart(data=df, x='Total_Insurance', y='State',color='#46039C')


    #11
    
    elif select=="11. Top 5 Brands in Rajasthan with highest registered users":
        cursor.execute('''SELECT Brand, sum(transaction_count) AS Total_Users
                  FROM aggregate_user WHERE State = 'Rajasthan' GROUP BY Brand
                  ORDER BY Total_Users DESC LIMIT 5''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users'])
        col1,col2 = st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 5 Brands in Rajasthan")
            st.bar_chart(data=df, x='Total_Users', y='Brand',color='#46039C')
    
           

    #12
    
    elif select=="12. Top 5 Districts of Rajasthan with highest transaction amount":
        cursor.execute('''SELECT District, SUM(Transaction_Amount) AS Total FROM map_transaction
                        WHERE State = 'Rajasthan' GROUP BY District ORDER BY Total desc LIMIT 5''')
        df = pd.DataFrame(cursor.fetchall(),columns=['District','Total_Transaction'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.header("Top 5 Districts of Rajasthan with highest transaction amount")
            st.bar_chart(data=df,x="Total_Transaction",y="District",color='#46039C')
    
    
    
    #13
            
    elif select=="13. Top 5 Rajasthan Districts with Insurance users":
        cursor.execute('''Select district, sum(transaction_amount) as Insurance from map_insurance 
                       where state='Rajasthan' group by district order by Insurance desc limit 5
                       ''')
        df=pd.DataFrame(cursor.fetchall(), columns=['District','Insurance'])
        col1, col2 =st.columns(2)
        with col2:
            st.write(df)
        with col1:
            st.header("Top 5 District with Insurance Users")
            st.bar_chart(data=df, x='Insurance',y='District',color='#46039C')


 
