import paramiko

def configure_domain():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        print(f"\n[RUN] {cmd}")
        if out:
            print("[OUT]", out[:300])
        if err:
            print("[ERR]", err[:300])
        return out, err

    # 1. Update Django ALLOWED_HOSTS
    run("python3 -c \"path='/root/24-7-hizmat/backend/config/settings.py'; content=open(path).read(); content=content.replace('ALLOWED_HOSTS = [\\'*\\']', 'ALLOWED_HOSTS = [\\'*\\', \\'ishtop24.uz\\', \\'admin.ishtop24.uz\\', \\'api.ishtop24.uz\\', \\'185.196.215.231\\']'); open(path,'w').write(content)\"")

    # 2. Update Nginx configuration for ishtop24.uz and admin.ishtop24.uz
    nginx_conf = """server {
    listen 80;
    listen [::]:80;
    server_name ishtop24.uz www.ishtop24.uz admin.ishtop24.uz api.ishtop24.uz 185.196.215.231 _;

    client_max_body_size 50M;

    location /static/ {
        alias /root/24-7-hizmat/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /root/24-7-hizmat/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    run(f"cat << 'EOF' > /etc/nginx/sites-available/default\n{nginx_conf}\nEOF")
    run("nginx -t")
    run("systemctl restart nginx")
    run("systemctl restart 24-7-web")

    # 3. Install certbot for SSL
    run("DEBIAN_FRONTEND=noninteractive apt-get install -y certbot python3-certbot-nginx || DEBIAN_FRONTEND=noninteractive apt-get install -y certbot")

    client.close()

if __name__ == '__main__':
    configure_domain()
