import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_text_with_overlap(text, chunk_size, overlap):
  chunks = []
  
  for start in range(0, len(text), chunk_size - overlap):
    end = min(start + chunk_size, len(text))
    chunks.append(text[start - overlap: end])

  return chunks

def find_and_substring(text):
  uppercase_index = next((i for i, char in enumerate(text) if char.isupper()), None)

  if uppercase_index is not None:
    text = text[uppercase_index:].strip()
  else:
    text = text.strip()

  last_period_index = text.rfind('.')

  if last_period_index != -1:
    return text[:last_period_index + 1]
  else:
    return text

def get_search_results(top_indices, similarities, chunks):
    results = [(similarities[index], chunks[i]) for index, i in enumerate(top_indices)]

    return results
  
def search(query, vectors, features, chunks, number_of_results=3):
    top_indices, similarities = search_vectorized_data(query, vectors, features, number_of_results)

    results = get_search_results(top_indices, similarities, chunks)

    return results
  
def search_vectorized_data(query, vectors, features, number_of_results=3):
    vectorizer = TfidfVectorizer(vocabulary=features)

    query_vector = vectorizer.fit_transform([query]).toarray()

    similarities = cosine_similarity(query_vector, vectors)
    top_indices = np.argsort(similarities[0], kind = "stable")[::-1][:number_of_results]

    return top_indices, similarities[0][top_indices]

def vectorize_text(text, chunk_size=1000, overlap=50):
    vectors, features, chunks = vectorize_chunks(text, chunk_size, overlap)

    return vectors, features, chunks

def vectorize_chunks(text, chunk_size, overlap=50):
    vectorizer = TfidfVectorizer()

    chunks = chunk_text_with_overlap(text, chunk_size, overlap)
    
    vectors = vectorizer.fit_transform(chunks).toarray()
    features = vectorizer.get_feature_names_out()

    return vectors, features, chunks