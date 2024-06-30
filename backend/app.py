from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import numpy as np
import requests
from bs4 import BeautifulSoup

from Investigation import Investigation

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from deepmultilingualpunctuation import PunctuationModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


app = Flask(__name__)

#CORS(app) # TODO:2: Restrict CORS only to frontend URL
CORS(app, resources={r"/*": {"origins": "*"}})

# there are three different neural net models used currently
# general purpose nlp is spacy, punctuation (for transcripts), and text summariser
investigation = Investigation(model="spacy_en_sm")
punctuation_model = PunctuationModel()
summariser = LsaSummarizer()
parser = PlaintextParser.from_string(text, Tokenizer('english'))

def punctuate_transcript(transcript):
    result = punctuation_model.restore_punctuation(transcript)
    return result

def fetch_article(url):
    """sends a get request to the url string provided as argument.
    processes response to filter out the html and returns the article text content"""
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(
            response.content, "html.parser"
        )  # parse html from response content
        article = soup.find(
            "article"
        )  # extract article text based on known HTML structure
        if not article:
            raise ValueError(f"No article was found at {url}")

        # gather and process article text for response to fe
        article_text = []
        for paragraph in article.find_all("p"):
            article_text.append(paragraph.get_text())

        full_text = "\n".join(article_text)
        return full_text

    except:
        return f"Error occurred in fetch_article() for {url}"

@app.route("/fetch_and_process_doc_data", methods=["POST"])
def fetch_and_process_doc_data():
    """ Receives a fetch request, triages it according to user intention, then triggers operations to process the text.
    Returns text chunks as a list of dicts with metadata"""
    try:
        data = request.json
        url = data.get("url")
        desired_action = data.get("desired_action")
    except:
        pass
    
    if desired_action == "youtube_transcript":
        # extract video id
        # standard url string format == https://www.youtube.com/watch?v=RIWfH3iEgXU
        _, video_id = url.split("watch?v=")
        # TODO:2: make all endpoint error handling uniform
        transcript_text = youtube_transcript_scraper(video_id)
        transcript_text = punctuate_transcript(transcript_text)
        doc = investigation.create_doc_object(transcript_text, metadata_label="origin", metadata_value=url)
        named_entities = investigation.find_entities(doc)
        matched_patterns = investigation.apply_matched_patterns(doc) 
        
        ## together these will give highlighted entities on the front end
        for pattern in matched_patterns:
            named_entities.append(pattern)
            
        text_chunks = investigation.chunk_text(doc, text_type="transcript")

        parser = PlaintextParser.from_string(doc.text, Tokenizer('english'))
        text_summary = investigation.create_document_summary(doc, parser, summariser)

    elif desired_action == "article":
        scraped_text = fetch_article(url)
        # TODO:3: maybe return article in paragraph banches here. could also be a job for js object in frontend
        doc = investigation.create_doc_object(scraped_text, metadata_label="origin", metadata_value=url)
        named_entities = investigation.find_entities(doc)
        matched_patterns = investigation.apply_matched_patterns(doc) 
        
        ## together these will give highlighted entities on the front end
        for pattern in matched_patterns:
            named_entities.append(pattern)
        
        text_chunks = investigation.chunk_text(doc, text_type="article")

        parser = PlaintextParser.from_string(doc.text, Tokenizer('english'))
        text_summary = investigation.create_document_summary(doc, parser, summariser)

    elif desired_action == "vector_search":
        string_for_vector_comparison = data.get("string_for_vector_comparison")
   

        best_doc, vector_similarity_data = investigation.investigate_vector_similarity(string_for_vector_comparison=string_for_vector_comparison)
        
        most_similar_span = vector_similarity_data['most_similar_span']
        highest_similarity = str(float(vector_similarity_data['highest_similarity'])) #can not serialise from float 32> therefore turned into int
        best_doc_text = best_doc.text
        best_doc_metadata = best_doc._.origin
        top_most_similar = vector_similarity_data['top_most_similar']
    

        return_dict = dict(
        #most_similar_span=most_similar_span,
        #highest_similarity=highest_similarity,
        #best_doc_metadata=best_doc_metadata,
        #best_doc_text=best_doc_text,
        top_most_similar=top_most_similar)

        return jsonify(return_dict)

    elif desired_action == "twitter":
        return jsonify({"article_text": "UNDER CONSTRUCTION"})

    else:
        print("no target for scrape specified.")
        return jsonify({"article_text": "UNDER CONSTRUCTION"})

    print(text_summary)
    return jsonify({"text_chunks": text_chunks, "named_entities": named_entities, "text_summary": text_summary})
    # return jsonify({"article_text": chunked_text, "named_entities": named_entities_dict})

@app.route("/get_document_records", methods=['GET'])
def get_document_record():
    """Returns all processed documents (spaCy Doc objects) from the investigation"""
    doc_objects = investigation.processed_documents
    doc_object_metadata = []
    for doc_object in doc_objects:
        doc_object_metadata.append(doc_object._.origin)

    return jsonify(doc_object_metadata)

    
def process_text_into_doc_object(doc, url_for_metadata_label):
    """Uses spaCy pipeline to get named entities from a piece of text.
    Returns a dict of ner strings that were found in text and their respective labels"""

    entity_text_and_label_dicts = investigation.process_text(text_to_process, url_for_metadata_label)
    return entity_text_and_label_dicts

def youtube_transcript_scraper(video_id):
    """Gets the transcript for the given video ID. returns as string
    test example: #https://www.youtube.com/watch?v=1zErA1Igtow. 
    NOTE: Not all youtube vids have transcripts!"""

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # format it into plain text
        formatter = TextFormatter()
        formatted_transcript_text = formatter.format_transcript(transcript)
        
        print(f"Transcript for video {video_id}:\n{formatted_transcript_text[0:10]}...\n")
        return formatted_transcript_text

    except Exception as error:
        print(f"Error retrieving transcript for video {video_id}: {error}")
        return None


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(host="0.0.0.0", port=5000)



# Following functions are boilerplate for CRUD when db is connected

# db connection
# TODO:2 make sample config.env. put this in it!
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://osint:osint@localhost:5432/osint"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

# # TODO:3 make model schema in models.py
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(100), nullable=False)

# @app.route("/")
# def index():
#     with app.app_context():
#         # Simple query to test the database connection
#         result = db.session.execute(text("SELECT 1")).fetchone()
#         return jsonify({"result": result[0]})


# @app.route("/add/<string:name>")
# def add_user(name):
#     new_user = User(name=name, password="password")
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"result": "User added"})


# @app.route("/users")
# def get_users():
#     users = User.query.all()
#     result = [{"id": user.id, "name": user.name} for user in users]
#     return jsonify(result)