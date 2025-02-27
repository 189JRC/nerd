# This is the active python object that will persist data for the session.
# Until DB models completed data will only persist for the lifespan of this object



#TODO 
# add filter rules to make highlight/ manage entities returned
# Put together demo material
# Consider the summary feature and pipe it in
# Sort details from entities


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
        #self.add_custom_attributes()

        self.patterns = self.create_example_patterns()
        self.processed_documents = self.preprocess_example_documents()
        self.matcher = Matcher(self.nlp.vocab)
        self.instantiate_example_match_patterns()
        
        self.entity_texts_and_labels = []
        #self.instantiate_match_patterns()

    # def add_custom_attributes(self):
    #     # Adding custom extension attributes to the Doc class
    #     if not Doc.has_extension("metadata"):
    #         Doc.set_extension("metadata", default={})

    def create_document_summary(self, doc, parser, summariser):
        #find number of sentences
        summary = summariser(parser.document, sentences_count=1) 
        summary_text = ' '.join(str(sentence) for sentence in summary)
        return summary_text

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

        doc1.set_extension('origin', default=None, force=True)
        doc2.set_extension('origin', default=None, force=True)

        doc1._.origin = "Sample text 1"
        doc2._.origin = "Sample text 2"
        return [doc1, doc2]

    def create_example_patterns(self):
        # TODO:3: store these patterns (with user defined patterns) in a db table for retrieval.
        # pattern will flag the string such as 'a teenager was reported missing'
        example_pattern1 = [
            {"LIKE_NUM": True},
            {"LOWER": "men"}
        ]
        # pattern2 will flag the string 'Spanish Island'
        example_pattern2 = [
            {"LOWER": "airbnb"},
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
        return matched_segments

    def instantiate_nlp_model(self):
        if self.model == "spacy_en_sm":
            nlp = spacy.load("en_core_web_sm")
            # tfbert_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
            return nlp

    def chunk_text(self, doc, text_type, chunk_size=10):
        """Takes a text that is a list of sentences and formats them into a list of chunks of specified size."""
        #NOTE: Youtube transcripts do not come with punctuation - therefore parsing sentences for chunks will require different technique
        #For now just return full text
        #doc = self.create_doc_object(text)

        if text_type == 'article' or text_type == 'transcript':
            sentences = [sent.text for sent in doc.sents]
            print(f"{len(sentences)} sentences found in text")
            chunks = []
            for index in range(0, len(sentences), chunk_size):
                chunk = ' '.join(sentences[index:index + chunk_size])
                chunks.append(chunk)
            print("created", len(chunks), "chunks from the document")
        else:
            print("Problem in chunk_text() method. Cannot determine text_type")
        return chunks

    def apply_metadata_to_doc(self, doc, metadata_label, metadata_value):
        """Applies metadata to a document. Currently the only metadata is 'origin' set to the origin url"""
        doc.set_extension('origin', default=None, force=True)
        doc._.origin = metadata_value 
        return doc

    def create_doc_object(self, text, metadata_label=False, metadata_value=False):
        """Creates a doc object from a sample of text and adds it to the investigation's processed texts.
        Returns the document object with a metadata dict."""
        # Metadata could be used to integrate investigation docs into model training data
        # currently only a document label is stored
        doc = self.nlp(text)

        if metadata_label and metadata_value:
            doc = self.apply_metadata_to_doc(doc, metadata_label, metadata_value)
            self.processed_documents.append(doc)
            print(f"added doc {metadata_label}:{metadata_value}... to processed documents in investigation.")
        else:
            self.processed_documents.append(doc)
            print(f"Doc {doc.text[:10]} created with no metadata")

        return doc

    def find_entities(self, doc, relevant_entities=None):

       
        # all pretrained entity types and descriptions: https://github.com/explosion/spaCy/discussions/9147
        if relevant_entities == None:
            relevant_entities = [
                "PERSON",
                #"NORP", #e.g. british, spanish
                "FAC", #facilities
                "GPE", #geopolitical entities e.g. states
                "LOC",
                #"EVENT",
                #"DATE",
                #"TIME",
                #"MONEY",
            ]
        
        for ent in doc.ents:
            entity = (ent.text, ent.label_)
            if ent.label_ in relevant_entities:
                if { "name": ent.text, "label": ent.label_} not in self.entity_texts_and_labels:
                    self.entity_texts_and_labels.append(
                        {"name": ent.text, "label": ent.label_}
                    )
        return self.entity_texts_and_labels

    def investigate_vector_similarity(self, string_for_vector_comparison, window_size=10):
        # Process the search string to get its vector
        #TODO:3: include timing function to check measure whether this feature can scale
        #working assumption is that it can, although will need some tinkering to optimise
        #Currently it is performant on a couple of docs, but could be significantly slow when handling a dozen or a hundred
        #Also would be good to do comparisons between en_core_web_lg and en_core_web_md models

        
        #make a vector representation of the user inputted search string
        #set variables for vector analysis comparison
        search_doc = self.nlp(string_for_vector_comparison)
        search_vector = search_doc.vector
        most_similar_sentence = None
        highest_similarity = -1
        best_doc = None
        top_most_similar = []
        # after receiving duplicates on front end, this is a stop gap 
        # to prevent duplicates
        similarity_filter_list = []

        for doc in self.processed_documents:
            if doc._.origin:
                print(doc._.origin)
            else:
                print("DOC HAS NO METADATA")
            
            for sentence in doc.sents:
                if sentence.has_vector:
                    similarity = self.calculate_similarity(sentence.vector, search_vector)
                    
                    #this is probably not necessary anymore
                    #now only using top most similar on front end
                    #left here to avoid unnecessary damage
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        most_similar_sentence = sentence.text
                        best_doc = doc
                    
                    #append to top_most_similar if similarity is above a threshold (really not very scientific!)
                    if similarity > 0.2:
                        if similarity not in similarity_filter_list:
                            similarity_filter_list.append(similarity)
                            top_most_similar.append({"doc": doc.text, "doc_metadata": doc._.origin, "sentence": sentence.text, "similarity": float(similarity)})
                
        top_most_similar.sort(key=lambda similarity_value: similarity_value['similarity'], reverse=True)
        # return the top 10 only
        top_most_similar = top_most_similar[:11]
        
        #perhaps would be better to just return top_most_popular as a sorted list. it should have best_doc in it already.
        #for now keep best_doc in there (the no span is found with cosine sim > the value set for entry into the top_most_similar list)
        #then the result of this function would be nada
        return best_doc, dict(most_similar_span=most_similar_sentence, highest_similarity=float(highest_similarity), top_most_similar=top_most_similar)

    def calculate_similarity(self, vector1, vector2):
        cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        return cosine_similarity