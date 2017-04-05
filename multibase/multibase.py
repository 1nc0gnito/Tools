import base64

def multib64decode(b64EncFile):
    message = base64.b64decode(b64EncFile)
    while True:
        try:
            message = base64.b64decode(message)
        except:
            break
    return message
