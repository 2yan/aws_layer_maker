import json
import base64
from urllib.parse import parse_qs

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


def get_body(event):
    if event.get('isBase64Encoded', False):
        data = base64.b64decode(event['body']).decode('utf-8')
        body = parse_qs(data)
        
    else:
        body = event.get('body', False)
        if body:
            try:
                body= json.loads(body)
            except json.JSONDecodeError:
                body = parse_qs(body)
        else:

            body = event.get('queryStringParameters', {'status': 'NO DATA SUBMITTED'} )
    return body
    
def find_method(event):
    method = event.get('httpMethod', False)
    if not(method): 
        try:
            method = event['requestContext']['http']['method']  
        except Exception as e: 
            return 'POST'
    return method.upper()
    

