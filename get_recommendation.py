from django.http import JsonResponse
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import col
import json

def get_recommendations(request):
    # Инициализируем Spark Session
    spark = SparkSession.builder.appName('Recommendation System').getOrCreate()
    
    # Получаем данные из запроса
    data = json.loads(request.body)
    social = data['social']
    friends = int(data['friends'])

    # Загружаем исходные данные
    interactions = spark.read.csv('path_to_data.csv', header=True, inferSchema=True)
    filtered_data = interactions.filter((col('social') == social) & (col('friends') == friends))

    # Обучение модели ALS
    als = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="item_id", ratingCol="rating", coldStartStrategy="drop")
    model = als.fit(filtered_data)

    # Создание рекомендаций
    user_subset = filtered_data.select(als.getUserCol()).distinct()
    recommendations = model.transform(user_subset)

    recommendations_list = recommendations.collect()
    recommendations_json = [{'user_id': row['user_id'], 'recommendation': row['prediction']} for row in recommendations_list]

    return JsonResponse({'recommendations': recommendations_json})

# Не забудьте добавить URL-маршрут в urls.py:
# path('recommendations', views.get_recommendations, name='get_recommendations')
