##train data for the sentiment analysis
train = [
('What an amazing weather.', 'satisfied'),
('this is an amazing idea!', 'satisfied'),
('feel very good about these ideas.', 'satisfied'),
('this is my best performance.', 'satisfied'),
("what an awesome view", 'satisfied'),
('thank you so much', 'satisfied'),
('Thanks','satisfied'),
('Thank','satisfied'),
('I hate this place', 'unsatisfied'),
('am tired of this stuff.', 'slightly unsatisfied'),
('he is my sworn enemy!', 'unsatisfied'),
('my friends is horrible.', 'unsatisfied'),
('she do not know how to', 'unsatisfied'),
('she is beautiful','satisfied'),
('she is ugly', 'unsatisfied'),
('very few give', 'unsatisfied'),
('too big to give','satisfied'),
("rarely enter",'unsatisfied'),
('bati mutudlo','unsatisfied'),
('kamao mutudlo','satisfied'),
('always present','satisfied'),
('always absent','unsatisfied'),
('go ahead and be absent','unsatisfied'),  
('too much to do', 'unsatisfied'),
('gives us time to do', 'satisfied'),
('she comes early', 'satisfied'), 
('mostly comes early', 'slight satisfied'),
('sometimes late', 'slightly unsatisfied'),
('she comes late', 'unsatisfied'),
('she is late sometimes', 'slightly unsatisfied'),
('Ramesh is a friend of mine.', 'slightly satisfied'),
('she is sometimes not in the mood', 'slightly satisfied'),
('gwapa','satisfied'),
('feel and nawng','unsatisfied'),
('he is a good and very kind','satisfied'),
('bad', 'unsatisfied'),
('good','satisfied'),
('little will give a','unsatisfied'),
('size and grade','satisfied'),
('not going on and absent','unsatisfied'),
('not effective','unsatisfied'),
('ineffective', 'unsatisfied'),
('They are not doing their job','unsatisfied'),
('effective', 'satisfied'),
('like','satisfied'),
('I dont like you','unsatisfied'),
('monetary','unsatisfied'),
('no obvious','unsatisfied'),
('clear','satisfied'),
('putang ina','unsatisfied'),
('stupid','unsatisfied'),
('bogo', 'unsatisfied'),
('bright mutudlo','satisfied'),
('fist find a way','satisfied'),
('curiosity finds a way','satisfied'),
('boutan','satisfied'),
('nothing', 'neutral'),
('I don\'t know what to say', 'neutral'),
('I dont know what to say', 'neutral'),
('no comment','neutral'),
('ambot', 'neutral'),
('wa lang','neutral'),
('Don\'t Know Mind','unsatisfied'),
('Knowledge Mutual','satisfied'),
('Slightly grade and grade','unsatisfied'),
('great grade and grade','satisfied'),
('Bati Mutut','unsatisfied'),
('nice to get','satisfied'),
('I like you','satisfied'),
('licks and fingers','satisfied')
 ]
test = [
('the food was great.', 'satisfied'),
("I feel amazing!", 'satisfied'),
('follows schedule','satisfied'),

('I do not want to live anymore', 'unsatisfied'),
('she is not beautiful','unsatisfied'),
("I ain't feeling dandy today.", 'unsatisfied'),

('I have nothing to say', 'neutral')
]

from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from googletrans import Translator
from nltk.text import TextCollection
from textblob.classifiers import NaiveBayesClassifier
import enchant
from array import * 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost';
app.config['MYSQL_USER'] = 'root';
app.config['MYSQL_PASSWORD'] = '';
app.config['MYSQL_DB'] = 'isent';

mysql = MySQL(app)

@app.route("/login.html", methods=["POST","GET"])
def login():
	if request.method == "POST":
		return redirect(url_for("evaluate"))
	else:
		return render_template("login.html")

