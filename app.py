import streamlit as st
import datetime as dt
import pytz
import holidays
import requests
import os

# Ejemplo básico para empezar con Streamlit
st.title('Hootsi Application')

# Simular la funcionalidad de check-in y clock-out
def notificate_check_in():
    email_service= "model_postmark"  # Placeholder
    us_holidays = holidays.US()
    today_date = dt.datetime.now(tz=pytz.timezone('UTC'))

    users = [{"id": 315, "project_id": None, "time_zone": "America/New_York", "is_clocked_in": 0, "email": "user@example.com", "first_name": "User", "warehouse_id": 1, "tenant_id": 1}]

    if today_date not in us_holidays:
        for user in users:
            if user['id'] == 315 and user['project_id'] is None:
                user_tz = pytz.timezone(user['time_zone'])
                utc_now = dt.datetime.now(tz=pytz.timezone('UTC'))
                user_now = utc_now.astimezone(user_tz)

                if user_now.hour == 8 and user['is_clocked_in'] != 1:  # Recordatorio de clock in
                    st.write(f"Sending reminder email to: {user['email']}")
                    st.write("Hootsi would like to remind you to clock in and then check in for your project today.")

def notificate_clock_out():
    email_service= "model_postmark"  # Placeholder
    us_holidays = holidays.US()
    today_date = dt.datetime.now(tz=pytz.timezone('UTC'))

    users = [{"id": 315, "is_clocked_in": 1, "time_zone": "America/New_York", "email": "user@example.com", "first_name": "User", "warehouse_id": 1, "tenant_id": 1}]

    if today_date not in us_holidays:
        for user in users:
            if user['id'] == 315 and user['is_clocked_in'] == 1:  # Recordatorio de clock out
                user_tz = pytz.timezone(user['time_zone'])
                utc_now = dt.datetime.now()
                user_now = utc_now.astimezone(user_tz)
                if user_now.hour == 20 or True:
                    st.write(f"Sending reminder email to: {user['email']}")
                    st.write("Hootsi would like to remind you to clock out for the day.")

# Opciones de la interfaz
st.sidebar.title("Options")
option = st.sidebar.selectbox(
    'Select an action:',
    ('Check-In Notification', 'Clock-Out Notification')
)

if option == 'Check-In Notification':
    notificate_check_in()
elif option == 'Clock-Out Notification':
    notificate_clock_out()
