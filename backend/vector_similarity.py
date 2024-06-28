import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_lg")
import numpy as np 
# Example documents
doc_texts = [
    "The 19-year-old from Lancashire went missing after a music festival in Tenerife Jay Slater’s.",
    "He was from Lancashire and wasn't seen after attending the NRG music festival in Tenerife.",
    "Jay Slater’s father has said he is in a “living hell” as the search for the missing teenager enters its second week."
]

# Create spaCy doc objects
docs = [nlp(text) for text in doc_texts]

# String to search for in the documents
search_string = "he went to a festival"

# Process the search string to get its vector
search_doc = nlp(search_string)
search_vector = search_doc.vector

# Initialize variables to store the most similar span and its similarity score
most_similar_span = None
top_most_similar = []
highest_similarity = -1
best_doc = None

# Function to calculate similarity between vectors
def calculate_similarity(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

window_size = 100
# Iterate over each document
top_most_similar = []
for doc in docs:
    doc_text = doc.text
    # Iterate over possible spans in the current document
    for start_char in range(len(doc_text) - window_size + 1):
        end_char = start_char + window_size
        span_text = doc_text[start_char:end_char]

        # Find the span in the doc that corresponds to this text
        span = doc.char_span(start_char, end_char)
        
        if span is not None and span.has_vector:
            similarity = calculate_similarity(span.vector, search_vector)
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_span = span
                best_doc = doc
            if similarity > 0.5:
                # highest_similarity = similarity
                most_similar_span = span
                top_most_similar.append({"doc":doc, "span": span, "similarity":similarity})

print(f"Most similar span in the document base: {most_similar_span.text}")
print(f"Similarity score: {highest_similarity}")
print(f"Found in document: {best_doc.text}")
print("MOST SIMILAR > .5", top_most_similar)
