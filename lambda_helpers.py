import json
import base64

def get_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS, GET', 
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
            }
    
def handle_options(event):
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",  # Allow any origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # Allow all common methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization,",  # Allow any header
                "Access-Control-Max-Age": '10'  # Cache pre-flight response for 10 secs
            },
            'body': ''  # OPTIONS requests don't typically need a body
        }

# Updating the get_event function to handle multipart data
def get_event(event):
    print(event)

    if 'body' in event:
        if not event['body']:
            raise KeyError('No Params Passed in')

        body = event['body']

        if event.get('isBase64Encoded', True):
            body = base64.b64decode(body).decode('utf-8')
        else:
            return json.loads(body)
            
def find_method(event):
    method = event.get('httpMethod', False)
    if not(method): 
        try:
            method = event['requestContext']['http']['method']  
        except Exception as e: 
            return 'POST'
    return method.upper()
    

