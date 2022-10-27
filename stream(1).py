# 引入包，将作业使用的包都放在这里一并引入
# 如有可视化设置，也在这里写明
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
st.title("data")
df=pd.read_csv('Train.csv')
df = df.sample(5000).reset_index(drop=True)

if st.checkbox('Show dataframe'):
    df

#每列特征含义
st.write("Means of data：")
st.write("ID: ID Number of Customers.")
st.write("Warehouse block: The Company have big Warehouse which is divided in to block such as A,B,C,D,E.")
st.write("Mode of shipment:The Company Ships the products in multiple way such as Ship, Flight and Road.")
st.write("Customer care calls: The number of calls made from enquiry for enquiry of the shipment.")
st.write("Customer rating: The company has rated from every customer. 1 is the lowest (Worst), 5 is the highest (Best).")
st.write("Cost of the product: Cost of the Product in US Dollars.")
st.write("Prior purchases: The Number of Prior Purchase.")
st.write("Product importance: The company has categorized the product in the various parameter such as low, medium, high.")
st.write("Gender: Male and Female.")
st.write("Discount offered: Discount offered on that specific product.")
st.write("Weight in gms: It is the weight in grams.")
st.write("Reached on time: It is the target variable, where 1 Indicates that the product has NOT reached on time and 0 indicates it has reached on time.")

st.title("questions one")
#"仓库区域和是否到达的是否运达有没有关系")
st.write("Whether the warehouse area is related to whether the goods arrive or not")
p=plt.figure()
sns.barplot(x='Warehouse_block',y='Reached.on.Time_Y.N',data=df,palette='Spectral')
st.pyplot(p)
#仓库地区对是否运达基本没有影响")
st.write("The warehouse area has little influence on the delivery")

st.title("questions two")
#"不同的装运方式,重要性和到达率之间的关系")
st.write("Relationship between different shipping methods, importance and arrival rate")
p=plt.figure()
sns.barplot(x='Mode_of_Shipment',y='Reached.on.Time_Y.N',data=df,hue='Product_importance',palette='ch:s=-.2,r=.6')
st.pyplot(p)
#不同的装运方式的到达率基本一致，但是重要性更高的产品到达率相对更高")

st.title("plots")

#"用热力图查看各个特征之间是否具有相关性")
st.write("Check whether each feature is related with each other with hot diagram")
#"颜色对应相关性在右侧条形显示，正负值分别代表正反相关，值越接近1、-1代表相关性越大.可以看到商品价格和重量之间没有绝对的关系")
p=plt.figure()
sns.heatmap(df.corr(),annot=True)
st.pyplot(p)

#产品折扣和重量的关系
st.write("Relationship between product discount and weight")
#"根据这张图表，可以看到大多数产品的折扣低于10美元，重量超过4公斤的产品折扣不超过10美元，有些例外。")
f, ax = plt.subplots(figsize=(15, 8))
sns.despine(f, left=True, bottom=True)
sns.scatterplot(x="Discount_offered", y="Weight_in_gms",
                palette="ch:r=-.2,d=.3_r",
                sizes=(1, 8), linewidth=0,
                data=df, ax=ax)
st.pyplot(f)


#运输方式，产品成本与数量
st.write("Transportation mode, product cost and quantity")
#"每种颜色代表不同运输方式，横轴表示产品成本，纵轴表示数量，可以看到无论产品的成本多少，大部分都选择用船的方式进行运输，其余两种运输方式比例类似")
f=plt.figure(figsize=(10,6))
df[df['Mode_of_Shipment']=='Flight']['Cost_of_the_Product'].hist(alpha=0.5,color='blue',bins=30,label='Flight')
df[df['Mode_of_Shipment']=='Road']['Cost_of_the_Product'].hist(alpha=0.5,color='red',bins=30,label='Road')
df[df['Mode_of_Shipment']=='Ship']['Cost_of_the_Product'].hist(alpha=0.5,color='grey',bins=30,label='Ship')
plt.xlabel('COST')
plt.legend()
st.pyplot(f)


#"用折线图表示货物区域，客户评估等级和是否到达之间的关系")
st.write("Use a line chart to show the cargo area, and the relationship between the customer's evaluation level and whether the goods arrive")
f=plt.figure(figsize=(10,6))
sns.lineplot(x='Warehouse_block',y='Customer_rating',hue='Reached.on.Time_Y.N',data=df).set_title('Warehouse_block VS Customer_rating lineplot')
st.pyplot(f)

st.sidebar.header("filtering widgets")
st.title("filtering widgets")
input= st.sidebar.number_input('Which index data do you want to watch?(<5000)',value=0, min_value = 0, max_value = 10)
st.write("watch input index data")
data=pd.DataFrame(df.iloc[[input]])
st.dataframe(data)


options = st.sidebar.multiselect(
   'What Warehouse_block do you want to show',
    ('A', 'B', 'C','D','E','F'), ('A'))

st.write("watch Warehouse_block filter data")
for i in options:
    df.loc[df['Warehouse_block']==i]


values = st.sidebar.slider(
'Select a range of values in cost of the product',
   df['Cost_of_the_Product'].min(), df['Cost_of_the_Product'].max(),(120,250))
filter=df.loc[(df['Cost_of_the_Product']<=values[1]) & (df['Cost_of_the_Product']>=values[0])]
st.write("watch cost of the product filter data")
st.dataframe(filter)