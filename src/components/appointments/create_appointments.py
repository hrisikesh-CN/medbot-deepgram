from langchain.tools import BaseTool, StructuredTool, tool
from ..llm_components.chains import SqlQueryChain
from src.utils import  get_appointment_database_url

def get_sql_query_chain():
    return SqlQueryChain(database_uri=get_appointment_database_url())


@tool
def get_doctor_slots(doctor_name):
    """Useful when you need to get available slots of a doctor"""
    query = f"What is the slots available for {doctor_name}"
    return get_sql_query_chain().run(query)


@tool
def create_appointments(doctor_name: str, patient_name: str, appointment_time: str):
    """Useful when you need to create appointments for a doctor."""

    patient_add_data_query = f"""Put appointment records into the table.
                Patient Name: {patient_name}
                doctor name: {doctor_name}
                time: {appointment_time}

                """

    # del the record in sql database with respect to the doctor name
    update_table_query = f"""An appointment has been booked for {doctor_name}
                time slot: {appointment_time}
                Please del that slot in available slot table

                """

    get_sql_query_chain().run(patient_add_data_query)
    get_sql_query_chain().run(update_table_query)

