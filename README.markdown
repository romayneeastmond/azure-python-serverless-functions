# Azure Python Serverless Functions

A collection of Azure servless endpoints, written in Python, used in conjunction with an [Azure OpenAI chat completion instance](https://github.com/romayneeastmond/azure-openai-angular).

## Functions

| Name                         | Description                                                                                                                                                                                                                                                                                  |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GetContentFromUrls           | Parses any valid website URL from the given prompt and returns scraped content. First attempts to locate the body tag and removes header, footer, and nav content. If no body is located, returns the entire webpage content.                                                                |
| GetDocumentFromContent       | Accepts plain content and returns the byte array of a text file.                                                                                                                                                                                                                             |
| GetFilesContents             | Accepts files in PDF, Word, text, and markdown format. Returns the document name, file type, content, word count, and pages count (only for PDFs).                                                                                                                                           |
| GetResultsFromContent        | Performs a vectorized search using cosine similarity on the distance between the given prompt and the given content. Used as a way of locating semantic meaning, usually from a scraped website or content of a document. Only results higher than 0 are returned.                           |
| GetResultsFromContentClauses | Performs a vectorized search using cosine similarity on the distance between a list of clauses (separated each on a new line) and the given content. Used as a way of locating if clauses are contained in content. Only results higher than 0 and greater than 55% similarity are returned. |
| GetWordFromHtml              | Accepts HTML content and returns the byte array of a Word Document.                                                                                                                                                                                                                          |


## Debugging Locally

To debug locally install [Azure Functions Core](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local) and press F5 within Visual Studio Code to run the functions against http://localhost:7071

## Copyright and Ownership

All terms used are copyright to their original authors.
