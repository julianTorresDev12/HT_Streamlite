import streamlit as st
import datetime as dt
import pytz
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from streamlit_option_menu import option_menu

# Generar datos de inventario simulados
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
warehouses = ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4', 'Warehouse5']

inventories = [{"id": i, "brand": random.choice(brands), "warehouse": random.choice(warehouses), "quantity": random.randint(50, 200)} for i in range(1, 201)]

work_hours_records = []
check_in_records = []
clock_out_records = []
project_management_records = []

# 20 ciudades más importantes de EE.UU.
us_cities = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
    "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
    "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC"
]

# Roles y cargos
roles = {
    "Administrative": ["CEO", "CFO", "COO", "VP of Operations", "Administrative Manager", "Office Assistant", "HR Manager", "Accountant", "Marketing Manager", "Analyst"],
    "IT Team": ["VP of IT", "IT Manager", "Network Administrator", "System Administrator", "Database Administrator", "Software Engineer", "Developer"],
    "Logistics Team": ["Logistics Manager", "Warehouse Supervisor", "Inventory Specialist", "Forklift Operator", "Shipping and Receiving Clerk"]
}

# Diccionario para soporte bilingüe con especificaciones
translations = {
    "es": {
        "title": "Aplicación Hootsi",
        "check_in_notification": "Notificación de Check-In",
        "clock_out_notification": "Notificación de Check-Out",
        "inventory_tracking": "Seguimiento de Inventario",
        "work_hours_tracking": "Seguimiento de Horas Trabajadas",
        "view_inventory": "Ver inventario",
        "mark_items": "Marcar elementos",
        "reserve_products": "Reservar productos",
        "search_specifications": "Buscar especificaciones",
        "audit_inventory": "Auditar inventario",
        "select_action": "Selecciona una acción",
        "select_technician": "Selecciona un rol/cargo",
        "register": "Registrar",
        "inventory_available": "Inventario disponible",
        "devices_of": "dispositivos de",
        "marked_for": "marcados para",
        "reserved_for_project": "reservados para el proyecto",
        "specifications_for": "Especificaciones para",
        "inventory_in": "dispositivos en",
        "hours_tracking": "Seguimiento de Horas Trabajadas",
        "action": "acción",
        "registered_for": "registrado para",
        "sent_email_with_timesheet": "Se ha enviado un correo con la hoja de tiempos de",
        "email_sent_to": "Correo enviado a",
        "options": "Opciones",
        "select_language": "Selecciona un idioma",
        "spanish": "Español",
        "english": "Inglés",
        "select_warehouse": "Selecciona la bodega",
        "select_brand": "Selecciona la marca",
        "no_data_available": "No hay datos disponibles",
        "name": "Nombre",
        "role": "Cargo",
        "activity": "Actividad a realizar",
        "location": "Ubicación",
        "submit": "Enviar",
        "check_in_time": "Hora de check-in",
        "clock_out_time": "Hora de check-out",
        "total_hours_worked": "Total de horas trabajadas",
        "brand_specifications": {
            "BrandA": "BrandA es conocida por su durabilidad y eficiencia. Especificaciones: 8GB RAM, 256GB SSD, Procesador Intel i5.",
            "BrandB": "BrandB ofrece una excelente relación calidad-precio. Especificaciones: 4GB RAM, 128GB SSD, Procesador Intel i3.",
            "BrandC": "BrandC es famosa por su diseño elegante. Especificaciones: 16GB RAM, 512GB SSD, Procesador Intel i7.",
            "BrandD": "BrandD tiene productos de alta gama. Especificaciones: 32GB RAM, 1TB SSD, Procesador Intel i9.",
            "BrandE": "BrandE es conocida por su accesibilidad. Especificaciones: 2GB RAM, 64GB SSD, Procesador Intel Pentium."
        },
        "work_actions": ["Inicio de jornada", "Llegada a proyecto", "Toma de descansos", "Salida de proyecto", "Fin de jornada"],
        "configure_notifications": "Configurar Notificaciones Personalizadas",
        "inventory_below_threshold": "Inventario bajo el umbral",
        "break_time_exceeded": "Tiempo de descanso excedido",
        "threshold": "Umbral",
        "email": "Correo Electrónico",
        "save_settings": "Guardar Configuración",
        "settings_saved": "Configuración de notificación guardada",
        "dashboard": "Dashboard de Reportes",
        "predict_inventory": "Análisis Predictivo de Inventario",
        "project_management": "Gestión de Proyectos",
        "real_time_geolocation": "Geolocalización en Tiempo Real",
        "task_description": "Descripción de la Tarea",
        "due_date": "Fecha de Vencimiento",
        "assign_task": "Asignar Tarea",
        "task_assigned": "Tarea asignada",
        "predictions_for_inventory": "Predicciones de Inventario para los próximos días",
        "location": "Ubicación",
        "current_location": "Ubicación actual",
        "inventory_by_brand": "Inventario por Marca",
        "inventory_by_warehouse": "Inventario por Bodega",
        "data_saved": "Datos guardados"
    },
    "en": {
        "title": "Hootsi Application",
        "check_in_notification": "Check-In Notification",
        "clock_out_notification": "Clock-Out Notification",
        "inventory_tracking": "Inventory Tracking",
        "work_hours_tracking": "Work Hours Tracking",
        "view_inventory": "View Inventory",
        "mark_items": "Mark Items",
        "reserve_products": "Reserve Products",
        "search_specifications": "Search Specifications",
        "audit_inventory": "Audit Inventory",
        "select_action": "Select an action",
        "select_technician": "Select a role/position",
        "register": "Register",
        "inventory_available": "Inventory available",
        "devices_of": "devices of",
        "marked_for": "marked for",
        "reserved_for_project": "reserved for the project",
        "specifications_for": "Specifications for",
        "inventory_in": "devices in",
        "hours_tracking": "Work Hours Tracking",
        "action": "action",
        "registered_for": "registered for",
        "sent_email_with_timesheet": "An email with the timesheet has been sent for",
        "email_sent_to": "Email sent to",
        "options": "Options",
        "select_language": "Select a language",
        "spanish": "Spanish",
        "english": "English",
        "select_warehouse": "Select the warehouse",
        "select_brand": "Select the brand",
        "no_data_available": "No data available",
        "name": "Name",
        "role": "Role",
        "activity": "Activity to perform",
        "location": "Location",
        "submit": "Submit",
        "check_in_time": "Check-in time",
        "clock_out_time": "Clock-out time",
        "total_hours_worked": "Total hours worked",
        "brand_specifications": {
            "BrandA": "BrandA is known for its durability and efficiency. Specifications: 8GB RAM, 256GB SSD, Intel i5 Processor.",
            "BrandB": "BrandB offers excellent value for money. Specifications: 4GB RAM, 128GB SSD, Intel i3 Processor.",
            "BrandC": "BrandC is famous for its sleek design. Specifications: 16GB RAM, 512GB SSD, Intel i7 Processor.",
            "BrandD": "BrandD has high-end products. Specifications: 32GB RAM, 1TB SSD, Intel i9 Processor.",
            "BrandE": "BrandE is known for its accessibility. Specifications: 2GB RAM, 64GB SSD, Intel Pentium Processor."
        },
        "work_actions": ["Start of workday", "Arrival at project", "Break", "Leaving project", "End of workday"],
        "configure_notifications": "Configure Custom Notifications",
        "inventory_below_threshold": "Inventory Below Threshold",
        "break_time_exceeded": "Break Time Exceeded",
        "threshold": "Threshold",
        "email": "Email",
        "save_settings": "Save Settings",
        "settings_saved": "Notification settings saved",
        "dashboard": "Reports Dashboard",
        "predict_inventory": "Predictive Inventory Analysis",
        "project_management": "Project Management",
        "real_time_geolocation": "Real-Time Geolocation",
        "task_description": "Task Description",
        "due_date": "Due Date",
        "assign_task": "Assign Task",
        "task_assigned": "Task assigned",
        "predictions_for_inventory": "Predictions for Inventory for the coming days",
        "location": "Location",
        "current_location": "Current Location",
        "inventory_by_brand": "Inventory by Brand",
        "inventory_by_warehouse": "Inventory by Warehouse",
        "data_saved": "Data saved"
    }
}

