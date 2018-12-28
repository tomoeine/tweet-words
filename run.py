# coding:utf-8
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import models

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    """ トップページ """
    return render_template('index.html', results={})
 
@app.route('/view/<twitter_name>')
def view(twitter_name):
    """ 分析 """
    result = models.mecab_analyze(twitter_name)
    return render_template('view.html',  result=result, twitter_name=twitter_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
