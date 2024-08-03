from typing import OrderedDict
import joblib
import pandas as pd
import streamlit as st # type: ignore
import seaborn as sns
import json

#from otodom_ml import GroupbyTransformer, OutlierRemover,SimpleImputer, MultiplyTransformer, ColumnTransformer # type: ignore


st.header('Квартиры Польши: средняя цена по городу')

PATH_DATA = 'df_transformed2.csv'
#PATH_DATA = 'otogom_csv_data_full_6.csv'
#PATH_MODEL = 'model_6_weights.pkl'

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    data = data.sample(5000)
    return data

# @st.cache_data
# def load_model(path):
#     #data = pd.read_csv(path)
#     model = joblib.load(PATH_MODEL)
    
#     return model


@st.cache_data
def transform(data):
    colors = sns.color_palette("coolwarm").as_hex()
    n_colors = len(colors)
    
    data = data.reset_index(drop=True)
    # data["norm_price"] = data["price"] / data["area"]
    
    data["label_colors"] = pd.qcut(data["by_city__mean_target.Price"],n_colors, labels=colors)
    data["label_colors"] = data["label_colors"].astype("str")

    return data

df = load_data(PATH_DATA)

df = transform(df)
#st.write(df[:6])№ #если хотим вывести таблицу

df = df.rename(columns={'num__coordinates.latitude': 'latitude', 'num__coordinates.longitude': 'longitude'})
st.map(df)

    

# Открываем файл и загружаем словарь с городами
with open('cities_data_sorted.json', 'r') as f:
    cities = json.load(f)    
        
    
def user_input_features():
    st.sidebar.markdown("Выберите параметры Вашей квартиры для предсказания ее стоимости ")     

    miasta = ['Warszawa', 'Kraków', 'Łódź', 'Wrocław', 'Poznań', 'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Katowice', 'Białystok', 'Gliwice', 'Другой город']

    selected_miasto = st.sidebar.selectbox('Выберите город', miasta)
    selected_voivodeship = None  # Инициализация переменной
    selected_city = None  # Инициализация переменной

    if selected_miasto != 'Другой город':
        st.write(f"")
    else:
        # Получение списка воеводств
        voivodeships = list(cities.keys())
        # Выбор воеводства
        selected_voivodeship = st.sidebar.selectbox('Выберите воеводство', voivodeships)
        # Выбор города на основе выбранного воеводства
        selected_city = st.sidebar.selectbox('Выберите город', cities[selected_voivodeship])
     
    
      
    
    year_built = st.sidebar.slider('Год постройки', min_value=1900, max_value=int(max(df['ex_v_By__target.Build_year'])), value=1900)
    st.sidebar.markdown(" ")  
    floor = st.sidebar.number_input('Этаж квартиры', min_value=1, max_value=int(max(df['num__target.Floor_no'])))
    st.sidebar.markdown(" ")
    total_floors = st.sidebar.slider('Этажность дома', min_value=1, max_value=int(max(df['ex_v_Bfn__target.Building_floors_num'])))
    st.sidebar.markdown(" ")
    area = st.sidebar.number_input('Площадь (в кв. м)', min_value=int(min(df['ex_v_Area__target.Area'])), max_value=int(max(df['ex_v_Area__target.Area'])))
    st.sidebar.markdown(" ")
    rooms = st.sidebar.slider('Количество комнат',  min_value=1, max_value=int(max(df['num__target.Rooms_num'])))
    st.sidebar.markdown(" ")
    
        # Создаем словарь с выбранными параметрами в нужном порядке
    selected_params = OrderedDict()
    if selected_miasto != 'Другой город':
        selected_params['Город'] = selected_miasto
    else:
        selected_params['Воеводство'] = selected_voivodeship
        selected_params['город'] = selected_city
    selected_params['Год постройки'] = year_built
    selected_params['Этаж квартиры'] = floor
    selected_params['Этажность дома'] = total_floors
    selected_params['Площадь (в кв. м)'] = area
    selected_params['Количество комнат'] = rooms

    # Создаем строку Markdown с выбранными параметрами
    markdown_string = "## Выбранные параметры квартиры\n"
    for param, value in selected_params.items():
        if value is not None:  # Пропускаем параметры с значением None
            markdown_string += f"**{param}**: {value}<br>\n"

    st.markdown(markdown_string, unsafe_allow_html=True)

    # Сохраняем словарь в JSON-файл
    with open('selected_params.json', 'w', encoding='utf-8') as f:
        json.dump(selected_params, f, ensure_ascii=False, indent=4)
    
user_input_features()




button = st.button("Predict")
if button:
    st.write("Предсказание цены Вашей квартиры")