# Opciones de la interfaz
st.sidebar.title("Options")
lang = st.sidebar.selectbox("Select a language", ["es", "en"])

t = translations[lang]

st.title(t['title'])  # Aseguramos que el título esté siempre en la parte superior

# Variables globales para almacenar horas de check-in y check-out
check_in_times = {}
check_out_times = {}

# Función para obtener la geolocalización de una ciudad
def get_city_location(city):
    # Coordenadas de ejemplo para las 20 ciudades
    locations = {
        "New York, NY": {"latitude": 40.7128, "longitude": -74.0060},
        "Los Angeles, CA": {"latitude": 34.0522, "longitude": -118.2437},
        "Chicago, IL": {"latitude": 41.8781, "longitude": -87.6298},
        "Houston, TX": {"latitude": 29.7604, "longitude": -95.3698},
        "Phoenix, AZ": {"latitude": 33.4484, "longitude": -112.0740},
        "Philadelphia, PA": {"latitude": 39.9526, "longitude": -75.1652},
        "San Antonio, TX": {"latitude": 29.4241, "longitude": -98.4936},
        "San Diego, CA": {"latitude": 32.7157, "longitude": -117.1611},
        "Dallas, TX": {"latitude": 32.7767, "longitude": -96.7970},
        "San Jose, CA": {"latitude": 37.3382, "longitude": -121.8863},
        "Austin, TX": {"latitude": 30.2672, "longitude": -97.7431},
        "Jacksonville, FL": {"latitude": 30.3322, "longitude": -81.6557},
        "Fort Worth, TX": {"latitude": 32.7555, "longitude": -97.3308},
        "Columbus, OH": {"latitude": 39.9612, "longitude": -82.9988},
        "Charlotte, NC": {"latitude": 35.2271, "longitude": -80.8431},
        "San Francisco, CA": {"latitude": 37.7749, "longitude": -122.4194},
        "Indianapolis, IN": {"latitude": 39.7684, "longitude": -86.1581},
        "Seattle, WA": {"latitude": 47.6062, "longitude": -122.3321},
        "Denver, CO": {"latitude": 39.7392, "longitude": -104.9903},
        "Washington, DC": {"latitude": 38.9072, "longitude": -77.0369}
    }
    return locations.get(city, {"latitude": 0.0, "longitude": 0.0})

