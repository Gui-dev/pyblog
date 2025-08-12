def test_get_valid_token(client):
	"""should be able to login with the correct credentials"""
	user_data = {
		'email': 'test_auth@email.com',
		'password': '123456',
	}
	client.post('/users', json=user_data)
	
	form_data = {
		'username': 'test_auth@email.com',
		'password': '123456',
	}
	
	response = client.post('/token', data=form_data)
	
	assert response.status_code == 200
	assert 'access_token' in response.json()
	assert response.json()['token_type'] == 'bearer'