from flask import Blueprint

add=Blueprint('add',__name__,url_prefix='/add')

from . import addviews