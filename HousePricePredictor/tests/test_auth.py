def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'user'
    }, follow_redirects=True)
    assert b'Successfully registered' in response.data

def test_login_success(client, user):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Successful login' in response.data or b'Welcome' in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Incorrect username or password' in response.data

def test_logout(client, user):
    client.post('/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data
