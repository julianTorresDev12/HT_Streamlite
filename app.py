import streamlit as st
import datetime as dt
import pytz
import holidays
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd

# Generar datos de inventario simulados
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
warehouses = ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4', 'Warehouse5']

inventories = [{"id": i, "brand": random.choice(brands), "warehouse": random.choice(warehouses), "quantity": random.randint(50, 200)} for i in range(1, 201)]

users = [
    {"id": 1, "name": "TechnicianA", "warehouse_id": 1, "projects": [], "working_hours": []},
    {"id": 2, "name": "TechnicianB", "warehouse_id": 2, "projects": [], "working_hours": []},
]

# Diccionario para soporte bilingüe
translations = {
    "es": {
        "title": "Aplicación Hootsi",
        "check_in_notification": "Notificación de Check-In",
        "clock_out_notification": "Notificación de Clock-Out",
        "inventory_tracking": "Seguimiento de Inventario",
        "work_hours_tracking": "Seguimiento de Horas Trabajadas",
        "view_inventory": "Ver inventario",
        "mark_items": "Marcar elementos",
        "reserve_products": "Reservar productos",
        "search_specifications": "Buscar especificaciones",
        "audit_inventory": "Auditar inventario",
        "select_action": "Selecciona una acción",
        "select_technician": "Selecciona el técnico",
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
        "no_data_available": "No hay datos disponibles"
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
        "select_technician": "Select a technician",
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
        "no_data_available": "No data available"
    }
}

# Opciones de la interfaz
st.sidebar.title("Options")
lang = st.sidebar.selectbox("Select a language", ["es", "en"])

t = translations[lang]

st.title(t['title'])  # Aseguramos que el título esté siempre en la parte superior

# Definir las funciones de notificación
def notificate_check_in(lang):
    email_service = "model_postmark"  # Placeholder
    us_holidays = holidays.US()
    today_date = dt.datetime.now(tz=pytz.timezone('UTC'))

    users = [{"id": 315, "project_id": None, "time_zone": "America/New_York", "is_clocked_in": 0, "email": "julian.torres@ahtglobal.com", "first_name": "User", "warehouse_id": 1, "tenant_id": 1}]

    if today_date not in us_holidays:
        for user in users:
            if user['id'] == 315 and user['project_id'] is None:
                user_tz = pytz.timezone(user['time_zone'])
                utc_now = dt.datetime.now(tz=pytz.timezone('UTC'))
                user_now = utc_now.astimezone(user_tz)

                if user_now.hour == 8 and user['is_clocked_in'] != 1:  # Recordatorio de clock in
                    st.write(f"Sending reminder email to: {user['email']}")
                    st.write("Hootsi would like to remind you to clock in and then check in for your project today.")

def notificate_clock_out(lang):
    email_service = "model_postmark"  # Placeholder
    us_holidays = holidays.US()
    today_date = dt.datetime.now(tz=pytz.timezone('UTC'))

    users = [{"id": 315, "is_clocked_in": 1, "time_zone": "America/New_York", "email": "julian.torres@ahtglobal.com", "first_name": "User", "warehouse_id": 1, "tenant_id": 1}]

    if today_date not in us_holidays:
        for user in users:
            if user['id'] == 315 and user['is_clocked_in'] == 1:  # Recordatorio de clock out
                user_tz = pytz.timezone(user['time_zone'])
                utc_now = dt.datetime.now()
                user_now = utc_now.astimezone(user_tz)
                if user_now.hour == 20 or True:
                    st.write(f"Sending reminder email to: {user['email']}")
                    st.write("Hootsi would like to remind you to clock out for the day.")

