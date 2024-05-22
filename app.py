import streamlit as st
import datetime as dt
import pytz
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from io import BytesIO

# Generar datos de inventario simulados
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'BrandF', 'BrandG', 'BrandH', 'BrandI', 'BrandJ', 
          'BrandK', 'BrandL', 'BrandM', 'BrandN', 'BrandO', 'BrandP', 'BrandQ', 'BrandR', 'BrandS', 'BrandT']
categories = ['Tecnología', 'Comunicaciones', 'Vehículos', 'Electrodomésticos', 'Muebles', 'Ropa', 'Juguetes', 'Libros']
warehouses = ['Warehouse' + str(i) for i in range(1, 21)]
us_cities = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
    "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
    "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC"
]

# Generar datos históricos
dates = pd.date_range(start='2018-01-01', end='2023-12-01', freq='MS')
data = []
for brand in brands:
    category = random.choice(categories)
    for warehouse, city in zip(warehouses, us_cities):
        for date in dates:
            quantity = random.randint(50, 200)
            data.append([date, brand, category, warehouse, city, quantity])

inventory_df = pd.DataFrame(data, columns=['Date', 'Brand', 'Category', 'Warehouse', 'City', 'Quantity'])

# Traducción
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
        "clock_out_time": "Hora de clock-out",
        "total_hours_worked": "Total de horas trabajadas",
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
        "data_saved": "Datos guardados",
        "download_pdf": "Descargar Dashboard en PDF"
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
        "data_saved": "Data saved",
        "download_pdf": "Download Dashboard as PDF"
    }
}

# Selección de idioma
st.markdown("<h1 style='text-align: center;'>Options</h1>", unsafe_allow_html=True)
lang = st.selectbox("", ["es", "en"], index=0)

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
def notificate_check_in():
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

def notificate_clock_out():
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
def configure_notifications():
    st.header(t['configure_notifications'])

    notification_type = st.selectbox(t['select_action'], [t['inventory_below_threshold'], t['break_time_exceeded']])
    threshold = st.number_input(t['threshold'], min_value=0, value=10)
    email = st.text_input(t['email'])

    if st.button(t['save_settings']):
        st.success(t['settings_saved'])
        # Aquí se guardaría la configuración en una base de datos o archivo

# Función de dashboard de reportes
def dashboard():
    st.header(t['dashboard'])

    # KPI
    st.subheader("KPIs")
    total_inventory = inventory_df['Quantity'].sum()
    avg_inventory = inventory_df.groupby('Brand')['Quantity'].mean().mean()
    max_inventory = inventory_df.groupby('Brand')['Quantity'].sum().max()

    st.metric(label="Total Inventory", value=f"{total_inventory}")
    st.metric(label="Average Inventory per Brand", value=f"{avg_inventory:.2f}")
    st.metric(label="Maximum Inventory by Brand", value=f"{max_inventory}")

    # Gráficos de Check-In y Clock-Out
    if check_in_records or clock_out_records:
        st.subheader("Check-In and Clock-Out Records")
        check_in_df = pd.DataFrame(check_in_records)
        clock_out_df = pd.DataFrame(clock_out_records)

        if not check_in_df.empty:
            st.write("Check-In Records")
            st.table(check_in_df)
            st.line_chart(check_in_df['time'])

        if not clock_out_df.empty:
            st.write("Clock-Out Records")
            st.table(clock_out_df)
            st.line_chart(clock_out_df['time'])

    # Gráficos de horas trabajadas
    if work_hours_records:
        st.subheader("Work Hours Records")
        work_hours_df = pd.DataFrame(work_hours_records)
        st.table(work_hours_df)
        st.line_chart(work_hours_df['timestamp'])

    # Gráficos de gestión de proyectos
    if project_management_records:
        st.subheader("Project Management Records")
        project_management_df = pd.DataFrame(project_management_records)
        st.table(project_management_df)
        st.line_chart(project_management_df['due_date'])

    # Ejemplo de gráficos de inventario
    st.subheader("Inventory Records")
    df = inventory_df
    brand_counts = df.groupby('Brand')['Quantity'].sum().reset_index()
    warehouse_counts = df.groupby('Warehouse')['Quantity'].sum().reset_index()

    fig1 = px.bar(brand_counts, x='Brand', y='Quantity', title=t['inventory_by_brand'])
    fig2 = px.bar(warehouse_counts, x='Warehouse', y='Quantity', title=t['inventory_by_warehouse'])

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    # Botón para descargar en PDF
    if st.button(t['download_pdf']):
        download_pdf()

