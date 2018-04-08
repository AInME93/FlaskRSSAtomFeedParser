from flask import Blueprint

feeds = Blueprint('feeds', __name__)

from . import views