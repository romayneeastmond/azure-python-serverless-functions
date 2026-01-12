import logging
import azure.functions as func
import json
import time
from get_translation_from_content import call_llm

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info("Python HTTP trigger function processed a request.")
    
    try:
        body = req.get_json()
        prompt = body.get("prompt")
        files = body.get("files", [])

        if not prompt or not files:
            return func.HttpResponse(
                json.dumps({"error": "Prompt and files are required"}),
                status_code=400,
                mimetype="application/json"
            )

        results = []

        for file in files:
            file_name = file.get("fileName")
            content = file.get("content")

            if not file_name or not content:
                continue

            translated_text = call_llm(prompt, content)

            results.append({
                "fileName": file_name,
                "translation": translated_text
            })
                   
        stop_time = time.perf_counter()
        elapsed_time = stop_time - start_time

        logging.info(f"Script execution time: {elapsed_time:.4f} seconds")  

        return func.HttpResponse(
            body=json.dumps({"translations": results}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing files: {e}")


        