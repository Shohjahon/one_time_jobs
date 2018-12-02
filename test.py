import  requests
response = requests.get("https://data.gov.uz/uz/api/v1/json/dataset/3397/version/12561?access_key=10448a8848f8a88633a4961c0e6e19a8", verfy=False)

# Get the response data as a python object.  Verify that it's a dictionary.
data = response.json()
print(type(data))