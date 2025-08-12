def test_create_user(client):
	"""should be able to create a new user"""
	user_data = {
		'email': 'test@email.com',
		'password': '123456',
	}
	response = client.post('/users', json=user_data)
	
	assert response.status_code == 201
	assert response.json()['email'] == user_data['email']
	assert 'id' in response.json()