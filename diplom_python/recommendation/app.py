from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import time
from datetime import datetime

app = Flask(__name__)

# Загрузка модели
model = load_model('diplom.h5')

# Загрузка данных
data = pd.read_csv('datadiplom.csv')

# Кодирование категориальных переменных
label_encoder_gender = LabelEncoder()
data['Gender'] = label_encoder_gender.fit_transform(data['Gender'])
label_encoder_temperament = LabelEncoder()
data['Corrected Temperament'] = label_encoder_temperament.fit_transform(data['Corrected Temperament'])

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/recommend', methods=['POST'])
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_temperament = request.form['temperament']
        user_date = request.form['date']
        user_age = int(request.form['age'])
        user_gender = request.form['gender']

        if user_date.lower() == 'now':
            user_timestamp = int(time.time())
        else:
            user_datetime = datetime.strptime(user_date, '%Y-%m-%d %H:%M:%S')
            user_timestamp = int(user_datetime.timestamp())

        temperament_encoded = label_encoder_temperament.transform([user_temperament])[0]
        gender_encoded = label_encoder_gender.transform([user_gender])[0]

        # Создание списка из четырех отдельных входных массивов
        input_data = [np.array([temperament_encoded]), np.array([gender_encoded]), np.array([user_timestamp]), np.array([user_age])]

        # Предсказание модели
        predicted_preference = model.predict(input_data)[0]

        if predicted_preference > 0.5:
            preferred_movies = data[(data['Corrected Temperament'] == temperament_encoded) & (data['Rating'] >= 4)]
            recommended_movies = preferred_movies['Title'].value_counts().nlargest(5).index.tolist()
            return f"Рекомендуемые фильмы: {recommended_movies}"
        else:
            return "На основе ваших предпочтений, рекомендуемые фильмы не найдены."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
