from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.auth import *
from api.v1.views.files import *
from api.v1.views.patients import *
from api.v1.views.studies import *
from api.v1.views.series import *
from api.v1.views.instances import *
