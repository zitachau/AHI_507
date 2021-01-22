#Data Preprocessing Tools

#Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
from scipy.stats import norm



#Importing the dataset
dataset = pd.read_csv('/Users/zitachau/Downloads/HAN507/data_meds_ph.csv')


#Creating a sub-sample of the dataset since it is large/random selection of 20 rows
temp = dataset.sample(20)

#Previewing the set
temp 

#Since there is an erraneous column 1 - lets remove 
dataset = dataset.drop(columns=['Unnamed: 0'])

#Confirming that it's gone
list(dataset)

#Making sure that updates are working on the temp dataset
temp = dataset.sample(20)




#Looking what additional cleaning should happen, first up is date columns
#Transforming the date columns to actual dates
#Seeing what the column names are
list(temp)

#Appears they are 'created' and 'date_expired'
#Lets transform those to actual date/times
dataset['created'] = pd.to_datetime(dataset['created'])

#Confirming
#Updating our temp dataset, and then order that column from earliest to latest dates
temp = dataset.sample(20)
temp = temp.sort_values(by=['created'])

#Looks good
#Doing the same to the other date column 
dataset['date_expired'] = pd.to_datetime(dataset['date_expired'])

#Confirming and double checking here as well: 
temp = dataset.sample(20)
temp = temp.sort_values(by=['date_expired'])




#Seeing what other data cleaning might be warranted: 
temp 

#It appears 'name' represents drug name, lets rename the column so it is more clear
dataset = dataset.rename(columns = {'name': 'drug_name'}, inplace = False)

#Confirming change: 
temp = dataset.sample(20)
temp
#looks better!


#Doing the same for 'roa' which stands for route_of_administration 
dataset = dataset.rename(columns = {'roa': 'route_of_admin'}, inplace = False)






#For the 'frequency' column, it looks like there is the medical abbreviation, and then
#there is the actual human-readable form - lets make this one column to two columns - 
#one with the abbreviation, and a seperate one with the full description

#Making sure that the column is a string 
dataset["frequency"] = dataset["frequency"].astype(str)

#Seeing that the abbreviation and seperated by some white space, so in the code, we're
#going to give the names of the two new columns that we want to create, which is 
# "frequency_abbreviation" and "frequency_readible", then we SPLIT the columns by the white space, 
#which is designated by " " 
dataset[["frequency_abbreviation", "frequency_readible"]]= dataset["frequency"].str.split(" ", n = 1, expand = True) 


#Confirming that it worked 
temp = dataset.sample(20)
temp

#Great! But, looks like we should remove our old 'frequency' column since that is no 
#longer needed, and lets remove the ( ) from our last new variable that we created, 'frequency_readible'

dataset = dataset.drop(columns=['frequency'])
dataset['frequency_readible']= dataset['frequency_readible'].str.replace('(', '')
dataset['frequency_readible']= dataset['frequency_readible'].str.replace(')', '')

#Confirming
temp = dataset.sample(20)
temp
#looks better!


#Cleaning up the drug details column - this right now is in the structure of a DICTIONARY, but it is a string 
#First, lets convert the string to a dictionary, and then get the nested information out 
drug_details = df.drug_details.apply(eval)


#Confirming that it worked, but getting the first medispan ID value
drug_details[0]['medispan_id']

#looks good! 




#Geting the columns we want - medispan ID, NDC number, and product name
#and create this as a new dataframe
drug_details_pd = pd.DataFrame(drug_details.tolist(), columns=['medispan_id', 'ndcndf_id', 'product_name'])

#because we have the same amount of rows in our new drug_details_pd as our original dataset, 
#we're going to merge the two dataframes together into a new DF called clean_df
clean_df = df.merge(drug_details_pd, how='left', left_index=True, right_index=True)






#Understanding our missing data
df_missing = pd.DataFrame(clean_df.isnull().sum())
df_missing = df_missing.reset_index() #This resets the index, so our index now becomes a column variable that we can filter by 

#Seeing how many unique patients we have in this DF 
clean_df.UUID.nunique()

#Finding how the average number of TOTAL medications for each patient 
counts = clean_df.groupby(['UUID']).size().reset_index(name='total_med_counts') #this is grouping each row by UID - 
counts.total_med_counts.mean()

#Finding out the frequency counts for 'added_by' --> each number represents a unique physician 
added_by_counts = pd.DataFrame(clean_df.addedby.value_counts())
added_by_counts = added_by_counts.reset_index()

#Finding out what the most commonly prescribed medication is by 'product_name'
common_meds = pd.DataFrame(clean_df['product_name'].value_counts())
common_meds = common_meds.reset_index()

#Finding out which medications have the highest re-fill rate 
refilled = pd.DataFrame(clean_df.groupby(['refills_rxed','product_name']).size())
refilled = refilled.reset_index()

#Finding out which medications are the most prescribed by doses_rxed column
doses = pd.DataFrame(clean_df.groupby(['doses_rxed','product_name']).size())
doses = doses.reset_index()

#Finding out what the most common route of administration is 
roa = pd.DataFrame(clean_df['route_of_admin'].value_counts())
roa = roa.reset_index()
#Looks like there might be some repeat values in ROA, we'll take care of that later 




#Looking at some visualizations and means to understand if our continuous data is NORMAL 
#The only varialbes that are continuous that we are interested in here are doses_rxed and refills_rxed

#Getting the mean, median, and mode + quartiles for doses_rxed
#Making sure the column is not a string, but an integer 
clean_df['doses_rxed'] = pd.to_numeric(clean_df['doses_rxed'], errors='coerce')
doses_rxed_table = pd.DataFrame(clean_df.doses_rxed.describe())

#Geting the mean, median, and mode + quartiles for refills_rxed
#Making sure the column is not a string, but a integer 
clean_df['refills_rxed'] = pd.to_numeric(clean_df['refills_rxed'], errors='coerce')
refills_rxed_table = pd.DataFrame(clean_df.refills_rxed.describe())


#Making a box plot for doses_rxed 
ax = sns.boxplot(x=clean_df["doses_rxed"])

#Making a box plot for refills_rxed
ax = sns.boxplot(x=clean_df["refills_rxed"])

#Creating a histogram of doses_rxed 
sns.distplot(clean_df['doses_rxed'], fit=norm)

#Creating a histogram of doses_rxed 
sns.distplot(clean_df['refills_rxed'], fit=norm)
