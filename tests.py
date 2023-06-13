import streamlit as st
import folium
import streamlit_folium as sf
import json
from folium import LatLngPopup
from folium.plugins import LocateControl


# # Задайте начальные координаты для карты
# START_COORDINATES = (55.7602, 37.6185)

# # Создайте инструменты для ввода данных
# # (в данном случае мы просим пользователя ввести координаты точки на карте)
# lat = st.number_input('Введите широту', value=START_COORDINATES[0])
# lon = st.number_input('Введите долготу', value=START_COORDINATES[1])

# # Сгенерируйте точки на карте
# coordinates = [(lat, lon)]

# # Создайте карту
# map = folium.Map(location=START_COORDINATES, zoom_start=12)

# # Нарисуйте точки на карте
# for coord in coordinates:
#     folium.Marker(coord).add_to(map)

# # Выведите карту на экран
# folium_static(map)



# with open('K:\Downloads\Загрузки Яндекс\map.geojson', 'r') as temp:
#     st.write(json.loads(temp.read())['features'])