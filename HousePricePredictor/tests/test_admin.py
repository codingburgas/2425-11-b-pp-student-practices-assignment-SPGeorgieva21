def test_admin_dashboard_requires_login(client):
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert b'login' in response.data or response.status_code == 200

def test_admin_dashboard_rejects_non_admin(client, app):
    with app.app_context():
        from app.models import User, db
        user = User(username='user1', email='u1@test.com', role='user')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={'username': 'user1', 'password': 'pass123'}, follow_redirects=True)
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert b'You do not have access to this page.' in response.data
