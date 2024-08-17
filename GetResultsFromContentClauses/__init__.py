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

    content = req_body.get('content')
    clauses = req_body.get('clauses')
    temperature = req_body.get('similarity')

    if not content or not clauses:
        return func.HttpResponse(
            body=json.dumps({}),
            status_code=204,
            mimetype="application/json"
        )
        
    if not temperature:
        temperature = 0.25
    
    vectors, features, chunks = vectorize_text(content, 1000, 100)
    
    individual_clauses = clauses.split("\n")
    
    contents = []
    
    for i, (clause) in enumerate(individual_clauses):
        search_result = search(clause, vectors, features, chunks, 1)
        
        similarity = search_result[0][0]
        result = search_result[0][1]
        
        result = result.replace("   ", " ").replace("  ", " ")
        result = find_and_substring(result)
        
        if similarity != 0.0 and similarity > temperature:
            contents.append({
                "clause": clause,
                "similarity": f"{similarity:.4f}"
            })        
    
    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time
    
    logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

    return func.HttpResponse(
        body=json.dumps(contents),
        status_code=200,
        mimetype="application/json"
    )