from flask import render_template, request
from . import ai_bp
from .forms import PredictForm
from .model import SimpleLinearRegression
import numpy as np

# Примерни тренировъчни данни
X_train = np.array([
    [1400, 3],
    [1600, 3],
    [1700, 4],
    [1875, 4],
    [1100, 2],
    [1550, 3]
])
y_train = np.array([245000, 312000, 279000, 308000, 199000, 219000])

# Обучаваме модела веднъж при стартиране
model = SimpleLinearRegression()
model.fit(X_train, y_train)

@ai_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictForm()
    prediction = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        x_input = np.array([[size, rooms]])
        prediction = model.predict(x_input)[0]

    return render_template('ai/predict.html', form=form, prediction=prediction)