@app.route("/evaluation page", methods = ["POST", "GET"])
def evaluate():
	
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM questionaire where section = 1")
	section1 = cur.fetchall()

	cur.execute("SELECT * FROM questionaire where section = 2")
	section2 = cur.fetchall()

	cur.execute("SELECT * FROM questionaire where section = 3")
	section3 = cur.fetchall()

	cur.execute("SELECT * FROM questionaire where section = 4")
	section4 = cur.fetchall()

	cur.execute("SELECT * FROM questionaire where section = 5")
	section5= cur.fetchall()

	cur.close()


	if request.method == 'POST':
		#Declaring variables for list to store rating in each section
		sec1_rating	= []
		sec2_rating	= []
		sec3_rating	= []
		sec4_rating	= []
		sec5_rating	= []

		for i in range(len(section1)):
				sec1_rating.append(request.form[f'rating[{i}]'])

		for i in range(len(section2)):
				sec2_rating.append(request.form[f'rating2[{i}]'])

		for i in range(len(section3)):
				sec3_rating.append(request.form[f'rating3[{i}]'])

		for i in range(len(section4)):
				sec4_rating.append(request.form[f'rating4[{i}]'])

		for i in range(len(section5)):
				sec5_rating.append(request.form[f'rating5[{i}]'])

		#code for the translation and getting sentiment analysis
		comment = request.form["txtcomment"]


		cl = NaiveBayesClassifier(train)
		translator = Translator()

		# Lets test the accuracy of the classifier
		#print ("training set accuracy : ", cl.accuracy(train))
		#print ("test set accuracy     : ", cl.accuracy(test))
		if (len(comment) == 0):
			result = "neutral"

		else:
		    translated = translator.translate(comment, dest="en")

	     	#check if the word exist
		    count_string = (len(translated.text.strip().split(" ")))

		    if (count_string <= 1):
		          if(count_string == 0):
		               result = "neutral"
		          elif(count_string == 1):
		               d = enchant.Dict("en_US")
		               check_word = d.check(translated.text)

		               #counter number of letters (own logic (there is no sentimental word that has
		               # 1 or 2 letters only))
		               if(len(translated.text) <= 2):
		                    result="neutral"
		               #if the word exist then classify else neutral
		               elif(check_word):
		                     result = cl.classify(translated.text)
		               else:
		                    result="neutral"


		    else:
		          result = cl.classify(translated.text)

		
		try:       
			cur = mysql.connection.cursor()
			#converting list into string
			sec1_string = ','.join(sec1_rating) 
			sec2_string = ','.join(sec2_rating)
			sec3_string = ','.join(sec3_rating) 
			sec4_string = ','.join(sec4_rating) 
			sec5_string = ','.join(sec5_rating)    

			sql = "INSERT INTO evaluation (idteacher,idstudent,section1,section2,section3,section4,section5,comment,sentiment)\
			 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
			val = ("18013672","18013672",sec1_string,sec2_string,sec3_string,sec4_string,sec5_string,comment,result)
			cur.execute(sql,val)
			mysql.connection.commit()
			cur.close()
			return f'<h1>Successfully saved!</h1>'

		except Exception as exp:
			return f'<h1>{exp}</h1>'

		#return redirect(url_for("scratch", sec1_rating = sec1_rating, sec2_rating = sec2_rating, sec3_rating = sec3_rating,
		#			sec4_rating = sec4_rating,sec5_rating = sec5_rating, result = result))

	else:
		return render_template("evaluation_page.html", section1 = section1, section2 = section2, lensec1 = len(section1),
			lensec2= len(section2), section3 = section3, lensec3= len(section3), section4 = section4, lensec4 = len(section4),
			section5 = section5, lensec5 = len(section5))


@app.route("/<sec1_rating><sec2_rating><sec3_rating><sec4_rating><sec5_rating><result>")
def scratch(sec1_rating, sec2_rating,sec3_rating, sec4_rating,sec5_rating, result):
	return f"<h1>{sec1_rating}{sec2_rating}{sec3_rating}{sec4_rating}{sec5_rating}{result}</h1>"

if __name__ == "__main__":
	app.run(debug =True)