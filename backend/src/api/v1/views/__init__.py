from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.auth.decorator import *
from api.v1.views.auth.register import *
from api.v1.views.auth.login import *
from api.v1.views.auth.reset_password import *
