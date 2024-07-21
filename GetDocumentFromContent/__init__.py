import logging
import azure.functions as func
import json
import time
from get_content_document_from_text import generate_content_document

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    
    content = req_body.get('content')
    
    if not content or not content:
        return func.HttpResponse(
            body=json.dumps({}),
            status_code=204,
            mimetype="application/json"
        )
        
    content_document_bytes = generate_content_document(content)   
    
    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time
    
    logging.info(f"Content: {content}")
    logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

    return func.HttpResponse(
        body=content_document_bytes,
        status_code=200,
        mimetype="application/json"
    )
