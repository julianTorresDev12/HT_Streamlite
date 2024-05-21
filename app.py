import streamlit as st
import datetime as dt
import pytz
import holidays
import requests

# Simular datos de inventario y usuarios
inventories = [
    {"id": 1, "brand": "BrandA", "warehouse": "Warehouse1", "quantity": 100},
    {"id": 2, "brand": "BrandB", "warehouse": "Warehouse2", "quantity": 150},
]

users = [
    {"id": 1, "name": "TechnicianA", "warehouse_id": 1, "projects": [], "working_hours": []},
    {"id": 2, "name": "TechnicianB", "warehouse_id": 2, "projects": [], "working_hours": []},
]

st.title('Hootsi Application')

# Función de seguimiento de inventario
def track_inventory():
    st.header('Herramienta de Seguimiento de Inventario')
    
    action = st.selectbox('Selecciona una acción', ['Ver inventario', 'Marcar elementos', 'Reservar productos', 'Buscar especificaciones', 'Auditar inventario'])
    
    if action == 'Ver inventario':
        st.write('Inventario disponible:')
        for inventory in inventories:
            st.write(f"{inventory['quantity']} dispositivos de {inventory['brand']} en {inventory['warehouse']}")
    
    elif action == 'Marcar elementos':
        brand = st.selectbox('Selecciona la marca', ['BrandA', 'BrandB'])
        quantity = st.number_input('Cantidad de dispositivos a marcar', min_value=0)
        warehouse = st.selectbox('Selecciona la bodega de destino', ['Warehouse1', 'Warehouse2'])
        
        if st.button('Marcar'):
            for inventory in inventories:
                if inventory['brand'] == brand and inventory['warehouse'] == warehouse:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} dispositivos de {brand} marcados para {warehouse}')
    
    elif action == 'Reservar productos':
        brand = st.selectbox('Selecciona la marca', ['BrandA', 'BrandB'])
        quantity = st.number_input('Cantidad de dispositivos a reservar', min_value=0)
        project = st.text_input('Nombre del proyecto de automatización')
        
        if st.button('Reservar'):
            for inventory in inventories:
                if inventory['brand'] == brand:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} dispositivos de {brand} reservados para el proyecto {project}')
    
    elif action == 'Buscar especificaciones':
        brand = st.selectbox('Selecciona la marca', ['BrandA', 'BrandB'])
        
        if st.button('Buscar'):
            st.write(f'Especificaciones para {brand}: (Detalles ficticios)')
    
    elif action == 'Auditar inventario':
        warehouse = st.selectbox('Selecciona la bodega para auditar', ['Warehouse1', 'Warehouse2'])
        
        if st.button('Auditar'):
            for inventory in inventories:
                if inventory['warehouse'] == warehouse:
                    st.write(f'{inventory["quantity"]} dispositivos de {inventory["brand"]} en {warehouse}')

# Función de seguimiento de horas trabajadas
def track_work_hours():
    st.header('Seguimiento de Horas Trabajadas')
    
    user = st.selectbox('Selecciona el técnico', [user['name'] for user in users])
    action = st.selectbox('Selecciona una acción', ['Inicio de jornada', 'Llegada a proyecto', 'Toma de descansos', 'Salida de proyecto', 'Fin de jornada'])
    
    if st.button('Registrar'):
        selected_user = next((u for u in users if u['name'] == user), None)
        if selected_user:
            timestamp = dt.datetime.now(tz=pytz.timezone('UTC')).isoformat()
            selected_user['working_hours'].append({'action': action, 'timestamp': timestamp})
            st.write(f'{action} registrado para {user} a las {timestamp}')
            
            if action == 'Fin de jornada':
                st.write(f'Se ha enviado un correo con la hoja de tiempos de {user}')
                # Simulación de envío de correo
                st.write(f'Correo enviado a: admin@hootsi.com')

# Opciones de la interfaz
st.sidebar.title("Options")
option = st.sidebar.selectbox(
    'Select an action:',
    ('Check-In Notification', 'Clock-Out Notification', 'Seguimiento de Inventario', 'Seguimiento de Horas Trabajadas')
)

if option == 'Check-In Notification':
    notificate_check_in()
elif option == 'Clock-Out Notification':
    notificate_clock_out()
elif option == 'Seguimiento de Inventario':
    track_inventory()
elif option == 'Seguimiento de Horas Trabajadas':
    track_work_hours()
