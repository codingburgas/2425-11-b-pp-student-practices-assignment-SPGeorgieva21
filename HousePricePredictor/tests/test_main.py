def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data
