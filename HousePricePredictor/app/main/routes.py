from flask import Blueprint, render_template

from HousePricePredictor.app.main.forms import PredictForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    prediction = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        # Използвай само полетата, които имаш във формата
        prediction = size * 1000 + rooms * 5000

    return render_template('ai/predict.html', form=form, prediction=prediction)