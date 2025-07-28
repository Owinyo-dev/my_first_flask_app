import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, Response, send_from_directory
app=Flask(__name__, template_folder='templates')

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method== 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')

        if username == 'brenda' and password== '123456':
            return 'success'
        else:
            return 'failed'
        
@app.route('/fileupload', methods=['POST'])
def file_upload():
    file=request.files['file']
    if file.content_type == 'text/plain':
        return file.read().decode()
    elif file.content_type in ['application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel.sheet.macroEnabled.12']:
        df=pd.read_excel(file)
        return df.to_html()
    else:
        return 'Unsupported file type', 400
    

@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    file = request.files['file']
    df = pd.read_excel(file)

    response = Response(df.to_csv(), mimetype='text/csv', headers={
        'Content-Disposition': 'attachment; filename=converted.csv'
    })
    return response


@app.route('/convert_csv2', methods=['POST'])
def convert_csv2():
    file = request.files['file']
    df=pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f"{uuid.uuid4()}.csv"
    df.to_csv(os.path.join('downloads', filename))

    return render_template('download',filename,download_name='result.csv')


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, download_name = 'result.csv')
 


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)