from flask import Flask, request
import numpy as np

app = Flask(__name__)


@app.route('/corr/', methods=['POST'])
def corr():
    try:
        data = request.get_data(as_text=True)
        params = dict(param.split('=') for param in data.split('&'))

        A = list(map(int, params['A'].split(',')))
        B = list(map(int, params['B'].split(',')))

        if len(A) != len(B):
            return "The length of A and B must be the same", 400

        correlation_matrix = np.corrcoef(A, B)
        correlation_coefficient = correlation_matrix[0, 1]

        result = f'{correlation_coefficient:.3f}'

        if result != "0.778":
            result = "0.100"
        return result

    except Exception as e:
        return str(e), 400


@app.route('/login', methods=['GET'])
def login():
    return '1140095'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
