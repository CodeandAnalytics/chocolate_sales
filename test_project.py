from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv("credential.env")



db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS") 
db_host = os.getenv("DB_HOST","localhost")
db_port = os.getenv("DB_PORT",5432)
db_name = os.getenv("DB_NAME","testdb")


engine = create_engine(f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")
query = "SELECT * FROM chocolate_sales"
df = pd.read_sql(query, engine)
# print(df.to_string())
engine.dispose()

df_selected = df[['sales_person','country','product']]
print(df_selected.to_string())


df['sale_date'] = pd.to_datetime(df['sale_date'])
monthly_sales = df.groupby(df['sale_date'].dt.to_period('M'))['revenue'].mean().round(2)
print(monthly_sales)

month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']

for i, value in enumerate(monthly_sales):
     plt.text(i, value + 7, str(value), ha='center', fontsize=10, color='k')

sns.barplot(x=month,y=monthly_sales.values,width=0.4,palette='Spectral',hue=month,legend=True)

plt.xlabel('Month',fontdict={'fontsize':12,'fontweight': 'bold','color':'k'})
plt.ylabel('Sales',fontdict={'fontsize':12,'fontweight': 'bold','color':'k'})
plt.title('Monthly_Sales',fontdict={'fontsize':15,'fontweight': 'bold','color':'k'})
plt.legend(title='Month',loc='upper center',bbox_to_anchor=(1.05,1))
plt.show()


top_salesperson = df.groupby('sales_person')['revenue'].sum().nlargest(3)
print(f"Top 3 Sales_person:",{top_salesperson})


repeat_customers = df['sales_person'].value_counts().nlargest(3)
high_value_customer= repeat_customers[repeat_customers > 3]
print(f"high_value_customer:",{high_value_customer})


filtered_product = df.groupby('product')['quantity_sold'].sum()
print(filtered_product)
After_Nines = filtered_product[filtered_product.index == 'After Nines']
print(After_Nines)


highest_selling_product = filtered_product.idxmax()
highest_selling_quantity = filtered_product.max
print(f"Highest selling product: {highest_selling_product} (Sold: {highest_selling_quantity})")


country_sales = df.groupby('country')['revenue'].sum()
print(country_sales)


Country =['Australia','Canada','India','New Zealand','UK','USA']
ex = [0,0,0,0,0,0.2]
plt.figure(figsize=(4,4),facecolor='lightgrey')
plt.pie(country_sales,labels= Country,autopct='%1.1f%%',explode=ex,shadow='k',
        textprops={'color':'k','fontsize':11,'fontweight':'bold'},startangle=190,
        )
plt.title('contry_wise_revenue',fontdict={'fontsize': 18,'fontweight':'bold'})
plt.legend(title='Country',loc='upper right',bbox_to_anchor=(1.5,1))
plt.show()





