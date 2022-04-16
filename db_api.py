import pymongo 
from uuid import uuid1
from flask import Flask, request, url_for

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.test
texts = db.texts


@app.route('/save_text', methods=['POST'])
def save_text():
    if request.method == 'POST' and request.json:
        text = request.json.get('text')
        if text:
            id = str(uuid1())
            text = {
                'id': id,
                'text': text,
            }
            # db add text
            # db.add() or something
            texts.insert_one(text)
            return {'result': 'ok', 'id': id}
    return {'result': 'error', 'error': 'proizoshel kal'}

@app.route('/get_text')
def get_text():
    id = request.args.get('id')
    if id:
        text: dict = texts.find_one({'id': id})
        if text:
            text.pop('_id')
            return {'result': [text]}
        else:
            return {
                'result': 'error',
                'error_message': 'no such id'
            }
    else:
        # return all
        result = []
        for text in texts.find():
            text.pop('_id')
            result.append(text)
        return {'result': result}

@app.route('/delete_text', methods=['POST'])
def delete_text():
    if request.method == 'POST' and request.json:
        id = request.json.get('id')
        if id:
            result = texts.delete_one({'id': id})
            if result.deleted_count == 1:
                return {'result': 'ok'}
            else:
                return {
                    'result': 'error',
                    'error_message': f'no such id {id}'
                }
        return {
            'result': 'error',
            'error_message': 'id was not passed'
        }

