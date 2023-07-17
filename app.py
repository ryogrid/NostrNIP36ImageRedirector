from flask import Flask, request, redirect
import re

app = Flask(__name__)

def is_supporting_client(uagent, referer):
    print(uagent)
    if uagent.find("okhttp/5.0.0-alpha.11") != -1: # Amethyst?
        return True
    else:
        return False

def check_path(path):
    pattern = r'^[a-zA-Z0-9/\.]*$'
    if re.match(pattern, path):
        return True
    else:
        return False

@app.route('/<path:path>')
def root_path(path):
    uagent = request.headers.get('User-Agent')
    if not is_supporting_client(uagent, request.referrer):
        return "", 403
    
    if not check_path(path):
        return "", 400
    
    return redirect("https://nostr.build/" + path)
