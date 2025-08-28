import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# 관리자 계정 생성
username = 'admin'
email = 'admin@hanaart.com'
password = 'hana1234!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"관리자 계정이 생성되었습니다.")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print("관리자 계정이 이미 존재합니다.")

# 추가 스태프 계정 생성
staff_username = 'manager'
staff_email = 'manager@hanaart.com'
staff_password = 'manager1234!'

if not User.objects.filter(username=staff_username).exists():
    staff_user = User.objects.create_user(
        username=staff_username, 
        email=staff_email, 
        password=staff_password
    )
    staff_user.is_staff = True
    staff_user.first_name = '관리'
    staff_user.last_name = '담당자'
    staff_user.save()
    print(f"\n매니저 계정이 생성되었습니다.")
    print(f"Username: {staff_username}")
    print(f"Password: {staff_password}")
else:
    print("매니저 계정이 이미 존재합니다.")