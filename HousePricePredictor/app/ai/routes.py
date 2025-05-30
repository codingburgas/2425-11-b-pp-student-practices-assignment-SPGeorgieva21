import io
import base64
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from ..ai.forms import PredictForm
from ..ai.model import SimpleLinearRegression

ai_bp = Blueprint('ai', __name__, url_prefix='/ai', template_folder='templates')

@ai_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if not current_user.is_authenticated:
        return render_template('ai/login_required.html')

    form = PredictForm()
    prediction = None
    graph_url = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        x_data = [size + rooms]  # Сума на двете стойности

        # Примерни тренировъчни данни
        X = [50, 60, 70, 80, 90, 100]
        y = [100000, 120000, 140000, 160000, 180000, 200000]

        model = SimpleLinearRegression()
        model.fit(X, y)

        prediction = model.predict(x_data)[0]

        plt.figure(figsize=(6, 4))
        plt.scatter(X, y, color='blue', label='Данни')
        plt.plot(X, model.predict(X), color='red', label='Регресия')
        plt.xlabel("Size (m²)")
        plt.ylabel("Price (€)")
        plt.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

    return render_template('ai/predict.html', form=form, prediction=prediction, graph_url=graph_url)
