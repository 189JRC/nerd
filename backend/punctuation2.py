import spacy

# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

def add_punctuation(text):
    doc = nlp(text)
    punctuated_tokens = []
    
    for i, token in enumerate(doc):
        punctuated_tokens.append(token.text)
        
        if i < len(doc) - 1:
            next_token = doc[i + 1]
            
            # Add punctuation based on POS tags
            if next_token.pos_ in ['NOUN', 'PROPN', 'VERB']:
                punctuated_tokens.append('.')
            elif next_token.pos_ == 'ADP':  # Example rule: sentences shouldn't end in a preposition
                punctuated_tokens.append('.')
            else:
                punctuated_tokens.append(' ')
    
    return ''.join(punctuated_tokens)

# Example text (transcript snippet)
text = """
dozens of firefighters police and Mountain Rangers have joined what authorities had hoped would be a massive sech on tener for missing British teenager Jay Slater fewer than a dozen members of the public responded to an appeal for experienced volunteers to come and help the 19-year-old was last seen on the 17th of June in a national park on a remote part of the Spanish Island police say today's search would go over much of the same ground as previous searches but that it would be more intensive and detailed making extra use of extra Personnel let's speak to our correspondent Nick Garnet who is on tenar Reef hello to you Nick um just tell us how things are there and what's going on the search started uh earlier on today and involves around 25 to 30 fire officers uh police civil protection officers and around half a dozen members of the public the call had gone out at yesterday asking for people who had Mountain experience or were experienced Walkers to come and offer their support only half a dozen did come uh one of them was a British tick tocker one was a private detective and there were a couple of a couple who live on the island who wanted to offer their help and support they say that they are doing what they can had had seen the news that Jay had disappeared and they wanted to help as much as they possibly could they

"""

# Add punctuation using SpaCy and custom rules
processed_text = add_punctuation(text)

print(processed_text)