import streamlit as st
import pandas as pd
import numpy as np
import streamlit_folium as sf
import folium
from jinja2 import Template
from typing import Iterable
import geopandas as gpd


from DB_work import *

# pipreqs
table_name = 'test_table'
DB_object = DB_ORM()


st.set_page_config(page_title='ТЕСТ',page_icon=":bar_chart",layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# print(pd.DataFrame([55.7522, 37.6156], columns = ['lat', 'ln']))

START_COORDINATES = (52.2978, 104.296)
transport_types = ['Автобус', 'Трамвай', 'Троллейбус']
route_numbers = {}


for tr_type in transport_types:
    route_numbers.update({tr_type : [i[0] for i in DB_object.execute(f'''
        SELECT Route FROM {table_name} 
            WHERE Type = "{tr_type}"
    ''', is_change= False)]})


# st.session_state.update({ 'route_type' : transport_types }) if 'route_type' not in st.session_state else ''

# route_number = st.sidebar.number_input('Номер маршрута', min_value = 0, max_value = 9999, value = 0 if 'route_number' not in st.session_state else st.session_state.route_number)
# route_type = st.sidebar.selectbox('Тип транспорта', transport_types if 'route_type' not in st.session_state else st.session_state.route_type)

# route_number = st.sidebar.selectbox('Номер маршрута', options = DB_object.get_unique(table_name = table_name, column_name = 'Route') if 'route_number' not in st.session_state else st.session_state.route_number)
# route_number = st.sidebar.selectbox('Номер маршрута', options = route_numbers[route_type])


def state_updater(var_name : str, value : Iterable) -> bool:
    copy = st.session_state[var_name]                                 # не copy, чтобы работало с итерируемыми объектами
    copy.remove(value)
    copy.insert(0, value)
    st.session_state.update({ var_name : copy})


def marker_click_event(event):
    # Получение координат маркера
    lat, lon = event.latlng
    print("Нажат маркер на координатах:", lat, lon)
    

# if st.sidebar.button('Поиск', key = 'search_button_1'):
#     if st.session_state.route_type.index(route_type) != 0:
#         state_updater('route_type', route_type)


#     way_got = DB_object.get_route(route_num = route_number, route_type_ = route_type, table_name = table_name)
    
    # sf.folium_static(m)

    # if way_got:
    #     map = folium.Map(location=START_COORDINATES, zoom_start=12)
        # map.add_child(folium.ClickForLatLng(alert = True))
        # map.add_child(folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}"))
        # map.add_child(folium.LatLngPopup())
        # st.code(folium.Marker._template.render())

        
        # for counter in range(len(way_got)):
            # print(line)
        #     line = way_got[counter]

        #     folium.PolyLine(line).add_to(map)

            # if counter == len(way_got) -1:            # Возможно, неверно
            #     marker = [folium.Marker(line[0], popup=''), folium.Marker(line[-1], popup='')]

            # else:
            #     # marker = folium.Marker(line[-1], popup='''')
            #     marker = folium.Marker(line[-1], popup='')

            
            # if counter == 0:
            #     folium.PolyLine(line).add_to(map)
            #     # folium.Marker(line[0]).add_to(map)
            #     folium.Marker(line[-1]).add_to(map)
            
            # elif counter == len(way_got) -1:            # Возможно, неверно
            #     folium.PolyLine(line).add_to(map)
            #     folium.Marker(line[0]).add_to(map)
            #     folium.Marker(line[-1]).add_to(map)

            # else:
            #     folium.PolyLine(line).add_to(map)
            #     folium.Marker(line[-1]).add_to(map)

            # if isinstance(marker, list):
            #     for mark in marker:
            #         mark.add_to(map)
            
            # else:
            #     marker.add_to(map)

            # sf.folium_static(map)


        # st.write(map.get_root().render())
        

            
        # Выведите карту на экран
        # map = sf.folium_static(map)

        # DB_object.connection_close()
    
    # else:
    #     st.write("Выбранный маршрут не найден")





# Чтение данных из файла GeoJSON с помощью geopandas
# data = gpd.read_file('export.geojson')

# np.random.seed = 1

# Создание столбца "weight"
# data['weight'] = np.random.choice([1, 2, 3, 5], size=len(data), p=[0.3, 0.25, 0.2, 0.25]).tolist()
# data['weight'] = data['weight'].astype('int64')  # Преобразование типа данных в int

data = gpd.read_file('yes.geojson')

# Создание объекта карты folium
m = folium.Map(location=[52.22, 104.29], zoom_start=12)  # Задайте начальные координаты и масштаб карты

for index, row in data.iterrows():
    # Извлечение геометрии объекта
    geometry = row.geometry
    name = data.name[row.name]
    # weight = data['weight'].iloc()[row.name]
    weight = row['weight']

    # Добавление геометрии на карту folium
    if geometry.type == 'Point':
        # Обработка точечной геометрии
        coordinates = list(geometry.coords)[0]

        folium.Marker(location=[coordinates[1], coordinates[0]]).add_to(m)
    elif geometry.type == 'LineString':
        # Обработка линейной геометрии
        coordinates = list(geometry.coords)
        coordinates = [[sublist[1], sublist[0]] for sublist in coordinates]

        folium.PolyLine(locations=coordinates, popup=name, color='red').add_to(m)
    elif geometry.type == 'Polygon':
        # Обработка полигональной геометрии
        coordinates = list(geometry.exterior.coords)
        coordinates = [[sublist[1], sublist[0]] for sublist in coordinates]

        folium.Polygon(locations=coordinates, popup=name, color='red').add_to(m)

    elif geometry.type == 'MultiLineString':
        # Обработка мультисегментной линейной геометрии
        for line in geometry.geoms:
            coordinates = list(line.coords)
            coordinates = [[sublist[1], sublist[0]] for sublist in coordinates]

            folium.PolyLine(locations=coordinates, popup=name, color='red', weight=weight).add_to(m)

# колонка1, колонка2, колонка3, колонка4 = st.columns(4)
# # Сохранение карты в HTML-файл
# with колонка2:
sf.folium_static(m, width=1200, height=1000)