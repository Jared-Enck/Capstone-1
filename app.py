from flask_cors import CORS
from flask import Flask, redirect, render_template, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///digimon_tcg_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ayyfirstcapstonewoo!4242'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)