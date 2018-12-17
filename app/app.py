from flask import Flask, request
from flask_cors import CORS
import json
from random import randint
# change to.MarkovoModelSentenceGenerator to deploy
from MarkovModelSentenceGenerator import MarkovModelSentenceGenerator

app = Flask(__name__)
CORS(app)

BOOK_FILES = ["app/prideandprejudice.txt", "app/madamebovary.txt", "app/persuasion.txt", "app/sleepingbeauty.txt"]

@app.route("/")
def index():
    return "Flask App!"


# @app.route("/hello/<string:name>")
@app.route("/sentence", methods=["GET"])
def hello():
    data = request
    print(data)
    books = request.args.get('books')
    dict = json.loads(books)
    sentence_generator = MarkovModelSentenceGenerator()

    selected_books = []
    for key in dict:
        print(key, dict[key])
        if dict[key]:
            selected_books.append(key)
    if len(selected_books) == 0:
        # generate a random sentence
        print("RANDOM")
        randomNumber = randint(0, len(BOOK_FILES) - 1)
        sentence_generator.create_freq_table(BOOK_FILES[randomNumber])
        sentence_generator.compute_weighted_probabilities()
        sentence = sentence_generator.generate_sentence()
        return sentence

    else:
        print("NOT RANDOM")
        for key in selected_books:
            key = key.lower()
            key = key.replace(' ', '')
            print("app/" + key + ".txt")
            sentence_generator.create_freq_table("app/" + key + ".txt")
        sentence_generator.compute_weighted_probabilities()
        sentence = sentence_generator.generate_sentence()
        return sentence

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
