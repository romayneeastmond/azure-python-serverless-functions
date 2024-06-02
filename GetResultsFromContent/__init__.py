import logging
import azure.functions as func
import json
import time
from get_results_from_content import find_and_substring
from get_results_from_content import search
from get_results_from_content import vectorize_text

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    query = req_body.get('query')
    content = req_body.get('content')

    if not query or not content:
        return func.HttpResponse(
            body=json.dumps({}),
            status_code=204,
            mimetype="application/json"
        )

    vectors, features, chunks = vectorize_text(content, 1000, 100)
    results = search(query, vectors, features, chunks, 5)

    contents = []

    for i, (similarity, result) in enumerate(results):
        result = result.replace("\n", " ").replace("   ", " ").replace("  ", " ")
        result = find_and_substring(result)
        
        if similarity != 0.0:
            contents.append({
                "content": result,
                "similarity": f"{similarity:.4f}"
            })

    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time
    
    logging.info(f"Prompt: {query}")
    logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

    return func.HttpResponse(
        body=json.dumps(contents),
        status_code=200,
        mimetype="application/json"
    )