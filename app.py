from flask import Flask

app= Flask(__name__)
@app.route('/add/<int:number1>/<int:number2>')

def add(number1, number2):
    return f" {number1} + {number2} = {number1+number2}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)