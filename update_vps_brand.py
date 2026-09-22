import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('185.196.215.231', 22, 'root', 'IB@12345678ib')

cmd = """/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py shell -c "from bot_control.models import BotConfig; c = BotConfig.get_config(); c.project_name = 'IshBazari'; c.save(); print('VPS DB updated to:', c.project_name)" """

stdin, stdout, stderr = ssh.exec_command(cmd)
print("OUT:", stdout.read().decode('utf-8'))
print("ERR:", stderr.read().decode('utf-8'))

ssh.exec_command("systemctl restart 24-7-web && systemctl restart 24-7-bot")
ssh.close()
print("Done!")
