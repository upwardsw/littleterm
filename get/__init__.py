from flask import Blueprint
get=Blueprint('get',__name__,url_prefix='/get')
from . import getviews