# -*- coding: utf-8 -*-
"""FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yj-nHGxmQLDGmJFzigC-8YO9ztg7iNcH
"""

import pandas as pd
import numpy as np

data = pd.read_csv("Bengaluru_House_Data.csv")

"""
data.head()

data.isnull().sum()

data.dtypes
#converting nan row with location not provided on location column"""

data['location'] = data['location'].fillna('Location not provided')

"""# Replacing BHK,Bedroom,RK with only digits in size columns"""

data["size"]= data["size"].str.split(" BHK", n = 1, expand = True) 
data["size"]= data["size"].str.split(" Bedroom", n = 1, expand = True) 
data["size"]= data["size"].str.split(" RK", n = 1, expand = True)

"""# Raplacing none values with mode,mean in size,bath,balcony and other in society"""

data['size'].fillna(value=(data['size'].mode()[0]),inplace=True)
data['bath'].fillna(value=(data['bath'].mean()),inplace=True)
data['balcony'].fillna(value=(data['balcony'].mean()),inplace=True)
data['society'] = data['society'].fillna('Other')

"""# Handling with range values in total_sqft column"""

import re
x=data["total_sqft"]
a=[]
b=[]
for i in x:
  if ' - ' in str(i):
    a.append(str(i))
# a
for i in range(len(a)):
  txt=a[i]
  sp = re.split(" - ", txt)
  sum=float(sp[0])+float(sp[1])
  # print(sum/2)
  b.append(str(sum/2))
# b
m=0
for i in (x):
  if ' - ' in i:
    data['total_sqft'].replace({i:b[m]}, inplace=True)
    m+=1
z=data['total_sqft']
# z[:60]

"""# changing diff range to only sq.feet"""

for i in (data["total_sqft"]):

  if 'Sq. Meter' in str(i):
    a=re.split("Sq. Meter", str(i))
    m=float(a[0])*10.763910
    data['total_sqft'].replace({i:m}, inplace=True)
  
  elif 'Sq. Yards' in str(i):
    a=re.split("Sq. Yards", str(i))
    m=float(a[0])*9.0
    data['total_sqft'].replace({i:m}, inplace=True)

  elif 'Perch' in str(i):
    a=re.split("Perch", str(i))
    m=float(a[0])*272.25
    data['total_sqft'].replace({i:m}, inplace=True)

  elif 'Acres' in str(i):
    a=re.split("Acres", str(i))
    m=float(a[0])*43560.0
    data['total_sqft'].replace({i:m}, inplace=True)

  elif 'Cents' in str(i):
    a=re.split("Cents", str(i))
    m=float(a[0])*435.61545
    data['total_sqft'].replace({i:m}, inplace=True)

  elif 'Guntha' in str(i):
    a=re.split("Guntha", str(i))
    m=float(a[0])*1089.0
    data['total_sqft'].replace({i:m}, inplace=True)

  elif 'Grounds' in str(i):
    a=re.split("Grounds", str(i))
    m=float(a[0])*2400.0
    data['total_sqft'].replace({i:m}, inplace=True)

"""#Changing the column to float"""

data['total_sqft'] = data.total_sqft.astype(float)

data['size'] = data.total_sqft.astype(float)

data[~(data['total_sqft']/data['size'] < 350)]

data['price_per_sqft'] = data['price']*100000 / data['total_sqft']

#data.head()

# Removing outliers using help of 'price per sqrt'  taking std and mean per location
def remove_pps_outliers(data):
  df_out = pd.DataFrame()
  for key, subdf in data.groupby('location'):
    m=np.mean(subdf.price_per_sqft)
    st=np.std(subdf.price_per_sqft)
    reduced_df = subdf[(subdf.price_per_sqft>(m-st))&(subdf.price_per_sqft<=(m+st))]
    df_out = pd.concat([df_out, reduced_df], ignore_index = True)
  return df_out

data = remove_pps_outliers(data)

"""# Removing size outliers"""

# Removing size outliers
def remove_bhk_outliers(data):
  exclude_indices = np.array([])
  for location, location_df in data.groupby('location'):
    bhk_stats = {}
    for bhk, bhk_df in location_df.groupby('size'):
      bhk_stats[bhk]={
          'mean':np.mean(bhk_df.price_per_sqft),
          'std':np.std(bhk_df.price_per_sqft),
          'count':bhk_df.shape[0]}
    for bhk, bhk_df in location_df.groupby('size'):
      stats=bhk_stats.get(bhk-1)
      if stats and stats['count']>5:
        exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
  return data.drop(exclude_indices, axis='index')

data = remove_bhk_outliers(data)
#do from here

"""# here we are considering data only total no. bathroom = bhk + 1"""

# here we are considering data only total no. bathroom = bhk + 1
data = data[data.bath < data.size+2]

"""#changing area type column to 0,1,2,3"""

#data['area_type'].value_counts()

