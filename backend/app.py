from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import numpy as np
import requests
from bs4 import BeautifulSoup
from Investigation import Investigation
from deepmultilingualpunctuation import PunctuationModel

app = Flask(__name__)

#CORS(app) # TODO:2: Restrict CORS only to frontend URL
CORS(app, resources={r"/*": {"origins": "*"}})

investigation = Investigation(model="spacy_en_sm")

punctuation_model = PunctuationModel()
# db connection
# TODO:2 make sample config.env. put this in it!
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://osint:osint@localhost:5432/osint"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



# TODO:3 make model schema in models.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

def punctuate_transcript(transcript):
    result = punctuation_model.restore_punctuation(transcript)
    return result

def fetch_article(url):
    """sends a get request to the url string provided as argument.
    processes response to filter out the html and returns the article text content"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # will return HTTPError obj if req not successful

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
        return f"Error occurred in fetch_article()"


@app.route("/triage_request", methods=["POST"])
def triage_request():
    
    try:
        data = request.json
        url = data.get("url")
        type_of_scrape = data.get("type_of_scrape")
    except:
        pass
    
    if type_of_scrape == "youtube_transcript":
        # extract video id
        # standard url string format == https://www.youtube.com/watch?v=RIWfH3iEgXU
        _, video_id = url.split("watch?v=")
        # TODO:2: make all endpoint error handling uniform
        transcript_text = youtube_transcript_scraper(video_id)
        transcript_text = punctuate_transcript(transcript_text)
        print(transcript_text)
        chunked_text = investigation.chunk_text(transcript_text, text_origin="transcript")
        print(type(chunked_text))

    elif type_of_scrape == "article":
        full_text = fetch_article(url)
        # TODO:3: maybe return article in paragraph banches here. could also be a job for js object in frontend
        chunked_text = investigation.chunk_text(full_text, text_origin="article")
        print(type(chunked_text))

    elif type_of_scrape == "vector_search":
        string_for_vector_comparison = data.get("string_for_vector_comparison")
        vector_similarity_dict = calculate_vector_similarity(string_for_vector_comparison)
        return jsonify(vector_similarity_dict)

    elif type_of_scrape == "twitter":
        return jsonify({"article_text": "UNDER CONSTRUCTION"})

    else:
        print("no target for scrape specified.")
        return jsonify({"article_text": "UNDER CONSTRUCTION"})

    return jsonify({"article_text": chunked_text})


@app.route("/process", methods=["POST"])
def process_text():
    """Uses spaCy pipeline to get named entities from a piece of text.
    Returns a dict of ner strings that were found in text and their respective labels"""

    data = request.json
    text = data.get("text")
    entity_text_and_label_dicts = investigation.process_text(text)
    return entity_text_and_label_dicts

    


from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

@app.route("/scrape_youtube_transcript", methods=["POST"])
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

@app.route("/get_document_records", methods=['GET'])
def get_document_record():
    """Returns all processed documents (spaCy Doc objects) from the investigation"""
    doc_objects = investigation.processed_documents
    doc_object_metadata = []
    for doc_object in doc_objects:
        doc_object_metadata.append(doc_object._.metadata)

    return jsonify(doc_object_metadata)

# @app.route("/vector_similarity", methods=["POST"])
def calculate_vector_similarity(string_for_vector_comparison):

    best_doc, vector_similarity_data = investigation.investigate_vector_similarity(string_for_vector_comparison=string_for_vector_comparison)
    most_similar_span = vector_similarity_data['most_similar_span']
    highest_similarity = str(float(vector_similarity_data['highest_similarity'])) #can not serialise from float 32> therefore turned into int
    best_doc_text = best_doc.text
    best_doc_metadata = best_doc._.metadata
    top_most_similar = vector_similarity_data['top_most_similar']
    

    return_dict = dict(
    most_similar_span=most_similar_span,
    highest_similarity=highest_similarity,
    best_doc_metadata=best_doc_metadata,
    best_doc_text=best_doc_text,
    top_most_similar=top_most_similar)

    return return_dict

# Following functions are boilerplate for db CRUD
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


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(host="0.0.0.0", port=5000)
