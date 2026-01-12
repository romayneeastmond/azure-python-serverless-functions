import logging
import azure.functions as func
import json
import time
from get_summarization_from_content import chunk_text
from get_summarization_from_content import summarize_chunk

MAX_CHARS_PER_CHUNK = 125000

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info("Python HTTP trigger function processed a request.")
    
    try:    
        body = req.get_json()
        files = body.get("files", [])

        documents = []
        doc_map = {}
        doc_id = 0

        for file in files:
            file_name = file.get("fileName")
            content = file.get("content", "")

            if not file_name or not content:
                continue

            chunks = chunk_text(content, MAX_CHARS_PER_CHUNK)

            for chunk in chunks:
                documents.append({
                    "id": str(doc_id),
                    "language": "en",
                    "text": chunk
                })
                doc_map[str(doc_id)] = file_name
                doc_id += 1

        if not documents:
            return func.HttpResponse(
                json.dumps({"error": "No valid files provided"}),
                status_code=400,
                mimetype="application/json"
            )

        summaries_by_file = {}

        for doc in documents:
            file_name = doc_map.get(doc["id"])

            if file_name not in summaries_by_file:
                summaries_by_file[file_name] = []

            summary_text = summarize_chunk(doc["text"])
            summaries_by_file[file_name].append(summary_text)

        response_payload = {
            "summaries": [
                {
                    "fileName": file_name,
                    "summary": " ".join(texts)
                }
                for file_name, texts in summaries_by_file.items()
            ]
        }
  
        stop_time = time.perf_counter()
        elapsed_time = stop_time - start_time

        logging.info(f"Script execution time: {elapsed_time:.4f} seconds")  

        return func.HttpResponse(
            body=json.dumps(response_payload),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing files: {e}")