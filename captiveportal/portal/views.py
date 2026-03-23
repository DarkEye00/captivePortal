from django.shortcuts import render

# Create your views here.
import subprocess
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from django.shortcuts import render
from django.http import HttpResponse

RADIUS_SERVER = '192.168.0.1'  # your RADIUS server IP
RADIUS_SECRET = b'testing123'  # must match your clients.conf

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        client_ip = request.POST.get('client_ip', '')

        if authenticate_radius(username, password):
            # Unlock the client IP via iptables
            unlock_client(client_ip)
            return render(request, 'portal/success.html', {
                'username': username
            })
        else:
            return render(request, 'portal/login.html', {
                'error': 'Invalid username or password',
                'client_ip': client_ip
            })

    # GET request - show login form
    client_ip = request.GET.get('client_ip', request.META.get('REMOTE_ADDR', ''))
    return render(request, 'portal/login.html', {'client_ip': client_ip})


def authenticate_radius(username, password):
    try:
        client = Client(
            server=RADIUS_SERVER,
            secret=RADIUS_SECRET,
            dict=Dictionary()
        )
        req = client.CreateAuthPacket(
            code=pyrad.packet.AccessRequest,
            User_Name=username,
        )
        req["User-Password"] = req.PwCrypt(password)
        req["NAS-IP-Address"] = "192.168.0.100"
        req["NAS-Port"] = 0

        reply = client.SendPacket(req)
        return reply.code == pyrad.packet.AccessAccept

    except Exception as e:
        print(f"RADIUS error: {e}")
        return False


def unlock_client(client_ip):
    if not client_ip:
        return
    try:
        subprocess.run([
            'sudo', 'iptables', '-I', 'FORWARD',
            '-s', client_ip,
            '-j', 'ACCEPT'
        ], check=True)
    except Exception as e:
        print(f"iptables error: {e}")