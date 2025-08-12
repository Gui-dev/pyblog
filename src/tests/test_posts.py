def test_get_all_posts(client):
	"""should be able to return a list of Posts"""
	response = client.get('/posts')
	assert response.status_code == 200
	assert isinstance(response.json(), list)