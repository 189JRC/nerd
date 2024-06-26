# Early test suite for NERD app

from app import youtube_transcript_scraper 
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


if __name__ == "__main__":
    x = "https://www.youtube.com/watch?v=1zErA1Igtow"
    transcript = youtube_transcript_scraper("1zErA1Igtow")
    if type(transcript) == str and len(transcript) > 10:
        print("transcript returned successfully: {transcript[0:10]}")