replace_area_type = {'Super built-up  Area': 0, 'Built-up  Area': 1, 'Plot  Area': 2, 'Carpet  Area': 3}
data['area_type'] = data['area_type'].map(replace_area_type)

"""# changing availability column 0,1,2"""

def replace_availabilty(my_string):
    if my_string == 'Ready To Move':
        return 0
    elif my_string == 'Immediate Possession':
        return 1
    else:
        return 2

data['availability'] = data['availability'].apply(replace_availabilty)

"""#applying label encoder to location column"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['location']= le.fit_transform(data['location'])

# data = data.drop(["size","total_sqft"], axis =1)
# data.head()

# data = pd.get_dummies(data, drop_first=True, columns=['area_type','availability','location'])
# data.shape

# data.head()

"""#deleting society column as large data missing"""

data=data.drop(['society'],axis=1)

x=data.drop(['price'],axis=1)
# x = min_max_scaler.fit_transform(x) 
y=data['price']
# y=  min_max_scaler.fit_transform(y)

from sklearn.model_selection import train_test_split
train_x,test_x,train_y,test_y = train_test_split(x,y,test_size = 0.2,random_state=56)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(train_x)
train_x= sc.transform(train_x)
test_x = sc.transform(test_x)

"""#importing different models and fiting it"""

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier
#from xgboost import XGBClassifier
#from xgboost import XGBRegressor 


from sklearn.metrics import mean_absolute_error as mae

# lr=LinearRegression()
# lr.fit(train_x,train_y)
# lr.score(test_x,test_y)

# regressor = SVR(degree=5,kernel = 'rbf')
# regressor.fit(x, y)
# regressor.score(test_x,test_y)

# model = XGBRegressor (n_estimators=30,gamma=400,max_depth=4,min_child_weight=5,random_state=42,reg_lambda=1)
'''model=XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
             colsample_bynode=0.6, colsample_bytree=1, gamma=0,
             importance_type='gain', learning_rate=0.25, max_delta_step=0,
             max_depth=4, min_child_weight=1, missing=None, n_estimators=400,
             n_jobs=1, nthread=None, objective='reg:linear', random_state=0,
             reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
             silent=None, subsample=1, verbosity=1)
model.fit(train_x,train_y)
model.score(test_x,test_y)'''

from sklearn.linear_model import LinearRegression
model = LinearRegression()

#Fitting model with trainig data
model.fit(train_x,train_y)

#Finally saving the model using pickle"""

import pickle
filename = 'model.pkl'
pickle.dump(model, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

# rfRegressor = RandomForestRegressor()
# model = rfRegressor.fit(train_x,train_y)
# model.score(test_x,test_y)

# dtReg = DecisionTreeRegressor()
# model = dtReg.fit(train_x,train_y)
# model.score(test_x,test_y)

# l=Lasso()
# model=l.fit(train_x,train_y)
# model.score(test_x,test_y)

# r=Ridge()
# model=r.fit(train_x,train_y)
# model.score(test_x,test_y)

train_predict = model.predict(train_x) 
k = mae(train_predict,train_y)
print("Mean Absolute Error in predicting on training set:",k)

test_predict = model.predict(test_x) 
k = mae(test_predict,test_y)
print("Mean Absolute Error in predicting on test set:",k)

from sklearn import metrics
import numpy as np
print('Mean Absolute Error:', metrics.mean_absolute_error(test_predict,test_y)) 
print('Mean Squared Error:', metrics.mean_squared_error(test_predict,test_y))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(test_predict,test_y)))

list(x.columns)

# it help to get predicted value of hosue  by providing features value 
def predict_house_price(model,area_type,availability,location,size,total_sqft,bath,balcony,price_per_sqft):

  array =np.zeros(len(x.columns)) # create zero numpy array, len = 107 as input value for model

  # adding feature's value accorind to their column index
  array[0]=area_type
  array[1]=availability
  array[2]=location
  array[3]=size
  array[4]=total_sqft
  array[5]=bath
  array[6]=balcony
  array[7]=price_per_sqft
  
    # feature scaling
  array = sc.transform([array])[0] # give 2d np array for feature scaling and get 1d scaled np array
  return model.predict([array])[0] # return the predicted value by train model
"""
predict_house_price(model=model, bath=3,balcony=2,total_sqft=1672,size=3,price_per_sqft=8971.291866,area_type=2,availability=0,location=285)

predict_house_price(model=model, bath=3,balcony=2,total_sqft=1672,size=3,price_per_sqft=8571.428571,area_type=0,availability=0,location=285)

predict_house_price(model=model, bath=3,balcony=2,total_sqft=1672,size=3,price_per_sqft=8514.285714,area_type=1,availability=0,location=285)

"""

"""#Finally saving the columns in json

import json
columns={'data_columns': [col.lower() for col in x.columns]}
with open("columns.json","w") as f:
  f.write(json.dumps(columns))"""

