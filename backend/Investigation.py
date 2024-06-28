# This is the active python object that will persist data for the session.
# Until DB models completed data will only persist for the lifespan of this object

# NOTE: having experimented with other hugging face models, spacy library seems most applicable for this application
# from transformers import pipeline
import spacy
from spacy.matcher import Matcher


class Investigation:
    def __init__(self, model):
        self.model = model
        self.nlp = self.instantiate_nlp_model()
        self.patterns = self.create_example_patterns()
        self.process_documents = []
        self.matcher = Matcher(self.nlp.vocab)
        self.instantiate_example_match_patterns()
        
        self.entity_texts_and_labels = []
        #self.instantiate_match_patterns()

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

    def chunk_text(self, text, chunk_size=10):
        
        doc = self.create_doc_object(text)
        sentences = [sent.text for sent in doc.sents]
        print(len(sentences))
        chunks = []
        for index in range(0, len(sentences), chunk_size):
            chunk = ' '.join(sentences[index:index + chunk_size])
            chunks.append(chunk)

        print("there are", len(chunks), "chunks")
        return chunks

    def create_doc_object(self, text):
        doc = self.nlp(text)
        self.process_documents.append(doc)
        print(f"Created doc object {doc}")
        
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
