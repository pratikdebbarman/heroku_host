import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'area_type':0, 'availability':0, 'location':285, 'size':3, 'total_sqft':1672, 'bath':3, 'balcony':2 , 'price_per_sqft':8971})

print(r.json())
