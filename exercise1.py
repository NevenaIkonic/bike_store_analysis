import pandas as pd
import matplotlib.pyplot as plt

#Load the Dataset
sales = pd.read_csv('C:\\Users\\Nena\\Desktop\\Python_projekti\\data\\sales_data.csv', parse_dates=['Date'])


#Preview the Data
print("First five rows of the dataset:")
print(sales.head())

#Basic Dataset Information
print("\nDataset information:")
print(sales.info())

#Check for Missing Values
print("\nMissing values per column:")
print(sales.isnull().sum())

#What's the mean of Customers_Age?
print(sales['Customer_Age'].mean())
sales['Customer_Age'].plot(kind ='kde', figsize=(14, 6))
sales['Customer_Age'].plot(kind='box', vert=False, figsize=(14, 6))

#What's the mean of Order_Quantity?
sales['Order_Quantity'].mean()
sales['Order_Quantity'].plot(kind='box', vert=False, figsize=(14, 6))

sales['Order_Quantity'].plot(kind='hist',bins=30, figsize=(14, 6))

#How many sales per year do we have?
sales['Year'].value_counts()
sales['Year'].value_counts().plot(kind='pie', figsize=(6,6))

#How many sales per month do we have?
sales['Month'].value_counts()
sales['Month'].value_counts().plot(kind='bar', figsize=(14 , 6))

#Which country has the most sales quantity of sales?
sales['Country'].value_counts().head(1)
sales['Country'].value_counts()
sales['Country'].value_counts().plot(kind='bar',figsize=(14 , 6))

#Create a list of every product sold
sales['Product'].unique()
sales['Product'].value_counts().head(10).plot(kind='bar', figsize=(14, 6))

#Can you see any relationship between Unit_Cost and Unit_Price?
sales.plot(kind='scatter', x='Unit_Cost', y='Unit_Price', figsize=(6, 6))

#Can you see any relationship between Order_Quantity and Profit?
sales.plot(kind='scatter', x='Order_Quantity', y='Profit', figsize=(6, 6))

#Can you see any relationship between Profit per Country?
sales[['Profit','Country']].boxplot(by='Country', figsize=(10, 5))
#sales.plot(kind='scatter', x='Order_Quantity', y='Profit', figsize=(6, 6))
sales.plot(kind='scatter', x='Country', y='Profit', figsize=(6, 4))

#Can you see any relationship between the Customer_Age per Country?
sales[['Customer_Age', 'Country']].boxplot(by='Country', figsize=(10, 5))
sales.plot(kind='scatter', x='Country', y='Customer_Age', figsize=(6, 4))

#Add and calculate a new Calculated_Date column
sales['Calculated_Date'] = sales[['Year', 'Month', 'Day']].apply(lambda x: '{}-{}-{}'.format(x[0],x[1],x[2]), axis=1)
#sales['Calculated_Date'] = sales[['Year', 'Month', 'Day']].apply(lambda x: '{}-{}-{}'.format(x[0], x[1], x[2]), axis=1)

sales['Calculated_Date'].head()

#Parse your Calculated_Date column into a datetime object
sales['Calculated_Date'] = pd.to_datetime(sales['Calculated_Date'])
sales['Calculated_Date'].head()

#How did sales evolve through the years?
sales['Calculated_Date'].value_counts().plot(kind='line', figsize=(14, 6))

#Increase 50 U$S revenue to every sale
sales['Revenue'] += 50

#How many orders were made in Canada or France?
sales.loc[(sales['Country'] == 'Canada') | (sales['Country'] == 'France')].shape[0]
#france_states = sales.loc[sales['Country'] == 'France', 'State'].value_counts()

#How many Bike Racks orders were made from Canada?
sales.loc[(sales['Country'] == 'Canada') & (sales['Sub_Category'] == 'Bike Rocks')].shape[0]
#sales.loc[(sales['Country'] == 'Canada') & (sales['Sub_Category'] == 'Bike Racks')].shape[0]

#How many orders were made in each region (state) of France?
france_states = sales.loc[sales['Country'] == 'France', 'State' ].value_counts()
france_states

#Go ahead and show bar plot with the results:
france_states.plot(kind='bar',figsize=(14,6))

#How many sales were made per category?
sales['Product_Category'].value_counts()

#Go ahead and show a pie plot with the results:
sales['Product_Category'].value_counts().plot(kind='pie', figsize=(6,6))

#How many orders were made per accesory sub-categories?
accessories = sales.loc[sales['Product_Category'] == 'Accessories', 'Sub_Category'].value_counts()
accessories

#Go ahead and show a bar plot with the results:
accessories.plot(kind='bar', figsize=(14,6))

#How many orders were made per bike sub-categories?
bikes = sales.loc[sales['Product_Category'] == 'Bikes', 'Sub_Category'].value_counts()
bikes

#Go ahead and show a pie plot with the results:
bikes.plot(kind='pie', figsize=(6,6))

#Which gender has the most amount of sales?
sales['Customer_Gender'].value_counts()
sales['Customer_Gender'].value_counts().plot(kind='bar')

#How many sales with more than 500 in Revenue were made by men?
sales.loc[(sales['Customer_Gender'] == 'M') & (sales['Revenue'] == 500)].shape[0]

#Get the top 5 sales with the highest revenue
sales.sort_values(['Revenue'], ascending=False).head(5)

#Get the sale with the highest revenue
#sales.sort_values(['Revenue'], ascending=False).head(1)
cond = sales['Revenue'] == sales['Revenue'].max()
sales.loc[cond]

#What is the mean Order_Quantity of orders with more than 10k in revenue?
cond = sales['Revenue']> 10_000
sales.loc[cond, 'Order_Quantity'].mean()

#What is the mean Order_Quantity of orders with less than 10k in revenue?
cond = sales['Revenue'] < 10_000
sales.loc[cond, 'Order_Quantity'].mean()

#How many orders were made in May of 2016?
cond = (sales['Year'] == 2016) & (sales['Month'] == 'May')
sales.loc[cond].shape[0]

#How many orders were made between May and July of 2016?
cond = (sales['Year'] == 2016) & (sales['Month'].isin(['May','June','July']))
sales.loc[cond].shape[0]

#Show a grouped box plot per month with the profit values.
profit_2016 = sales.loc[sales['Year'] == 2016, ['Profit', 'Month']]
profit_2016.boxplot(by='Month', figsize=(14,6))


#Add 7.2% TAX on every sale Unit_Price within United States
#sales.loc[sales['Country'] == 'United States', 'Unit_Price'] = sales.loc[sales['Country'] == 'United States', 'Unit_Price'] * 1.072
sales.loc[sales['Country'] == 'United States', 'Unit_Price'] *= 1.072