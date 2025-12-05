import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boiler_analysis.settings')
django.setup()

from users.models import User

# 테스트 유저 생성
if not User.objects.filter(user_name='test').exists():
    user = User.objects.create_user(
        user_name='test',
        password='test1234'
    )
    print(f'User created: {user.user_name}')
else:
    print('User already exists')
