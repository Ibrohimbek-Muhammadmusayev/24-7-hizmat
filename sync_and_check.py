import paramiko

def sync_and_check():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        return out, err

    run("cd /root/24-7-hizmat && git fetch --all && git reset --hard origin/main")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")

    # Check DB counts
    out, err = run("cd /root/24-7-hizmat/backend && /usr/local/python3.10/bin/python3.10 manage.py shell -c 'from accounts.models import User; from orders.models import Order; from categories.models import Category; print(\"Users:\", User.objects.count()); print(\"Orders:\", Order.objects.count()); print(\"Categories:\", Category.objects.count())'")
    print("OUTPUT:\n", out)
    if err:
        print("ERROR:\n", err)

    client.close()

if __name__ == '__main__':
    sync_and_check()
