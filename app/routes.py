from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from datetime import datetime, timezone

@app.route('/')
def index():
    return render_template('index.html')
