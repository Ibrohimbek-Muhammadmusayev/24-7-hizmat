import paramiko

def test_domains():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
    # 1. Test main domain
    _, stdout, _ = client.exec_command("curl -s -H 'Host: ishtop24.uz' http://127.0.0.1/")
    landing_html = stdout.read().decode('ascii', errors='ignore')
    print("1. ishtop24.uz ->", "24/7-ishlar" in landing_html and "hero-title" in landing_html)

    # 2. Test admin subdomain
    _, stdout, _ = client.exec_command("curl -s -H 'Host: admin.ishtop24.uz' http://127.0.0.1/")
    admin_html = stdout.read().decode('ascii', errors='ignore')
    print("2. admin.ishtop24.uz ->", "id=\"root\"" in admin_html and "index-DmHZ7Uj4.js" in admin_html)

    client.close()

if __name__ == '__main__':
    test_domains()
