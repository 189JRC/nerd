from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import numpy as np
import requests
from bs4 import BeautifulSoup

# NOTE: having experimented with other hugging face models, spacy library seems most applicable for this application
# from transformers import pipeline
import spacy
from spacy.matcher import Matcher

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")
# tfbert_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)

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


# TODO:3 add tests for articles from different sources.
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
        # TODO:3: maybe return article in paragraph banches here. could be a job for js object in frontend
        return full_text

    except:
        return f"Error occurred in fetch_article()"


@app.route("/scrape", methods=["POST"])
def scrape():
    
    try:
        data = request.json
        url = data.get("url")
        type_of_scrape = data.get("type_of_scrape")
    except:
        pass
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if type_of_scrape == "youtube_transcript":
        # extract video id
        # standard url string format == https://www.youtube.com/watch?v=RIWfH3iEgXU
        _, video_id = url.split("watch?v=")
        # TODO:2: make all endpoint error handling uniform
        article_text = youtube_transcript_scraper(video_id)

    elif type_of_scrape == "article":
        article_text = fetch_article(url)

    elif type_of_scrape == "twitter":
        return jsonify({"article_text": "UNDER CONSTRUCTION"})
        
    else:
        print("no target for scrape specified.")
        return jsonify({"article_text": "UNDER CONSTRUCTION"})

    return jsonify({"article_text": article_text})


relevant_entities = ["GPE", "PERSON", "DATE"]


@app.route("/process", methods=["POST"])
def process_text():
    """Uses spaCy pipeline to get named entities from a piece of text.
    Returns a dict of ner strings that were found in text and their respective labels"""

    # all pretrained entity types and descriptions: https://github.com/explosion/spaCy/discussions/9147
    relevant_entities = [
        "PERSON",
        "NORP",
        "FAC",
        "GPE",
        "LOC",
        "EVENT",
        "DATE",
        "TIME",
        "MONEY",
    ]
    data = request.json
    text = data.get("text", "")
    model = data.get("model", "")

    doc = nlp(text)

    # custom defined pattern will match a text string 

    # TODO:3: Make this matcher block a seperate function and store these patterns (with user defined patterns) in a db table for retrieval. 
    # This pattern will flag the string 'a teenager was reported missing'
    pattern = [
        {"POS": "DET", "OP": "?"},  
        {"POS": "NOUN", "OP": "?"},  
        {"LEMMA": "be"},  
        {"POS": "VERB"},  
        {"POS": "VERB"},  
    ]
    # This pattern will flag the string 'Spanish Island'
    pattern2 = [
        {"ENT_TYPE": "NORP"},  
        {"LOWER": "island"},  
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("INDICATOR", [pattern])
    # matcher.add("NORP_LOC", [pattern2])
    matches = matcher(doc)

    # Matched segments are the sequences in the process text that are flagged as matching the defined patterns
    matched_segments = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_segments.append({"name": span.text, "label": "INDICATOR"})

    entity_text_and_label_dicts = []
    for segment in matched_segments:
        entity_text_and_label_dicts.append(segment)

    ###########
    if model == "spacy":

        for ent in doc.ents:
            entity = (ent.text, ent.label_)
            if ent.label_ in relevant_entities:
                if {
                    "name": ent.text,
                    "label": ent.label_,
                } not in entity_text_and_label_dicts:
                    entity_text_and_label_dicts.append(
                        {"name": ent.text, "label": ent.label_}
                    )

    return jsonify(entity_text_and_label_dicts) 

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
