import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


conn = sqlite3.connect('data/sakila.db')

df = pd.read_sql('''
    SELECT
        rental.rental_id, rental.rental_date, rental.return_date,
        customer.last_name AS customer_lastname,
        store.store_id,
        city.city AS rental_store_city,
        film.title AS film_title, film.rental_duration AS film_rental_duration,
        film.rental_rate AS film_rental_rate, film.replacement_cost AS film_replacement_cost,
        film.rating AS film_rating
    FROM rental
    INNER JOIN customer ON rental.customer_id == customer.customer_id
    INNER JOIN inventory ON rental.inventory_id == inventory.inventory_id
    INNER JOIN store ON inventory.store_id == store.store_id
    INNER JOIN address ON store.address_id == address.address_id
    INNER JOIN city ON address.city_id == city.city_id
    INNER JOIN film ON inventory.film_id == film.film_id
    ;
''', conn, index_col='rental_id', parse_dates=['rental_date', 'return_date'])



print(df.head())



print(df.describe)



# What's the mean of film_rental_duration?

print(df['film_rental_duration'].mean())



#What's the most common rental duration?

df['film_rental_duration'].value_counts().plot(kind='bar',figsize=(14,6))
plt.show()


#What is the most common rental rate?

#Show a bar plot with all possible rental rates.
#Wich plot you think fits the best in this case? Why?

df['film_rental_rate'].value_counts().plot(kind='pie', figsize=(6,6))
#df['film_rental_rate'].value_counts().plot(kind='bar', figsize=(14,6))
plt.show()


df['film_rental_rate'].value_counts().plot(kind='bar', figsize=(14,6))
plt.show()
#This one is better



#How is the replacement cost distributed?

#Show a box plot of the replacement cost.
#Show a density plot of the replacemant cost.
#Add a red line on the mean.
#Add a green line on the median median.

df['film_replacement_cost'].plot(kind='box', vert=False, figsize=(14,6))
#df['film_replacement_cost'].value_counts().plot(kind='bar', figsize=(14,6))
plt.show()

#ax = df['film_replacement_cost'].plot(kind='density', figsize=(14,6))
#ax.axvline(df['film_replacement_cost'].mean(), color='red')
#ax.axvline(df['film_replacement_cost'].median(), color='green')



ax = df['film_replacement_cost'].plot(kind='density', figsize=(14,6))
ax.axvline(df['film_replacement_cost'].mean(), color='red')
ax.axvline(df['film_replacement_cost'].median(), color='green')
plt.show()



#How many films of each rating do we have?

#Show the raw count of each film rating.
#Show a bar plot with all possible film ratings.

print(df['film_rating'].value_counts())
#df['film_rating'].value_counts().plot(kind='bar', figsize=(14,6))
#plt.show()



df['film_rating'].value_counts().plot(kind='bar', figsize=(14,6))
plt.show()



#Does the film replacemant cost vary depending on film ratting?

#Show a grouped box plot per film rating with the film replacemant cost

df[['film_replacement_cost', 'film_rating']].boxplot(by='film_rating', figsize=(14,6))
plt.show()



#Add and calculate a new rental_days columm

df['rental_days'] = df[['rental_date', 'return_date']].apply(lambda x: (x[1] - x[0]).days, axis=1 )
print(df['rental_days'].head())



#Analyze the distribution of rental_days

#Calculate the mean of rental_days.
#Show a density (KDE) of rental_days.

print(df['rental_days'].mean())

ax = df['rental_days'].plot(kind='density', figsize=(14,6))
ax.axvline(df['rental_days'].mean(), color = 'red')
plt.show()



#Add and calculate a new film_daily_rental_rate column

#This value should be the division of film_rental_rate by film_rental_duration.

df['film_daily_rental_rate'] = df['film_rental_rate'] / df['film_rental_duration']
print(df['film_daily_rental_rate'].head())



#Analyze the destribution of film_daily_rental_rate 

#Calculate the mean of film_daily_rental_rate.
#Show a density (KDE) of film_daily_rental_rate.

print(df['film_daily_rental_rate'].mean())

ax = df['film_daily_rental_rate'].plot(kind='density', figsize=(14,6))
ax.axvline(df['film_daily_rental_rate'].mean(), color = 'red')
plt.show()



#List 10 films with the lowest daily rental rate

print(df.loc[df['film_daily_rental_rate'] == df['film_daily_rental_rate'].min()].head(10))



#List 10 films with the highest daily rental rate

print(df.loc[df['film_daily_rental_rate'] == df['film_daily_rental_rate'].max()].head(10))



#How many rentals were made in Lethbridge city?

print(df.loc[df['rental_store_city'] == 'Lethbridge'].shape[0])



#How many rentals of each film rating were made in Lethbridge city?

print(df.loc[df['rental_store_city'] == 'Lethbridge', 'film_rating'].value_counts())
df.loc[df['rental_store_city'] == 'Lethbridge', 'film_rating'].value_counts().plot(kind='bar', figsize=(14,6))
plt.show


#How many rentals were made in Woodridge city with rental duration higher than 5 days?

print(df.loc[(df['rental_store_city'] == 'Woodridge') & (df['film_rental_duration'] > 5)].shape[0])



#How many rentals were made at the store with id 2 or with replacemant cost lower than 10.99 USD?

print(df.loc[(df['store_id'] == 2) | (df['film_replacement_cost'] < 10.99)].shape[0])

