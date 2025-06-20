"""
Модуль расчёта задолженности по лицевому счёту абонента.

Использует данные счётчиков, показаний, тарифов и оплат для вычисления начислений и задолженности.
"""

import psycopg2
import pandas as pd


def calculate_debts_for_account(account_number):
    """
    Выполняет расчёт задолженности для указанного лицевого счёта абонента.

    :param account_number: Лицевой счёт абонента
    :return: Словарь с информацией: имя, начисления, оплаты, итоговая задолженность.
             Если абонент или счётчики не найдены, возвращает None.
    """

    try:
        conn = psycopg2.connect(
            dbname="energy",
            user="postgres",
            password="1Wizard1",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name FROM abonents WHERE account_number = %s
        """, (account_number,))
        result = cursor.fetchone()
        if not result:
            return None

        abonent_id, full_name = result

        cursor.execute("SELECT id FROM meters WHERE abonent_id = %s", (abonent_id,))
        meter_ids = [row[0] for row in cursor.fetchall()]
        if not meter_ids:
            return None

        cursor.execute("""
            SELECT meter_id, reading_date, value
            FROM readings
            WHERE meter_id = ANY(%s)
            ORDER BY reading_date
        """, (meter_ids,))
        readings = cursor.fetchall()

        cursor.execute("SELECT start_date, value FROM tariffs ORDER BY start_date")
        tariffs = cursor.fetchall()

        cursor.execute("SELECT pay_date, amount FROM payments WHERE abonent_id = %s", (abonent_id,))
        payments = cursor.fetchall()

        cursor.close()
        conn.close()

        df_readings = pd.DataFrame(readings, columns=["meter_id", "reading_date", "value"])
        df_readings["reading_date"] = pd.to_datetime(df_readings["reading_date"])

        df_tariffs = pd.DataFrame(tariffs, columns=["start_date", "value"])
        df_tariffs["start_date"] = pd.to_datetime(df_tariffs["start_date"])

        df_payments = pd.DataFrame(payments, columns=["pay_date", "amount"])
        df_payments["pay_date"] = pd.to_datetime(df_payments["pay_date"])

        total_kwh = 0
        total_charge = 0

        if len(df_readings) >= 2:
            for i in range(1, len(df_readings)):
                diff = df_readings.iloc[i]["value"] - df_readings.iloc[i - 1]["value"]
                date = df_readings.iloc[i]["reading_date"]
                applicable_tariffs = df_tariffs[df_tariffs["start_date"] <= date]
                if not applicable_tariffs.empty:
                    tariff = applicable_tariffs.iloc[-1]
                    total_kwh += diff
                    total_charge += diff * tariff["value"]
                else:
                    print(f"Нет тарифа на дату {date.date()}, пропущено")
                total_kwh += diff
                total_charge += diff * tariff["value"]

        total_payment = df_payments["amount"].sum()
        debt = total_charge - total_payment

        return {
            "account_number": account_number,
            "full_name": full_name,
            "total_charge": round(total_charge, 2),
            "total_payment": round(total_payment, 2),
            "debt": round(debt, 2)
        }

    except Exception as e:
        print(f"Ошибка: {e}")
        return None
