import json


'''
CODE LIST

- is_detect
- processing_detect
- is_reid
- processing_reid
'''
def response_code(code, is_json=True):
    result = {
        'code': code
    }

    if is_json:
        return json.dumps(result)
    
    return result
