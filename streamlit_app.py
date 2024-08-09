import streamlit as st
import time
import json
from datetime import datetime

# Inicializar variáveis de estado
if 'running' not in st.session_state:
    st.session_state.running = False

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if 'current_speech' not in st.session_state:
    st.session_state.current_speech = None

if 'data' not in st.session_state:
    st.session_state.data = []

if 'view' not in st.session_state:
    st.session_state.view = 'Cronômetro'

# Funções para carregar e salvar dados
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

# Carregar dados
data = load_data()

# Função para iniciar o cronômetro
def start_timer(speech):
    st.session_state.current_speech = speech
    st.session_state.start_time = time.time()
    st.session_state.running = True
    st.session_state.view = 'Cronômetro'

# Função para parar o cronômetro
def stop_timer():
    if st.session_state.running:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.running = False
        st.session_state.data.append({
            'orador': st.session_state.current_speech['orador'],
            'discurso': st.session_state.current_speech['discurso'],
            'tempo': round(elapsed_time, 2),
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        save_data(st.session_state.data)

# Função para formatar o tempo em Minutos:Segundos
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Interface do cronômetro
if st.session_state.view == 'Cronômetro':
    st.title("Cronômetro de Discursos")
    
    if st.session_state.running:
        elapsed_time = time.time() - st.session_state.start_time
        time_left = st.session_state.current_speech['tempo_previsto'] * 60 - elapsed_time
        
        if time_left > 60:
            color = "green"
        elif time_left > 0:
            color = "yellow"
        else:
            color = "red"
        
        st.markdown(f"<h1 style='color:{color}; text-align: center; font-size: 100px;'>{format_time(elapsed_time)}</h1>", unsafe_allow_html=True)
        st.progress(elapsed_time / (st.session_state.current_speech['tempo_previsto'] * 60))
        st.subheader(st.session_state.current_speech['orador'])
        st.caption(st.session_state.current_speech['discurso'])
        
        if st.button("Parar Cronômetro"):
            stop_timer()
    else:
        st.write("Cronômetro não iniciado. Use a tela de cadastro para iniciar o cronômetro.")
    
    if st.button("Ir para Cadastro"):
        st.session_state.view = 'Cadastro'

# Interface de cadastro de discursos
elif st.session_state.view == 'Cadastro':
    st.title("Cadastro de Discursos")
    with st.form("Cadastro de Discurso"):
        orador = st.text_input("Nome do Orador")
        discurso = st.text_input("Nome do Discurso")
        tempo_previsto = st.number_input("Tempo Previsto (em minutos)", min_value=1, step=1)
        submit_button = st.form_submit_button("Cadastrar Discurso")

        if submit_button:
            data.append({
                'orador': orador,
                'discurso': discurso,
                'tempo_previsto': tempo_previsto
            })
            save_data(data)
            st.success("Discurso cadastrado com sucesso!")

    for i, speech in enumerate(data):
        if st.button(f"Iniciar {speech['discurso']} ({speech['orador']})"):
            start_timer(speech)

    if st.button("Ir para Cronômetro"):
        st.session_state.view = 'Cronômetro'

# Exibir tempos dos discursos anteriores
if st.button("Ver Tempos Registrados"):
    st.write(st.session_state.data)