import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

import flask
from flask import Flask, request, render_template

# nlp = spacy.blank("en") # load a new spacy model
# db = DocBin() # create a DocBin object

# import json
# f = open('annotations (12).json')
# TRAIN_DATA = json.load(f)
# # print(TRAIN_DATA)

# for text, annot in tqdm(TRAIN_DATA['annotations']): 
#     doc = nlp.make_doc(text) 
#     ents = []
#     for start, end, label in annot["entities"]:
#         span = doc.char_span(start, end, label=label, alignment_mode="contract")
#         if span is None:
#             print("Skipping entity")
#         else:
#             ents.append(span)
#     doc.ents = ents 
#     db.add(doc)

# db.to_disk("./training_data.spacy") # save the docbin object

app = Flask(__name__)
model = spacy.load('model-best')

@app.route('/',methods=['POST','GET'])
def index():
    input_text = request.form.get('input_text')
    if request.method == 'POST':
        pii_detected = []
        try:

            output = model(input_text)

            for word in output.ents:
                pii_detected.append(word.text)

            final_output = {
                'pii_detected' : pii_detected,
                'error' : ''
            }
        
        except Exception as e:
        
            final_output = {
                'pii_detected' : '',
                'error' : e
            }
        return render_template('index.html',final_output=final_output)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)