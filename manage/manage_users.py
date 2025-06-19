from app.user_service import create_user, delete_user

delete_user('admin')
create_user('admin', 'admin', 'admin')
