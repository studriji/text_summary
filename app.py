from flask import Flask, app,render_template,url_for,request
import re
import nltk
import heapq

contraction_mapping = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",

                           "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",

                           "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",

                           "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",

                           "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",

                           "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",

                           "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",

                           "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",

                           "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",

                           "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",

                           "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",

                           "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",

                           "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",

                           "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",

                           "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",

                           "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",

                           "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",

                           "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",

                           "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",

                           "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",

                           "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",

                           "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",

                           "you're": "you are", "you've": "you have"}


app=Flask(__name__)
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		article_text = request.form['message']
		# Removing Square Brackets and Extra Spaces
		article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
		article_text = re.sub(r'\s+', ' ', article_text)

		# Removing special characters and digits
		formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
		formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
		sentence_list = nltk.sent_tokenize(article_text)
		stopwords = nltk.corpus.stopwords.words('english')
		word_frequencies = {}
		for word in nltk.word_tokenize(formatted_article_text):
    		 if word not in stopwords:
        		if word not in word_frequencies.keys():
            		 word_frequencies[word] = 1
        		else:
            		 word_frequencies[word] += 1
		maximum_frequncy = max(word_frequencies.values())
		for word in word_frequencies.keys():
    		 word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
		sentence_scores = {}
		for sent in sentence_list:
    		 for word in nltk.word_tokenize(sent.lower()):
        		if word in word_frequencies.keys():
            		 if len(sent.split(' ')) < 30:
                		if sent not in sentence_scores.keys():
                    		 sentence_scores[sent] = word_frequencies[word]
                		else:
                    		 sentence_scores[sent] += word_frequencies[word]

		summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)
		summary = ' '.join(summary_sentences)
		print(summary)
		return render_template('result.html',result=summary)
    	 	 
			 

if __name__ == '__main__':
	app.run(debug=True)


