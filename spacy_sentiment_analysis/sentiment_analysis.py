import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("spacytextblob")


statement = "whats up doc. im dying"


doc = nlp(statement)
print(doc._.polarity)

# Check the polarity of the statement
if doc._.polarity > 0:
    print("The statement is positive")
elif doc._.polarity < 0:
    print("The statement is negative")
else:
    print("The statement is neutral")

