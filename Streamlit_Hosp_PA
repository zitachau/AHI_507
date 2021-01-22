#Importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time


@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

#Importing dataset
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2


def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


#Naming title of the website
st.title('Expenses in PA')

  
#Inputing description of the website
st.write('Hello! Below are some graphs and charts for PA'':sunglasses:') 
  
#Loading the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()



hospitals_pa = df_hospital_2[df_hospital_2['state'] == 'PA']


#Bar Chart
st.subheader('Types of Hospitals in PA')
bar1 = hospitals_pa['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

#Writing description for this bar chart
st.markdown('The majority of hospitals in PA are acute care, followed by psychiatric, and then critical access')


#Pie Chart
st.subheader('Pie Chart of Hospital Types in PA')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

#Writing description for this pie chart
st.markdown('77.1% of the hospitals in PA are acute care')

#Making a header
st.subheader('Map of PA Hospital Locations')

#Creating a chart with all the PA hospital locations
hospitals_pa_gps = hospitals_pa['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_pa_gps['lon'] = hospitals_pa_gps['lon'].str.strip('(')
hospitals_pa_gps = hospitals_pa_gps.dropna()
hospitals_pa_gps['lon'] = pd.to_numeric(hospitals_pa_gps['lon'])
hospitals_pa_gps['lat'] = pd.to_numeric(hospitals_pa_gps['lat'])

st.map(hospitals_pa_gps)

#Adding another header
st.subheader('Map of all Hospital Locations')

#Creating a chart with all the hospital locations
hospitals_gps = df_hospital_2['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_gps['lon'] = hospitals_gps['lon'].str.strip('(')
hospitals_gps = hospitals_gps.dropna()
hospitals_gps['lon'] = pd.to_numeric(hospitals_gps['lon'])
hospitals_gps['lat'] = pd.to_numeric(hospitals_gps['lat'])

st.map(hospitals_gps)




#Analyzing the Efficient Use of Medical Imaging
#Creating a header
st.subheader('PA Hospitals - Efficient Use of Medical Imaging')

#Making a bar chart to show how many PA hospitals have effecticient use of medical imaging
bar2 = hospitals_pa['efficient_use_of_medical_imaging_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='efficient_use_of_medical_imaging_national_comparison')
st.plotly_chart(fig2)

#Creating a description for the bar chart
st.markdown('Based on this above bar chart, we can see the majority of hospitals in the PA area are the same as the national average when it comes to efficient use of medical imaging')



#Drilling down into INPATIENT and OUTPATIENT just for PA 
st.title('Inpatient data for PA')


inpatient_pa = df_inpatient_2[df_inpatient_2['provider_state'] == 'PA']
total_inpatient_count = sum(inpatient_pa['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured' )
st.header( str(total_inpatient_count) )





#Seeing the top/bottom 10 common discharges 
common_discharges = inpatient_pa.groupby('drg_definition')['total_discharges'].sum().reset_index()

top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)




#Creating a header
st.header('DRGs')

#Making a table for top/bottom 10 DRGs
st.dataframe(common_discharges)

col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Creating bar charts of the costs 

costs = inpatient_pa.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_pa.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']

#Putting bar charts under the title 'COSTS'
st.title('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Hospitals")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_pa.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()

#writing a header for the above line
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)