# Definir las funciones de notificación
def notificate_check_in(lang):
    t = translations[lang]
    st.header(t['check_in_notification'])

    name = st.text_input(t['name'])
    role = st.text_input(t['role'])
    activity = st.text_input(t['activity'])
    city = st.selectbox(t['location'], us_cities)
    location = get_city_location(city)

    if st.button(t['submit']):
        check_in_time = dt.datetime.now(tz=pytz.timezone('UTC'))
        check_in_times[name] = check_in_time
        check_in_records.append({"name": name, "role": role, "activity": activity, "city": city, "location": location, "time": check_in_time})
        st.write(f"{t['name']}: {name}")
        st.write(f"{t['role']}: {role}")
        st.write(f"{t['activity']}: {activity}")
        st.write(f"{t['location']}: {city} ({location['latitude']}, {location['longitude']})")
        st.write(f"{t['check_in_time']}: {check_in_time.isoformat()}")
        st.map(pd.DataFrame({'lat': [location['latitude']], 'lon': [location['longitude']]}))

def notificate_clock_out(lang):
    t = translations[lang]
    st.header(t['clock_out_notification'])

    name = st.text_input(t['name'])
    role = st.text_input(t['role'])
    activity = st.text_input(t['activity'])
    city = st.selectbox(t['location'], us_cities)
    location = get_city_location(city)

    if st.button(t['submit']):
        check_out_time = dt.datetime.now(tz=pytz.timezone('UTC'))
        check_out_times[name] = check_out_time
        clock_out_records.append({"name": name, "role": role, "activity": activity, "city": city, "location": location, "time": check_out_time})
        st.write(f"{t['name']}: {name}")
        st.write(f"{t['role']}: {role}")
        st.write(f"{t['activity']}: {activity}")
        st.write(f"{t['location']}: {city} ({location['latitude']}, {location['longitude']})")
        st.write(f"{t['clock_out_time']}: {check_out_time.isoformat()}")
        st.map(pd.DataFrame({'lat': [location['latitude']], 'lon': [location['longitude']]}))

        if name in check_in_times:
            total_hours = (check_out_time - check_in_times[name]).total_seconds() / 3600
            st.write(f"{t['total_hours_worked']}: {total_hours:.2f} horas")

# Función de configuración de notificaciones personalizadas
def configure_notifications(lang):
    t = translations[lang]
    st.header(t['configure_notifications'])

    notification_type = st.selectbox(t['select_action'], [t['inventory_below_threshold'], t['break_time_exceeded']])
    threshold = st.number_input(t['threshold'], min_value=0, value=10)
    email = st.text_input(t['email'])

    if st.button(t['save_settings']):
        st.success(t['settings_saved'])
        # Aquí se guardaría la configuración en una base de datos o archivo

