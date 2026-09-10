import paramiko
import time

def install_deps_and_run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        print(f"\n[RUN] {cmd}")
        if out:
            print("[OUT]", out[:200])
        if err:
            print("[ERR]", err[:200])
        return out, err

    # Install system imaging libraries for pillow
    run("DEBIAN_FRONTEND=noninteractive apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk")

    # Install pip packages with --only-binary :all: or individual
    run("/usr/local/python3.10/bin/pip3.10 install django djangorestframework djangorestframework-simplejwt django-cors-headers channels daphne python-telegram-bot requests python-dotenv gunicorn")
    run("/usr/local/python3.10/bin/pip3.10 install pillow")

    # Test django import
    run("/usr/local/python3.10/bin/python3.10 -c 'import django; print(\"DJANGO READY:\", django.get_version())'")

    # Run Django Migrations & Collectstatic
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py migrate")
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # Restart Services
    run("systemctl daemon-reload")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    out8000, _ = run("curl -I http://127.0.0.1:8000/")
    out80, _ = run("curl -I http://127.0.0.1/")
    print("\n--- FINAL LIVE CHECK ---")
    print("PORT 8000:", out8000.strip())
    print("PORT 80 (NGINX):", out80.strip())

    client.close()

if __name__ == '__main__':
    install_deps_and_run()
