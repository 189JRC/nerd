# This is the active python object that will persist data for the session.
# Until DB models completed data will only persist for the lifespan of this object

# NOTE: having experimented with other hugging face models, spacy library seems most applicable for this application
# from transformers import pipeline
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
import numpy as np
import os
directory = os.path.dirname(__file__) 

class Investigation:
    def __init__(self, model):
        self.model = model
        
        self.nlp = self.instantiate_nlp_model()
        self.add_custom_attributes()

        self.patterns = self.create_example_patterns()
        self.processed_documents = self.preprocess_example_documents()
        self.matcher = Matcher(self.nlp.vocab)
        self.instantiate_example_match_patterns()
        
        self.entity_texts_and_labels = []
        #self.instantiate_match_patterns()

    def add_custom_attributes(self):
        # Adding custom extension attributes to the Doc class
        if not Doc.has_extension("metadata"):
            Doc.set_extension("metadata", default={})

    def preprocess_example_documents(self):
        # Read the contents of the text files
        file1_path = os.path.join(directory, 'sample_text_1.txt')
        file2_path = os.path.join(directory, 'sample_text_2.txt')

        with open(file1_path, 'r', encoding='utf-8') as file1:
            text1 = file1.read()
        
        with open(file2_path, 'r', encoding='utf-8') as file2:
            text2 = file2.read()

        # Process the texts into spaCy documents
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        doc1._.metadata = {"source": "sample_text_1.txt", "other_info": "Additional metadata here"}
        doc2._.metadata = {"source": "sample_text_2.txt", "other_info": "Additional metadata here"}

        return [doc1, doc2]

    def create_example_patterns(self):
        # TODO:3: store these patterns (with user defined patterns) in a db table for retrieval.
        # pattern will flag the string such as 'a teenager was reported missing'
        example_pattern1 = [
            {"POS": "DET", "OP": "?"},
            {"POS": "NOUN", "OP": "?"},
            {"LEMMA": "be"},
            {"POS": "VERB"},
            {"POS": "VERB"},
        ]
        # pattern2 will flag the string 'Spanish Island'
        example_pattern2 = [
            {"ENT_TYPE": "NORP"},
            {"LOWER": "island"},
        ]
        return {"example_pattern1":example_pattern1, "example_pattern2":example_pattern2}

    def instantiate_example_match_patterns(self):
        self.matcher.add("EXAMPLE_INDICATOR", [self.patterns["example_pattern1"]])
        self.matcher.add("NORP_LOC", [self.patterns["example_pattern2"]])
        #self.matcher.add("LANCASHIRE", [[{"LOWER":"lancashire"}]])
        return True

    def apply_matched_patterns(self, document_under_investigation):
        matches = self.matcher(document_under_investigation)

        # Matched segments are the sequences in the process text that are flagged as matching the defined patterns
        matched_segments = []
        for match_id, start, end in matches:
            span = document_under_investigation[start:end]
            matched_segments.append({"name": span.text, "label": "INDICATOR"})

        self.entity_text_and_label_dicts = []
        #TODO:1: this should be applied to document metadata with the set_extensions method
        for segment in matched_segments:
            self.entity_texts_and_labels.append(segment)

    def instantiate_nlp_model(self):
        if self.model == "spacy_en_sm":
            nlp = spacy.load("en_core_web_sm")
            # tfbert_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
            return nlp

    def chunk_text(self, text, text_origin, chunk_size=10):
        """Takes a text that is a list of sentences and formats them into a list of chunks of specified size."""
        #NOTE: Youtube transcripts do not come with punctuation - therefore parsing sentences for chunks will require different technique
        #For now just return full text
        doc = self.create_doc_object(text)

        if text_origin == 'article':
            sentences = [sent.text for sent in doc.sents]
            print(len(sentences))
            chunks = []
            for index in range(0, len(sentences), chunk_size):
                chunk = ' '.join(sentences[index:index + chunk_size])
                chunks.append(chunk)

            print("there are", len(chunks), "chunks")
        elif text_origin == 'transcript':
            chunks = [text]
        else:
            print("Problem in chunk_text() method. Cannot determine text_origin")
        return chunks

    def create_doc_object(self, text):
        doc = self.nlp(text)
        self.processed_documents.append(doc)
        print(f"Created doc object {doc}")
        print("Number of docs processed:", len(self.processed_documents))
        return doc 

    def process_text(self, virgin_text, relevant_entities=None):

        # process doc with nlp model
        document_under_investigation = self.nlp(virgin_text)
        # all pretrained entity types and descriptions: https://github.com/explosion/spaCy/discussions/9147
        if relevant_entities == None:
            relevant_entities = [
                "PERSON",
                # "NORP",
                # "FAC",
                # "GPE",
                # "LOC",
                # "EVENT",
                # "DATE",
                # "TIME",
                # "MONEY",
            ]
        
        self.apply_matched_patterns(document_under_investigation)

        for ent in document_under_investigation.ents:
            entity = (ent.text, ent.label_)
            if ent.label_ in relevant_entities:
                if { "name": ent.text, "label": ent.label_} not in self.entity_texts_and_labels:
                    self.entity_texts_and_labels.append(
                        {"name": ent.text, "label": ent.label_}
                    )
        return self.entity_texts_and_labels

    def investigate_vector_similarity(self, string_for_vector_comparison, window_size=100):
        # Process the search string to get its vector
        #TODO:3: include timing function to check measure compute times for feasibility
        #Perform comparisons between en_core_web_lg and _md
        search_doc = self.nlp(string_for_vector_comparison)

        #make a vector representation of the user inputted search string
        #set variables for vector analysis comparison
        search_vector = search_doc.vector
        most_similar_span = None
        highest_similarity = -1
        best_doc = None
        top_most_similar = []

        #loop through each spacy doc object
        for doc in self.processed_documents:
            doc_text = doc.text
            # iterate over spans in text document #NOTE: This needs more attention for optimising search
            # could be better to iterate over doc tokens
            for start_char in range(len(doc_text) - window_size + 1):
                end_char = start_char + window_size
                span_text = doc_text[start_char:end_char]

                # Find the span in the doc that corresponds to this text window
                span = doc.char_span(start_char, end_char)
                
                if span is not None and span.has_vector:
                    similarity = self.calculate_similarity(span.vector, search_vector)
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        most_similar_span = span
                        best_doc = doc
                    if float(similarity) > 0.5:
                        # highest_similarity = similarity
                        most_similar_span = span
                        top_most_similar.append({"doc":doc, "span": span, "similarity":similarity})
        #sort the top most similar according to their similarity
        #take the slice of the top 5 cosine sim scores
        #convered cosine sims to floats
        top_most_similar_with_floats = []
        for similar_result in top_most_similar:
            doc = similar_result['doc']
            span = similar_result['span']
            print(type(similar_result['similarity']))
            x = float(similar_result['similarity'])
            print(type(x))
            similarity = float(similar_result['similarity'])
            print(type(similarity))
            top_most_similar_with_floats.append({"doc":doc,"span":span})
        #It is trying to serialise an np array somehwwere
        return best_doc, dict(most_similar_span=most_similar_span.text, highest_similarity=float(highest_similarity), top_most_similar=top_most_similar_with_floats)

    def calculate_similarity(self, vector1, vector2):
        cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        return cosine_similarity