# Función de dashboard de reportes
def dashboard(lang):
    t = translations[lang]
    st.header(t['dashboard'])

    # Gráficos de Check-In y Clock-Out
    if check_in_records or clock_out_records:
        st.subheader("Check-In and Clock-Out Records")
        check_in_df = pd.DataFrame(check_in_records)
        clock_out_df = pd.DataFrame(clock_out_records)

        if not check_in_df.empty:
            st.write("Check-In Records")
            st.table(check_in_df)
            fig1 = px.line(check_in_df, x='time', y='name', title='Check-In Times')
            st.plotly_chart(fig1)

        if not clock_out_df.empty:
            st.write("Clock-Out Records")
            st.table(clock_out_df)
            fig2 = px.line(clock_out_df, x='time', y='name', title='Clock-Out Times')
            st.plotly_chart(fig2)

    # Gráficos de horas trabajadas
    if work_hours_records:
        st.subheader("Work Hours Records")
        work_hours_df = pd.DataFrame(work_hours_records)
        st.table(work_hours_df)
        fig3 = px.line(work_hours_df, x='timestamp', y='name', title='Work Hours Tracking')
        st.plotly_chart(fig3)

    # Gráficos de gestión de proyectos
    if project_management_records:
        st.subheader("Project Management Records")
        project_management_df = pd.DataFrame(project_management_records)
        st.table(project_management_df)
        fig4 = px.line(project_management_df, x='due_date', y='project_name', title='Project Management Tracking')
        st.plotly_chart(fig4)

    # Ejemplo de gráficos de inventario
    st.subheader("Inventory Records")
    df = pd.DataFrame(inventories)
    brand_counts = df.groupby('brand')['quantity'].sum()
    warehouse_counts = df.groupby('warehouse')['quantity'].sum()

    fig5 = px.bar(brand_counts, x=brand_counts.index, y='quantity', title=t['inventory_by_brand'])
    fig6 = px.bar(warehouse_counts, x=warehouse_counts.index, y='quantity', title=t['inventory_by_warehouse'])

    st.plotly_chart(fig5)
    st.plotly_chart(fig6)

# Función de análisis predictivo
def predict_inventory(lang):
    t = translations[lang]
    st.header(t['predict_inventory'])

    selected_brand = st.selectbox(t['select_brand'], brands)
    selected_warehouse = st.selectbox(t['select_warehouse'], warehouses)
    prediction_days = st.selectbox("Select prediction period (days)", [30, 60, 90, 120])

    # Filtrar datos históricos por marca y bodega
    historical_data = [inv for inv in inventories if inv['brand'] == selected_brand and inv['warehouse'] == selected_warehouse]

    if not historical_data:
        st.write(t['no_data_available'])
    else:
        df = pd.DataFrame(historical_data)
        df['day'] = range(1, len(df) + 1)  # Asumimos un día por cada registro
        X = df['day'].values.reshape(-1, 1)
        y = df['quantity'].values

        model = LinearRegression()
        model.fit(X, y)

        future_days = np.array(range(len(df) + 1, len(df) + 1 + prediction_days)).reshape(-1, 1)
        predicted_quantities = model.predict(future_days)

        st.write(t['predictions_for_inventory'])
        fig = px.line(x=future_days.flatten(), y=predicted_quantities, title="Inventory Prediction")
        st.plotly_chart(fig)

# Función de gestión de proyectos
def project_management(lang):
    t = translations[lang]
    st.header(t['project_management'])

    project_name = st.text_input(t['name'])
    role_category = st.selectbox(t['select_action'], list(roles.keys()))
    role = st.selectbox(t['select_technician'], roles[role_category])
    task_description = st.text_area(t['task_description'])
    due_date = st.date_input(t['due_date'])

    if st.button(t['assign_task']):
        project_management_records.append({"project_name": project_name, "role": role, "task_description": task_description, "due_date": due_date})
        st.success(t['task_assigned'])
        # Aquí se guardaría la tarea en una base de datos o archivo

