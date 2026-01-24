import logging
import azure.functions as func
import json
import time
from get_powerpoint_document_from_html import generate_powerpoint_presentation

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    slides = req_body.get('slides')

    if not slides or not isinstance(slides, list):
        return func.HttpResponse(
            body=json.dumps({"error": "Please provide a 'slides' array containing HTML strings."}),
            status_code=400,
            mimetype="application/json"
        )
    
    pptx_bytes = generate_powerpoint_presentation(slides)

    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time
    
    logging.info(f"Processed {len(slides)} slides.")
    logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

    return func.HttpResponse(
        body=pptx_bytes,
        status_code=200,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
