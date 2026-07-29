from app.database import get_connection

def insert_patient(data, age, bmi):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patient_demographics (
        Date_of_Birth, Age, Sex, Height_cm, Weight_kg, BMI,
        Neck_Circumference_cm, Family_History_OSA,
        Tobacco_Use, Alcohol_Use, Caffeine_Use, Shift_Work
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        data.date_of_birth,
        age,
        data.sex,
        data.height_cm,
        data.weight_kg,
        bmi,
        data.neck_circumference_cm,
        data.family_history_osa,
        data.tobacco_use,
        data.alcohol_use,
        data.caffeine_use,
        data.shift_work
    ))

    conn.commit()
    conn.close()