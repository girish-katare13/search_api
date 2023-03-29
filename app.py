import json
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

#endpoint for the search api
@app.route('/search')
def search_comments():
    #retrive values of all parameter from request
    author_name = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')
    
    #fetch the existing api to get comments
    response = requests.get('https://dev.ylytic.com/ylytic/test')
    
    comment_list = json.loads(response.text)['comments']

    #filter the comments with respect to the parameter's values
    comments = [comment for comment in comment_list if 
                (not author_name or comment['author'].lower() in author_name.lower()) and
                (not at_from or comment['at'] >= at_from) and
                (not at_to or comment['at'] <= at_to) and
                (not like_from or comment['like'] >= int(like_from)) and
                (not like_to or comment['like'] <= int(like_to)) and
                (not reply_from or comment['reply'] >= int(reply_from)) and
                (not reply_to or comment['reply'] <= int(reply_to)) and
                (not search_text or search_text.lower() in comment['text'].lower())]

    return jsonify(comments)

if __name__ == '__main__':
    app.run(debug=True)