# Función de análisis predictivo
def predict_inventory():
    st.header(t['predict_inventory'])

    selected_brand = st.selectbox(t['select_brand'], brands)
    selected_warehouse = st.selectbox(t['select_warehouse'], warehouses)
    prediction_days = st.selectbox("Select prediction period (days)", [30, 60, 90, 120])

    # Filtrar datos históricos por marca y bodega
    historical_data = inventory_df[(inventory_df['Brand'] == selected_brand) & (inventory_df['Warehouse'] == selected_warehouse)]

    if historical_data.empty:
        st.write(t['no_data_available'])
    else:
        df = historical_data
        df['Day'] = (df['Date'] - df['Date'].min()).dt.days
        X = df['Day'].values.reshape(-1, 1)
        y = df['Quantity'].values

        model = LinearRegression()
        model.fit(X, y)

        future_days = np.array(range(df['Day'].max() + 1, df['Day'].max() + 1 + prediction_days)).reshape(-1, 1)
        predicted_quantities = model.predict(future_days)

        prediction_dates = pd.date_range(start=df['Date'].max() + pd.Timedelta(days=1), periods=prediction_days, freq='D')
        prediction_df = pd.DataFrame({'Date': prediction_dates, 'Predicted Quantity': predicted_quantities})

        st.write(t['predictions_for_inventory'])
        fig = px.line(prediction_df, x='Date', y='Predicted Quantity', title=f'Predicted Inventory for {selected_brand} in {selected_warehouse}')
        st.plotly_chart(fig)

# Función de gestión de proyectos
def project_management():
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
def track_inventory():
    st.header(t['inventory_tracking'])

    action = st.selectbox(t['select_action'], [t['view_inventory'], t['mark_items'], t['reserve_products'], t['search_specifications'], t['audit_inventory']])

    if action == t['view_inventory']:
        st.write(t['inventory_available'])

        # Filtros para los gráficos
        selected_brand = st.selectbox(t['select_brand'], brands)
        selected_warehouse = st.selectbox(t['select_warehouse'], warehouses)

        df = inventory_df

        if selected_brand:
            df = df[df['Brand'] == selected_brand]
        if selected_warehouse:
            df = df[df['Warehouse'] == selected_warehouse]

        if df.empty:
            st.write(t['no_data_available'])
        else:
            brand_counts = df.groupby('Brand')['Quantity'].sum()
            warehouse_counts = df.groupby('Warehouse')['Quantity'].sum()

            fig1 = px.bar(brand_counts.reset_index(), x='Brand', y='Quantity', title=t['inventory_by_brand'])
            fig2 = px.bar(warehouse_counts.reset_index(), x='Warehouse', y='Quantity', title=t['inventory_by_warehouse'])

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

            fig = px.bar(brand_counts.reset_index(), x='brand', y='quantity', title=f"{t['inventory_by_warehouse']} {warehouse}")
            st.plotly_chart(fig)

# Función de seguimiento de horas trabajadas
def track_work_hours():
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

# Opciones de la interfaz
option = option_menu(
    menu_title=None,
    options=[
        t['check_in_notification'], 
        t['clock_out_notification'], 
        t['inventory_tracking'], 
        t['work_hours_tracking'], 
        t['configure_notifications'], 
        t['dashboard'], 
        t['predict_inventory'], 
        t['project_management']
    ],
    icons=["box-arrow-in-right", "box-arrow-left", "list-task", "clock", "gear", "bar-chart", "graph-up", "clipboard"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if option == t['check_in_notification']:
    notificate_check_in()
elif option == t['clock_out_notification']:
    notificate_clock_out()
elif option == t['inventory_tracking']:
    track_inventory()
elif option == t['work_hours_tracking']:
    track_work_hours()
elif option == t['configure_notifications']:
    configure_notifications()
elif option == t['dashboard']:
    dashboard()
elif option == t['predict_inventory']:
    predict_inventory()
elif option == t['project_management']:
    project_management()

def download_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size = 12)
    
    pdf.cell(200, 10, txt = t['title'], ln = True, align = 'C')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='pdf')
    buffer.seek(0)
    
    pdf.output(buffer)
    
    st.download_button(
        label=t['download_pdf'],
        data=buffer,
        file_name="dashboard_report.pdf",
        mime="application/pdf"
    )



