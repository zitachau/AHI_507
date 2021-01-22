#Importing packages
library(dplyr)
library(stringr)
library(reshape2)
library(tidyverse)
library(pastecs)

#Importing the dataset
dataset = read_csv('/Users/zitachau/Downloads/HAN507/data_meds_ph.csv')

#Creating a sub-sample of the dataset since it is large/random selection of 20 rows
temp = sample_n(dataset, 20)

#Previewing the set 
temp 

#Looks like there is a erraneous column 1 - lets remove 
dataset = select(dataset, -c(1))

#Confirming that it is gone: 
colnames(dataset)

#Seeing if the updates are working on the temp dataset
temp = sample_n(dataset, 20)


#Confirming the column types in our dataset
#the below function uses sapply, which means we want to apply a function to all columns/rows in 
#our dataframe, and the argument we are using is 'class', which means we want to understand the 
#class of each of the columns in our dataframe called 'dataset'
sapply(dataset, class)

#It looks like our two dates, created and date_expired have already been processed
#as being dates, which is = POSIXct / POSIXt 
#Unlike pandas/python script, we do not need to do anything to our dates

#It appears 'name' represents drug name, lets rename the column so it is more clear
#In the line below, we say that we want to rename our 'name' column into 'drug_name'
#Unlike python, we 1) can use <- which is the equivalent of our = command, 
#and 2) that when we are renaming our column, we are not using quotations 
dataset <- dataset %>% rename(drug_name = name) 

#Confirming the change has happened: 
temp = sample_n(dataset, 20)
temp
#Looks better! 

#Doing the same for 'roa' which stands for route_of_administration 
#Below, you can see that R can still take = command, which is the same thing as <- 
dataset = dataset %>% rename(route_of_admin = roa) 

#For the 'frequency' column, it looks like there is the medical abbreviation, 
#and then there is the actual human-readable form - lets make this one column 
#two columns - one with the abbreviation, and a separate one with the full description 

#Making sure that the column is a string 
newColNames <- c("frequency_abbreviation", "frequency_readible")

#We see that the abbreviation are separate by white space, 
#Giving the names of the two new columns that we want to create, which is 
# "frequency_abbreviation" and "frequency_readible", then we SPLIT the columns by the white space, 
#which is designated by " " 
newCols <- colsplit(dataset$frequency, " ", newColNames)
dataset <- cbind(dataset, newCols)

#Confirming
colnames(dataset)
#looks good! We can see our two new columns: frequency_abbreviation and frequency_readible

#Removing our old 'frequency' column since that is no needed
dataset = subset(dataset, select = -c(frequency) )

#Confirming
temp = sample_n(dataset, 20)
temp
#looks better!



#Geting the drug details OUT of the drug_details column 
#Removing the white space using str_trim and then we will search for 
#starting and stopping words, extract those to separate lists, then merge them back together
#into our dataframe

dataset$drug_details = str_trim(dataset$drug_details, side = c("both", "left", "right"))

medispan_id <- dataset$drug_details %>% str_extract("(?<='medispan_id':).*(?='name')")
ndcndf_id <- dataset$drug_details %>% str_extract("(?<='ndcndf_id':).*(?='product_name')")
product_name <- dataset$drug_details %>% str_extract("(?<='product_name':).*(?='va_id')")

drug_details_detail <- data.frame(medispan_id=medispan_id, ndcndf_id=ndcndf_id, product_name=product_name )

clean_df <- cbind(drug_details_detail, dataset)


#Looking at a subsample to make sure it worked 
temp = sample_n(clean_df, 20)
temp
#looks better!

#Understanding our missing data
missing <- data.frame(sapply(clean_df, function(x) sum(is.na(x))))

#Seeing how many unique patients we have in this DF 
sum(!duplicated(clean_df$UUID))

#Finding the average number of TOTAL medications for each patient 
counts = data.frame(clean_df %>% group_by(UUID) %>% summarize(count=n()))
mean(counts$count)

#Finding out the frequency counts for 'added_by' --> each number represents a unique physician 
added_by_counts = data.frame(table(clean_df$addedby))

#Finding out what the most commonly prescribed medication is by 'product_name'
common_meds = data.frame(table(clean_df$product_name))

#Finding out which medications have the highest re-fill rate 
refilled = data.frame(clean_df %>% 
  group_by(refills_rxed, product_name) %>%
  summarise(number = n()))

#Finding out which medications are the most prescribed by doses_rxed column
doses = data.frame(clean_df %>% 
                        group_by(doses_rxed, product_name) %>%
                        summarise(number = n()))


#Finding out what the most common route of administration is 
roa = data.frame(table(clean_df$route_of_admin))
#Looks like there might be some repeat values in ROA, we'll take care of that later 

#Looking at visualizations and means to understand if our continuous data is NORMAL 
#The only varialbes that are continuous that we are interested in here are doses_rxed and refills_rxed

#Getting the mean, median, and mode + quartiles for doses_rxed
#Making sure the column is not a string, but a integer 
clean_df$doses_rxed = as.numeric(as.character(clean_df$doses_rxed))
doses_rxed_table = summary(clean_df$doses_rxed)


#Getting the mean, median, and mode + quartiles for refills_rxed
#Making sure the column is not a string, but an integer 
clean_df$refills_rxed = as.numeric(as.character(clean_df$refills_rxed))
refills_rxed_table = summary(clean_df$refills_rxed)


#Making box plots 
boxplot(clean_df$refills_rxed)
boxplot(clean_df$doses_rxed)

#Looking at it with a histogram
hist(clean_df$refills_rxed)
hist(clean_df$doses_rxed)
