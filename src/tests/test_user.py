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


def test_should_be_able_to_get_all_users(client):
	"""should be able to return all users"""
	user_data = {
		'email': 'test_all_users@email.com',
		'password': '123456',
	}
	client.post('/users', json=user_data)
	
	response = client.get('/users')
	
	assert response.status_code == 200
	assert isinstance(response.json(), list)
	assert len(response.json()) > 0
    


def test_should_be_able_to_get_user_by_id(client):
	"""should be able to get user by id"""
	user_data = {
		'email': 'test_user_by_id@email.com',
		'password': '123456',
	}
	create_response = client.post('/users', json=user_data)
	user_id = create_response.json()['id']
	
	response = client.get(f'/users/{user_id}')
	assert response.status_code == 200
	assert response.json()['email'] == user_data['email']
	

def test_should_be_able_to_return_404_user_not_found(client):
	"""should be able to return 404 if user not found"""
	
	user_not_exists = 9999
	
	response = client.get(f'/users/{user_not_exists}')
	assert response.status_code == 404
	
	
	
	
	