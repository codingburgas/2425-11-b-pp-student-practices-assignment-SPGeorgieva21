import io
import base64
import matplotlib.pyplot as plt
from flask import Blueprint, render_template
from app.ai.forms import PredictForm
from app.ai.model import SimpleLinearRegression

ai_bp = Blueprint('ai', __name__, template_folder='templates')

@ai_bp.route('/predict', methods=['GET', 'POST'])
def predict():
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

        # 🎨 Генерирай графиката
        plt.figure(figsize=(6, 4))
        plt.scatter(X, y, color='blue', label='Данни')
        plt.plot(X, model.predict(X), color='red', label='Регресия')
        plt.xlabel("Size (m²)")
        plt.ylabel("Price (€)")
        plt.legend()
        plt.tight_layout()

        # 📸 Конвертирай в base64 за HTML
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

    return render_template('predict.html', form=form, prediction=prediction, graph_url=graph_url)