# Función de seguimiento de inventario
def track_inventory(lang):
    t = translations[lang]
    st.header(t['inventory_tracking'])

    action = st.selectbox(t['select_action'], [t['view_inventory'], t['mark_items'], t['reserve_products'], t['search_specifications'], t['audit_inventory']])

    if action == t['view_inventory']:
        st.write(t['inventory_available'])

        # Filtros para los gráficos
        selected_brand = st.selectbox(t['select_brand'], brands)
        selected_warehouse = st.selectbox(t['select_warehouse'], warehouses)

        df = pd.DataFrame(inventories)

        if selected_brand:
            df = df[df['brand'] == selected_brand]
        if selected_warehouse:
            df = df[df['warehouse'] == selected_warehouse]

        if df.empty:
            st.write(t['no_data_available'])
        else:
            brand_counts = df.groupby('brand')['quantity'].sum()
            warehouse_counts = df.groupby('warehouse')['quantity'].sum()

            fig1 = px.bar(brand_counts, x=brand_counts.index, y='quantity', title=t['inventory_by_brand'])
            fig2 = px.bar(warehouse_counts, x=warehouse_counts.index, y='quantity', title=t['inventory_by_warehouse'])

            st.plotly_chart(fig1)
            st.plotly_chart(fig2)

    elif action == t['mark_items']:
        brand = st.selectbox(t['select_brand'], brands)
        quantity = st.number_input('Quantity to mark', min_value=0)
        warehouse = st.selectbox(t['select_warehouse'], warehouses)

        if st.button(t['register']):
            for inventory in inventories:
                if inventory['brand'] == brand and inventory['warehouse'] == warehouse:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} {t["devices_of"]} {brand} {t["marked_for"]} {warehouse}')
                    break  # Ensure it only happens once

    elif action == t['reserve_products']:
        brand = st.selectbox(t['select_brand'], brands)
        quantity = st.number_input('Quantity to reserve', min_value=0)
        project = st.text_input('Project name')

        if st.button(t['register']):
            for inventory in inventories:
                if inventory['brand'] == brand:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} {t["devices_of"]} {brand} {t["reserved_for_project"]} {project}')
                    break  # Ensure it only happens once

    elif action == t['search_specifications']:
        brand = st.selectbox(t['select_brand'], brands)

        if st.button(t['register']):
            st.write(f'{t["specifications_for"]} {brand}: {t["brand_specifications"][brand]}')

    elif action == t['audit_inventory']:
        warehouse = st.selectbox(t['select_warehouse'], warehouses)

        filtered_inventories = [inv for inv in inventories if inv['warehouse'] == warehouse]

        if not filtered_inventories:
            st.write(t['no_data_available'])
        else:
            df = pd.DataFrame(filtered_inventories)
            brand_counts = df.groupby('brand')['quantity'].sum()

            fig = px.bar(brand_counts, x=brand_counts.index, y='quantity', title=f"{t['inventory_by_warehouse']} {warehouse}")
            st.plotly_chart(fig)

# Función de seguimiento de horas trabajadas
def track_work_hours(lang):
    t = translations[lang]
    st.header(t['work_hours_tracking'])

    name = st.text_input(t['name'])
    role_category = st.selectbox(t['select_action'], list(roles.keys()))
    role = st.selectbox(t['select_technician'], roles[role_category])
    action = st.selectbox(t['select_action'], t['work_actions'])
    city = st.selectbox(t['location'], us_cities)
    location = get_city_location(city)

    if st.button(t['register']):
        timestamp = dt.datetime.now(tz=pytz.timezone('UTC')).isoformat()
        work_hours_records.append({"name": name, "role": role, "action": action, "timestamp": timestamp, "city": city, "location": location})
        st.write(f'{action} {t["registered_for"]} {role} a las {timestamp}')
        st.write(f"{t['location']}: {city} ({location['latitude']}, {location['longitude']})")
        st.map(pd.DataFrame({'lat': [location['latitude']], 'lon': [location['longitude']]}))

        if action == t['work_actions'][-1]:  # If action is 'Fin de jornada' or 'End of workday'
            st.write(f'{t["sent_email_with_timesheet"]} {role}')
            st.write(f'{t["email_sent_to"]}: julian.torres@ahtglobal.com')

option = option_menu(
    menu_title=t['select_action'],
    options=[t['check_in_notification'], t['clock_out_notification'], t['inventory_tracking'], t['work_hours_tracking'], t['configure_notifications'], t['dashboard'], t['predict_inventory'], t['project_management']],
    icons=["check", "clock", "box", "clock", "bell", "bar-chart", "chart-line", "project-diagram"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if option == t['check_in_notification']:
    notificate_check_in(lang)
elif option == t['clock_out_notification']:
    notificate_clock_out(lang)
elif option == t['inventory_tracking']:
    track_inventory(lang)
elif option == t['work_hours_tracking']:
    track_work_hours(lang)
elif option == t['configure_notifications']:
    configure_notifications(lang)
elif option == t['dashboard']:
    dashboard(lang)
elif option == t['predict_inventory']:
    predict_inventory(lang)
elif option == t['project_management']:
    project_management(lang)
