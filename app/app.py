from flask import Flask
from flask_cors import CORS


import sys
sys.path.append("..")

from random import randint
from MarkovModelSentenceGenerator import MarkovModelSentenceGenerator

app = Flask(__name__)
CORS(app)

books = ["prideandprejudice.txt", "madamebovary.txt", "persuasion.txt", "sleepingbeauty.txt"]

@app.route("/")
def index():
    return "Flask App!"


# @app.route("/hello/<string:name>")
@app.route("/sentence", methods=["GET"])
def hello():
    randomNumber = randint(0, len(books) - 1)
    sentence_generator = MarkovModelSentenceGenerator()
    sentence_generator.create_freq_table(books[randomNumber])
    sentence_generator.compute_weighted_probabilities()
    sentence = sentence_generator.generate_sentence()

    return sentence

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
