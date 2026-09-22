import paramiko

def delete_obsolete_orders_on_vps():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
    python_script = (
        "import django, os; "
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); "
        "django.setup(); "
        "from orders.models import Order; "
        "cnt, _ = Order.objects.filter(id__in=[2, 3]).delete(); "
        "print('Deleted count:', cnt); "
        "print('Remaining orders:', list(Order.objects.values_list('id', flat=True)))"
    )
    cmd = f'''/usr/local/python3.10/bin/python3.10 -c "{python_script}"'''
    stdin, stdout, stderr = client.exec_command(f"cd /root/24-7-hizmat/backend && {cmd}")
    print("OUTPUT:", stdout.read().decode('ascii', errors='ignore'))
    print("ERROR:", stderr.read().decode('ascii', errors='ignore'))
    client.close()

if __name__ == '__main__':
    delete_obsolete_orders_on_vps()
