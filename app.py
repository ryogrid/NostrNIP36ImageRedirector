from flask import Flask, request, redirect
import re

app = Flask(__name__)

SUPPORTING_WEB_CLIENTS = [
    "syusui-s.github.io",
    "snort.social",
    "nostter.vercel.app",
    "astraea.mousedev.page",
    "stok33.github.io/NostrIllustStock/",
]

SUPPORTING_NATIVE_CLIENTS = [
    "okhttp/5.0.0-alpha.11", # Amethyst
    "Dart/3.0 (dart:io)", # Plebstr
]

MAX_STORE_IP_NUM = 1000
REMOVE_IP_NUM = 100

accessed_ip_list = []
accessed_ip_dict = {}

def is_supporting_client(uagent, referer, ip_addr):
    try:
        # for case that web client open image file URL in new tab or window
        # Damus is not NIP-36 supporting
        if uagent.find("damus") == -1 \
            and ip_addr != None \
            and accessed_ip_dict[ip_addr] == True:
                return True
    except:
        pass

    # native clients
    for client_url in SUPPORTING_NATIVE_CLIENTS:
        if uagent.find(client_url) != -1:
            return True
        
    # web clients
    for client_url in SUPPORTING_WEB_CLIENTS:
        if referer != None and referer.find(client_url) != -1:
            return True

    return False

def check_path(path):
    pattern = r'^[a-zA-Z0-9/\.]*$'
    if re.match(pattern, path):
        return True
    else:
        return False

@app.route('/<path:path>')
def root_path(path):
    global accessed_ip_list
    global accessed_ip_dict

    uagent = request.headers.get('User-Agent')
    if not is_supporting_client(uagent, request.referrer, request.remote_addr):
        return redirect("https://ryogrid.net/dist/nip36-needed.jpg")
    
    if not check_path(path):
        return "", 400

    # store accessed IP address    
    accessed_ip_list.append(request.remote_addr)
    accessed_ip_dict[request.remote_addr] = True
    # remove old memoried IP addresses
    if len(accessed_ip_list) > MAX_STORE_IP_NUM:
        for idx in range(0, REMOVE_IP_NUM):
            del accessed_ip_dict[accessed_ip_list[idx]]
        accessed_ip_list = accessed_ip_dict[REMOVE_IP_NUM:]

    return redirect("https://cdn.nostr.build/" + path)
