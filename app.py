import flask
from tensorflow import keras
import numpy as np

model = keras.models.load_model('model/model.h5')

app = flask.Flask(__name__, template_folder='templates')


def preprocess(sexe, section, score):
    if (sexe == 'Homme'):
        input_sexe = 1.
    else:
        input_sexe = 0.
    if section == 'Informatique':
        input_sec_1 = input_sec_2 = input_sec_3 = 0.
    elif section == 'Mathématique':
        input_sec_1 = 1.
        input_sec_2 = 0.
        input_sec_3 = 0.
    elif section == 'Science':
        input_sec_1 = 0.
        input_sec_2 = 1.
        input_sec_3 = 0.
    else:
        input_sec_1 = 0.
        input_sec_2 = 0.
        input_sec_3 = 1.

    input = np.array([[input_sexe, input_sec_1, input_sec_2, input_sec_3, score]], dtype=float)
    return input


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('main.html')

    if flask.request.method == 'POST':
        sexe = flask.request.form['sexe']
        section = flask.request.form['section']
        score = flask.request.form['score']

        input = preprocess(sexe, section, score)
        prediction = model.predict(input)
        for i in range(0, 4):
            prediction[0][i] = round(prediction[0][i], 2)
            if prediction[0][i] > 100:
                prediction[0][i] = 100
            if prediction[0][i] < 0:
                prediction[0][i] = 1

        return flask.render_template(
            'main.html',
            original_input={'Sexe': sexe,
                             'Section': section,
                             'Score bac': score},
                             result = True,
                             gl = prediction[0][0],
                             iia = prediction[0][1],
                             rt =  prediction[0][2],
                             imi = prediction[0][3]
                                     )


if __name__ == '__main__':
    app.run()
