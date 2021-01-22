#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 12:00:06 2020

@author: zitachau
"""

import pandas as pd
import numpy as np

#importing the dataset and defining the csv file as 'df'
df = pd.read_csv('/Users/zitachau/Downloads/HAN507/data_meds_ph.csv')

#Seeing how many rows and columns are in the dataset
print(df)

#Creating a temporary dataset with a random selection of 50 rows
temp = df.sample(50)

#Previewing the set
temp

#Seeing what the column names are
list(temp)

#Transforming 'created' column into date-time format
df['created'] = pd.to_datetime(df['created'])

#Renaming column from 'is_admin_record' TO 'externally_prescribed'
df = df.rename(columns = {'is_admin_record': 'externally_prescribed'}, inplace = False)

#Confirming that the change has happened
temp = df.sample(50)
temp

#Finding features in the nested column 'drug_details'
drug_details = df.drug_details.apply(eval)
drug_details.tolist()

#Seeing how many unique patients there are
df.UUID.nunique()

#Looking for missing data
df.isnull().sum()

#Finding the mean number of medications per patient
counts = df.groupby(['UUID']).size().reset_index(name='total_med_counts')
counts.total_med_counts.mean()

#Finding the 3 most commonly/least commonly prescribed medications
df.name.value_counts()

#Finding the most common route of administration
df.roa.value_counts()

#Finding the medication that has the 2nd highest prescription refill rate
df.groupby(['refills_rxed','name']).size()

#Finding the mean, median, and mode + quartiles for 'doses_rxed'
df['doses_rxed'] = pd.to_numeric(df['doses_rxed'], errors='coerce')
doses_rxed_table = pd.DataFrame(df.doses_rxed.describe())
df.doses_rxed.describe()

#Finding mode/median for 'doses_rxed'
df["doses_rxed"].mode()
df["doses_rxed"].median()


#Finding the mean, median, and mode + quartiles for 'refills_rxed'
df['refills_rxed'] = pd.to_numeric(df['refills_rxed'], errors='coerce')
refills_rxed_table = pd.DataFrame(df.refills_rxed.describe())
df.refills_rxed.describe()

#Finding mode/median for 'refills_rxed'
df["refills_rxed"].mode()
df["refills_rxed"].median()




#Importing packages
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import norm




#Visualizations in boxplot and histogram for 'doses_rxed' and 'refills_rxed'

#Making a box plot for 'doses_rxed' and 'refills_rxed'
ax = sns.boxplot(x=df["doses_rxed"])
sns.distplot(df['doses_rxed'], fit=norm)


#Making a box plot for 'refills_rxed'
ax = sns.boxplot(x=df["refills_rxed"])
sns.distplot(df['refills_rxed'], fit=norm)
