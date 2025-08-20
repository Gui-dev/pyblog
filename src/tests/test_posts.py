def get_auth_token(client):
	"""Auxiliary function to get a valid authentication token"""
	user_data = {
		'email': 'post_test_user@email.com',
		'password': '123456'
	}
	client.post('/users', json=user_data)
	
	form_data = {
		'username': 'post_test_user@email.com',
		'password': '123456'
	}
	response = client.post('/token', data=form_data)
	return response.json()['access_token']


def test_get_all_posts(client):
	"""should be able to return a list of Posts"""
	response = client.get('/posts')
	assert response.status_code == 200
	assert isinstance(response.json(), list)
	

def test_should_be_able_to_get_post_by_id(client):
	"""should be able to get a post by id"""
	token = get_auth_token(client)
	post_data = {
		'title': 'Meu titulo de teste de ID',
		'content': 'Meu conteudo de teste ID'
	}
	headers = { 'Authorization': f'Bearer {token}' }
	create_response = client.post('/posts', json=post_data, headers=headers)
	post_id = create_response.json()['id']
	
	response = client.get(f'/posts/{post_id}')
	
	assert response.status_code == 200
	assert response.json()['title'] == post_data['title']

	

def test_should_be_able_to_create_a_new_post(client):
	"""Should be able to create a new post with a valid user"""
	token = get_auth_token(client)
	post_data = {
		'title': 'Meu titulo de teste',
		'content': 'Meu conteudo de teste'
	}
	headers = { 'Authorization': f'Bearer {token}' }
	response = client.post('/posts', json=post_data, headers=headers)
	
	assert response.status_code == 201
	assert response.json()['title'] == post_data['title']
	