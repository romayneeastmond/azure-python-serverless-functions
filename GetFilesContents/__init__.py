import logging
import azure.functions as func
import json
import time
from get_file_contents import get_file_content
from get_file_contents import get_file_extension

def main(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.perf_counter()
    logging.info("Python HTTP trigger function processed a request.")

    try:
        file_details = []
        files = req.files.values()

        logging.info(req.files)

        for file in files:
            start_time_file = time.perf_counter()            

            file_type = get_file_extension(file.filename)
            content, number_of_words, number_of_pages, pages_content = get_file_content(file, file_type)

            file_details.append({
                "filename": file.filename, 
                "extension": file_type, 
                "content": content,
                "statistics": {
                    "words": number_of_words,
                    "pages": number_of_pages
                },
                "pages": pages_content
            })

            stop_time_file = time.perf_counter()
            elapsed_time_file = stop_time_file - start_time_file

            logging.info(f"Completed {file.filename} in time: {elapsed_time_file:.4f} seconds")

        stop_time = time.perf_counter()
        elapsed_time = stop_time - start_time

        logging.info(f"Script execution time: {elapsed_time:.4f} seconds")

        return func.HttpResponse(
            body=json.dumps(file_details),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing files: {e}")

