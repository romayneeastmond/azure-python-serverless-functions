import logging
import azure.functions as func
import json
import time
from get_content_from_urls import find_urls
from get_content_from_urls import get_body_content
from get_content_from_urls import get_webpage_content

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')

    if not query:
        return func.HttpResponse(
            body=json.dumps({}),
            status_code=204,
            mimetype="application/json"
        )

    contents = []

    all_urls = find_urls(query)

    for url in all_urls:
        content = get_webpage_content(url)

        if content:
            body_content = get_body_content(content)

            if body_content is None:
                body_content = ""
            
            contents.append({
                "url": url,
                "content": body_content,
                "statistics": {
                    "words": len(body_content.split()),
                    "pages": -1
                }
            })
        else:
            logging.error(f"Failed to download content from {url}")

    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time

    logging.info(f"Prompt: {query}")
    logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

    return func.HttpResponse(
        body=json.dumps(contents),
        status_code=200,
        mimetype="application/json"
    )
