#Installing packages
install.packages("DBI")
install.packages("dplyr")
install.packages("ggpubr")
install.packages("moments")
install.packages("car")
install.packages("stringr")
install.packages("psych")
install.packages("vcd")
install.packages("summarytools")
install.packages("nortest")
install.packages("CGPfunctions")
install.packages("pwr")
install.packages("odbc")

library(DBI)
library(dplyr)
library("ggpubr")
library(moments)
library(car)
library(stringr)
library(psych)
library(vcd)
library(summarytools)
library(nortest)
library(CGPfunctions)
library(pwr)

#Connecting to DBA
con <- DBI::dbConnect(odbc::odbc(),
                      Driver    = "MySQL", 
                      Server    = "---",
                      Database = "---",
                      UID       = "---",
                      PWD       = "---",
                      Port      = "---")

df <- dbReadTable(con, "ahi_zita")

#Picking at least 2-3 categorical variables (IVs - factors) and at least 1 DV (continuous)
df_sub = df %>% select ('num_medications', 'race', 'gender', 'age', 'medical_specialty')

#Renaming the columns: 
df_sub <- df_sub %>% rename('medcount' = 'num_medications', 'category' = 'medical_specialty', 'sex' = 'gender')

#Making sure the data varaible (continuous) is really continuous data / 
df_sub$medcount = as.numeric(df_sub$medcount)



#Recoding category
veryfrequent = c("InternalMedicine", "Emergency/Trauma", "Family/GeneralPractice",
                 "Cardiology", "Surgery-General")

frequent = c("Nephrology", "Orthopedics", "Orthopedics-Reconstructive",
                   "Radiologist")

df_sub$category_coded = ifelse(df_sub$category %in% veryfrequent, "Veryfrequent", 
                               ifelse(df_sub$category %in% frequent, "Frequent", "Notfrequent"))



#Recoding age
adolescent = c("0-10", "10-20")
elderly = c("60-70", "70-80", "80-90", "90-100")

df_sub$age_coded = ifelse(df_sub$age %in% adolescent, "Adolescent", 
                          ifelse(df_sub$age %in% elderly, "Elderly", "Middle-Aged"))

df_sub$age_coded_simple = ifelse(df_sub$age %in% adolescent, "Adolescent", "Middle-Aged")


#Recoding race
white = c("Caucasian")

df_sub$race_coded = ifelse(df_sub$race %in% white, "white", "not_white")


#Finding pValue using ANOVA with NO-INTERACTION 
res.aov2 <- aov(medcount ~ race_coded + age_coded_simple, data = df_sub)
summary(res.aov2)

#We see that the pValue for medcount on race and age is <2e-16. Which means it's
#not normally distributed
#So, we're thinking that there is a main effect for medcount on race and age. Older patients are
#more likely to have a higher medcount than younger patients. African Americans 
#patients are more likely to to have a higher medcount than Caucasian patients.
#You can see from the code below that race and age affects the mean


#Two-way ANOVA with interaction effect
res.aov3 <- aov(medcount ~ race * category_coded, data = df_sub)
summary(res.aov3)

#We see that the pValue for medcount on race and age is <2e-16. Which means it's
#not normally distributed
#So, there is an interaction effect for medcount on category and race based on
#the small pValue we've gotten from the code on line 92


#Visualization for medcount and category_coded
Plot2WayANOVA(medcount ~ category_coded * race, df_sub, plottype = "line")
