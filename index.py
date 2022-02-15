from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import collections as cl
import time
import os
import json
import csv
import TJ

app = Flask(__name__)
bootstrap = Bootstrap(app)
UPLOAD_FOLDER = './upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET'])
def get():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
  f1 = request.files.get('csv')
  filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f1.filename))
  f1.save(filename)
  data_dict_sorted = {}

  parameter = request.form.get('radio')
  
  if parameter == "PTJ":
    data_dict_sorted = TJ.PTJ(filename)
  elif parameter == "NPTJ5":
    data_dict_sorted = TJ.NPTJ5(filename)
  elif parameter == "NPTJ20":
    data_dict_sorted = TJ.NPTJ20(filename)
  elif parameter == "NPTJ100":
    data_dict_sorted = TJ.NPTJ100(filename)

  return render_template('index.html', data_dict=data_dict_sorted, query_file=f1)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)
