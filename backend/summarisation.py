from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Example text
text = """
dozens of firefighters, police and Mountain Rangers have joined what authorities had hoped would be a massive sech on tener for missing British teenager Jay Slater. fewer than a dozen members of the public responded to an appeal for experienced volunteers to come and help. the 19-year-old was last seen on the 17th of June in a national park on a remote part of the Spanish Island. police say today's search would go over much of the same ground as previous searches, but that it would be more intensive and detailed, making extra use of extra Personnel. let's speak to our correspondent, Nick Garnet, who is on tenar Reef. hello to you, Nick. um, just tell us how things are there and what's going on. the search started, uh, earlier on today and involves around 25 to 30 fire officers, uh police, civil protection officers and around half a dozen members of the public. the call had gone out at yesterday asking for people who had Mountain experience or were experienced Walkers to come and offer their support. only half a dozen did come. uh, one of them was a British tick tocker, one was a private detective and there were a couple of a couple who live on the island who wanted to offer their help and support. they say that they are doing what they can had had seen the news that Jay had disappeared and they wanted to help as much as they possibly could. they're searching the same areas that they have been searching in since he disappeared, 13 days ago now, and they've been in this Valley here right the way through the search and indeed today have been back in there. they say that they're going further and deeper than they've been able to before, and therefore it is searching new ground and making sure that the ground that they have searched is completely clear. at the moment, though, we still not heard that they have found any clues whatsoever as to how he disappeared. now the man who's leading the inquiry- it's a man called Sano Martin. he explained what the terrain is like. there are difficult areas, and we've given instructions for people not to risk their own safety, but there's something we need to make clear, which is that any area we don't go to well, Jay won't have gone there either. you have to think about it logically. if I see there's vegetation in front of me and I'm going to get spiked and I can't get through, then he won't have gone through that area either. we have to be logical. obviously, can you reach the sea directly from the area you were searching. you can reach the sea. in fact, last Saturday I went along the whole path. there are Old Paths which are only occasionally used because it's a cliff with very little attraction for sporting purposes, but you can reach the beach along them. so I reached the beach. uh, we didn't find anything. it's a path that goes above and not along the bottom of the cliff. it has drops and what's needed are ropes to get down, and we also know he was not equipped for that. how difficult are the difficult areas? there are rocky drops that you cannot get Beyond. you can only get down with a harness and ropes. the people searching that spot today will have to turn around, I think, because they don't have the necessary equipment, and, anyway, the best that Jay could do was simply to. so the search goes on and it will continue to go on, uh, in the same numbers, doing the same thing that they have done so far, hoping to get that final clue that will unlock what happened to jce Slater. okay, thank you very much for now. that's Nick garip for us there. live in tener.
"""
# Initialize parser and tokenizer
parser = PlaintextParser.from_string(text, Tokenizer('english'))

# Initialize LSA Summarizer
summarizer = LsaSummarizer()
summary = summarizer(parser.document, sentences_count=1)  # Adjust sentences_count as needed

# Print the summary
# for sentence in summary:
#     print(sentence)

# Accessing summary as a string
summary_text = ' '.join(str(sentence) for sentence in summary)
print("SUM==", summary_text)