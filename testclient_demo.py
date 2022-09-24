from app import app
users_data = [
   {'username': 'user1', 'password': '12345'},
   {'username': 'user2', 'password': '12345'},
   {'username': 'user3', 'password': '12345'},
]


test_client = app.test_client()
# response = test_client.get('/users')
response = test_client.get('/users/2')
print("json = ", response.json)
print("code = ", response.status_code)

res = test_client.delete('/users/2')
print(res.data)

response = test_client.get('/users/2')
print("json = ", response.json)
print("code = ", response.status_code)