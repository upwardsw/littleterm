from flask import Blueprint
generate=Blueprint('generate',__name__,url_prefix='/genenrate')
from . import genviews