# Función de seguimiento de inventario
def track_inventory(lang):
    t = translations[lang]
    st.header(t['inventory_tracking'])
    
    action = st.selectbox(t['select_action'], [t['view_inventory'], t['mark_items'], t['reserve_products'], t['search_specifications'], t['audit_inventory']])
    
    if action == t['view_inventory']:
        st.write(t['inventory_available'])
        for inventory in inventories:
            st.write(f"{inventory['quantity']} {t['devices_of']} {inventory['brand']} {t['inventory_in']} {inventory['warehouse']}")
        
        # Graficar inventario por marca
        df = pd.DataFrame(inventories)
        brand_counts = df.groupby('brand')['quantity'].sum()
        warehouse_counts = df.groupby('warehouse')['quantity'].sum()

        fig1, ax1 = plt.subplots()
        brand_counts.plot(kind='bar', ax=ax1)
        ax1.set_title("Inventory by Brand")
        ax1.set_xlabel("Brand")
        ax1.set_ylabel("Quantity")

        fig2, ax2 = plt.subplots()
        warehouse_counts.plot(kind='bar', ax=ax2)
        ax2.set_title("Inventory by Warehouse")
        ax2.set_xlabel("Warehouse")
        ax2.set_ylabel("Quantity")

        st.pyplot(fig1)
        st.pyplot(fig2)
    
    elif action == t['mark_items']:
        brand = st.selectbox('Select brand', ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE'])
        quantity = st.number_input('Quantity to mark', min_value=0)
        warehouse = st.selectbox('Select warehouse', ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4', 'Warehouse5'])
        
        if st.button(t['register']):
            for inventory in inventories:
                if inventory['brand'] == brand and inventory['warehouse'] == warehouse:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} {t["devices_of"]} {brand} {t["marked_for"]} {warehouse}')
                    break  # Ensure it only happens once
    
    elif action == t['reserve_products']:
        brand = st.selectbox('Select brand', ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE'])
        quantity = st.number_input('Quantity to reserve', min_value=0)
        project = st.text_input('Project name')
        
        if st.button(t['register']):
            for inventory in inventories:
                if inventory['brand'] == brand:
                    inventory['quantity'] -= quantity
                    st.write(f'{quantity} {t["devices_of"]} {brand} {t["reserved_for_project"]} {project}')
                    break  # Ensure it only happens once
    
    elif action == t['search_specifications']:
        brand = st.selectbox('Select brand', ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE'])
        
        if st.button(t['register']):
            st.write(f'{t["specifications_for"]} {brand}: (Detalles ficticios)')
    
    elif action == t['audit_inventory']:
        warehouse = st.selectbox(t['select_warehouse'], ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4', 'Warehouse5'])
        
        filtered_inventories = [inv for inv in inventories if inv['warehouse'] == warehouse]

        if not filtered_inventories:
            st.write(t['no_data_available'])
        else:
            df = pd.DataFrame(filtered_inventories)
            brand_counts = df.groupby('brand')['quantity'].sum()

            fig, ax = plt.subplots()
            brand_counts.plot(kind='bar', ax=ax)
            ax.set_title(f"Inventory Audit for {warehouse}")
            ax.set_xlabel("Brand")
            ax.set_ylabel("Quantity")

            st.pyplot(fig)

# Función de seguimiento de horas trabajadas
def track_work_hours(lang):
    t = translations[lang]
    st.header(t['work_hours_tracking'])
    
    user = st.selectbox(t['select_technician'], [user['name'] for user in users])
    action = st.selectbox(t['select_action'], ['Inicio de jornada', 'Llegada a proyecto', 'Toma de descansos', 'Salida de proyecto', 'Fin de jornada'])
    
    if st.button(t['register']):
        selected_user = next((u for u in users if u['name'] == user), None)
        if selected_user:
            timestamp = dt.datetime.now(tz=pytz.timezone('UTC')).isoformat()
            selected_user['working_hours'].append({'action': action, 'timestamp': timestamp})
            st.write(f'{action} {t["registered_for"]} {user} a las {timestamp}')
            
            if action == 'Fin de jornada':
                st.write(f'{t["sent_email_with_timesheet"]} {user}')
                st.write(f'{t["email_sent_to"]}: julian.torres@ahtglobal.com')

option = st.sidebar.selectbox(
    t['select_action'],
    [t['check_in_notification'], t['clock_out_notification'], t['inventory_tracking'], t['work_hours_tracking']]
)

if option == t['check_in_notification']:
    notificate_check_in(lang)
elif option == t['clock_out_notification']:
    notificate_clock_out(lang)
elif option == t['inventory_tracking']:
    track_inventory(lang)
elif option == t['work_hours_tracking']:
    track_work_hours(lang)

