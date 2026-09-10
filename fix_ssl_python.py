import paramiko
import time

def install_openssl_and_python():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        print(f"\n[RUN] {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        if out:
            print(out[:500] if len(out) > 500 else out)
        if err:
            print("[ERR]", err[:500] if len(err) > 500 else err)
        return out

    # 1. Download & Build OpenSSL 1.1.1w
    run("cd /tmp && wget -q https://www.openssl.org/source/old/1.1.1/openssl-1.1.1w.tar.gz && tar -xf openssl-1.1.1w.tar.gz")
    run("cd /tmp/openssl-1.1.1w && ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl shared zlib && make -j2 && make install_sw")
    run("echo '/usr/local/openssl/lib' > /etc/ld.so.conf.d/openssl-1.1.1w.conf && ldconfig")

    # 2. Build Python 3.10 with custom OpenSSL 1.1.1w
    run("cd /tmp/Python-3.10.13 && ./configure --with-openssl=/usr/local/openssl --prefix=/usr/local/python3.10 && make -j2 && make altinstall")

    # 3. Test SSL in Python 3.10
    run("/usr/local/python3.10/bin/python3.10 -c 'import ssl; print(\"SSL SUCCESS:\", ssl.OPENSSL_VERSION)'")

    # 4. Create venv and install packages
    run("rm -rf /root/24-7-hizmat/venv")
    run("/usr/local/python3.10/bin/python3.10 -m venv /root/24-7-hizmat/venv")
    run("/root/24-7-hizmat/venv/bin/pip install --upgrade pip")
    run("/root/24-7-hizmat/venv/bin/pip install -r /root/24-7-hizmat/backend/requirements.txt")
    run("/root/24-7-hizmat/venv/bin/pip install daphne gunicorn")

    # 5. Migrate & Collectstatic
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # 6. Restart Systemd and Nginx
    run("systemctl daemon-reload")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    run("curl -I http://127.0.0.1:8000/")
    run("curl -I http://127.0.0.1/")

    print("\n--- DEPLOYMENT SUCCESSFUL! ---")
    client.close()

if __name__ == '__main__':
    install_openssl_and_python()
