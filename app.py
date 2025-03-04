from flask import Flask, render_template, request
import os
import pandas as pd
import numpy as np
from projectFiles.pipeline.prediction import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def homePage():
    return render_template("index.html")