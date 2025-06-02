import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request
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
    show_graph_button = False

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        furnished = form.furnished.data
        furnished_numeric = 1 if furnished == 'yes' else 0

        action = request.form.get("action")

        # Подготовка на входа
        size_log = np.log(size + 1)
        x_data = np.array([[size_log, rooms, furnished_numeric]])

        # Примерни обучаващи данни
        sizes = np.array([50, 60, 70, 80, 90, 100])
        sizes_log = np.log(sizes + 1)
        rooms_arr = np.array([2, 3, 3, 4, 4, 5])
        furnished_arr = np.array([1, 0, 1, 0, 1, 0])

        X = np.column_stack((sizes_log, rooms_arr, furnished_arr))
        y = np.array([100000, 110000, 140000, 130000, 180000, 160000])

        model = SimpleLinearRegression()
        model.fit(X, y)

        prediction = model.predict(x_data)[0]
        show_graph_button = True

        if action == "show_graph":
            plt.figure(figsize=(6, 4))
            plt.scatter(sizes, y, color='blue', label='Данни')

            rooms_mean = np.mean(rooms_arr)
            furnished_fixed = 1  # Визуализация при обзаведено

            sizes_plot = np.linspace(min(sizes), max(sizes), 100)
            sizes_plot_log = np.log(sizes_plot + 1)
            X_plot = np.column_stack((
                sizes_plot_log,
                np.full_like(sizes_plot_log, rooms_mean),
                np.full_like(sizes_plot_log, furnished_fixed)
            ))
            y_plot = model.predict(X_plot)

            plt.plot(sizes_plot, y_plot, color='red', label='Регресия (лог)')
            plt.xlabel("Размер (кв.м.)")
            plt.ylabel("Цена (€)")
            plt.legend()
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()

    return render_template('ai/predict.html', form=form, prediction=prediction, graph_url=graph_url, show_graph_button=show_graph_button)
