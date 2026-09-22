import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('185.196.215.231', 22, 'root', 'IB@12345678ib')

# 1. Check existing users
check_cmd = """/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py shell -c "from accounts.models import User; print('VPS Users:'); [print(u.id, u.username, u.role, u.is_superuser, u.is_staff) for u in User.objects.all()]" """
stdin, stdout, stderr = ssh.exec_command(check_cmd)
print(stdout.read().decode('utf-8'))

# 2. Create or reset superuser 'admin'
create_cmd = """/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py shell -c "from accounts.models import User; u, created = User.objects.get_or_create(username='admin'); u.set_password('admin123'); u.role = User.Role.ADMIN; u.is_superuser = True; u.is_staff = True; u.is_active = True; u.save(); print('Superuser configured successfully: username=admin, password=admin123, role=ADMIN, is_superuser=', u.is_superuser)" """
stdin, stdout, stderr = ssh.exec_command(create_cmd)
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))

ssh.close()
