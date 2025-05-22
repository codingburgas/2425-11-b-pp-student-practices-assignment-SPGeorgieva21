from flask_login import login_required
# ... останалото ...

@ai_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictForm()
    prediction = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        x_input = np.array([[size, rooms]])
        prediction = model.predict(x_input)[0]

    return render_template('ai/predict.html', form=form, prediction=prediction)
