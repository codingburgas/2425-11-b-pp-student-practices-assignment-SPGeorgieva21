from flask import Blueprint
from app.admin import routes

admin_bp = Blueprint('admin', __name__, template_folder='templates')


