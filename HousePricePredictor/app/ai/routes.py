import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request
from flask_login import current_user
from ..ai.forms import PredictForm
from ..ai.model import SimpleLinearRegression
from ..models import db, Model, PredictionHistory

ai_bp = Blueprint('ai', __name__, url_prefix='/ai', template_folder='templates')

@ai_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if not current_user.is_authenticated:
        return render_template('ai/login_required.html')

    form = PredictForm()
    prediction = None
    graph_url = None
    loss_graph_url = None
    new_prediction = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        furnished = form.furnished.data
        furnished_numeric = 1 if furnished == 'yes' else 0
        city = form.city.data

        action = request.form.get("action")

        # Prepare input
        size_log = np.log(size + 1)
        x_data = np.array([[size_log, rooms, furnished_numeric]])

        # Training data
        sizes = np.array([50, 60, 70, 80, 90, 100])
        sizes_log = np.log(sizes + 1)
        rooms_arr = np.array([2, 3, 3, 4, 4, 5])
        furnished_arr = np.array([1, 0, 1, 0, 1, 0])

        X = np.column_stack((sizes_log, rooms_arr, furnished_arr))
        y = np.array([100000, 110000, 140000, 130000, 180000, 160000])

        model = SimpleLinearRegression()
        model.fit(X, y)

        # Save model to DB
        new_model = Model(name="SimpleLinearRegression", version="1.0")
        db.session.add(new_model)
        db.session.commit()

        prediction = model.predict(x_data)[0]

        # Adjust price based on city
        city_factors = {
            'sofia': 1.3,
            'plovdiv': 1.1,
            'varna': 1.0,
            'burgas': 0.9
        }
        factor = city_factors.get(city, 1.0)
        prediction *= factor

        # Always save prediction history when prediction is made
        new_prediction = PredictionHistory(
            user_id=current_user.id,
            area=size,
            rooms=rooms,
            furnished=furnished_numeric,
            city=city,
            result=prediction
        )
        db.session.add(new_prediction)
        db.session.commit()

        if action == "show_graph":
            # Plot graph 1
            plt.figure(figsize=(6, 4))
            plt.scatter(sizes, y, color='blue', label='Данни')
            rooms_mean = np.mean(rooms_arr)
            furnished_fixed = 1
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
            plt.title("Регресия върху данните")
            plt.legend()
            plt.tight_layout()

            buf1 = io.BytesIO()
            plt.savefig(buf1, format='png')
            buf1.seek(0)
            graph_url = base64.b64encode(buf1.getvalue()).decode('utf-8')
            buf1.close()
            plt.close()

            # Plot graph 2
            plt.figure(figsize=(6, 4))
            plt.plot(model.loss_history, color='orange')
            plt.xlabel("Итерация")
            plt.ylabel("Загуба (MSE)")
            plt.title("Загуба при обучението")
            plt.tight_layout()

            buf2 = io.BytesIO()
            plt.savefig(buf2, format='png')
            buf2.seek(0)
            loss_graph_url = base64.b64encode(buf2.getvalue()).decode('utf-8')
            buf2.close()
            plt.close()

    return render_template(
        'ai/predict.html',
        form=form,
        prediction=prediction,
        graph_url=graph_url,
        loss_graph_url=loss_graph_url
    )

@ai_bp.route('/history')
def history():
    if not current_user.is_authenticated:
        return render_template('ai/login_required.html')

    # Query PredictionHistory model, not Prediction model
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.timestamp.desc()).all()

    return render_template('ai/prediction_history.html', predictions=predictions)