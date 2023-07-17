from flask import Flask, request, redirect, make_response
import re

app = Flask(__name__)

SUPPORTING_WEB_CLIENTS = [
    "syusui-s.github.io",
    "snort.social",
    "nostter.vercel.app",
    "astraea.mousedev.page",    
]
def is_supporting_client(uagent, referer, cookies):
    try:
        # when a web client already permitted on the same browser
        if cookies.get('suppport36') == "true":
            return True
    except:
        pass

    if uagent.find("okhttp/5.0.0-alpha.11") != -1: # Amethyst
        # want to add Plebstar... but user agent is unknown...
        return True
    else: # web clients
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
    uagent = request.headers.get('User-Agent')
    if not is_supporting_client(uagent, request.referrer, request.cookies):
        return "", 403
    
    if not check_path(path):
        return "", 400
    
    response = make_response(redirect("https://nostr.build/" + path))
    response.set_cookie('suppport36', "true")
    return response
