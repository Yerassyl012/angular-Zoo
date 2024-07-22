from django.shortcuts import render
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def get_recommendations(request):
    if request.method == 'POST':
        social = request.POST.get('social')
        friends = int(request.POST.get('friends'))

        # Инициализация Spark
        spark = SparkSession.builder.appName('Recommendation System').getOrCreate()

        # Загрузка датасета
        events = spark.read.csv('path_to_events.csv', header=True, inferSchema=True)

        # Фильтрация по критериям
        if social == 'yes':
            filtered_data = events.filter((col('audience') == 'extrovert'))
        else:
            filtered_data = events.filter((col('audience') == 'introvert'))

        # Дополнительная фильтрация по количеству друзей
        friend_filter = 'low' if friends < 5 else 'high' if friends > 15 else 'medium'
        recommendations = filtered_data.filter(col('friends') == friend_filter).collect()

        # Конвертация результатов в список для отображения
        recommendations_list = [f"{row['type']} - {row['name']}" for row in recommendations]

        return render(request, 'index.html', {'recommendations': recommendations_list})

    return render(request, 'index.html')
