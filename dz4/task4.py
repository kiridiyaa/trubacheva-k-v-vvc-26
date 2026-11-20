import os
import numpy as np
import pandas as pd


def load_data(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    df = pd.read_csv(path)
    return df


def analyze_titanic(df):
    print("Первые 5 строк таблицы (DataFrame):")
    print(df.head())

    ages = df["Age"].dropna()
    fares = df["Fare"].dropna()
    survived = df["Survived"]

    print("\nЧисленные признаки (Series + numpy):")
    print("Средний возраст:", round(np.mean(ages), 2))
    print("Медианный возраст:", round(np.median(ages), 2))
    print("Максимальная цена билета:", round(np.max(fares), 2))
    print("Минимальная цена билета:", round(np.min(fares), 2))

    print("\nКатегориальные признаки:")
    print("Распределение по полу:")
    print(df["Sex"].value_counts())
    print("\nРаспределение по классу каюты:")
    print(df["Pclass"].value_counts())

    df["AgeGroup"] = df["Age"].apply(
        lambda x: "Неизвестно" if pd.isna(x) else ("Взрослый" if x >= 18 else "Ребенок")
    )
    print("\nГруппы по возрасту (lambda + тернарный оператор):")
    print(df["AgeGroup"].value_counts())

    mr_names = [name for name in df["Name"] if "Mr." in str(name)]
    print("\nКоличество пассажиров с 'Mr.' (генератор списков):", len(mr_names))

    survival_rate = np.mean(survived) * 100
    status = "Высокая выживаемость" if survival_rate >= 50 else "Низкая выживаемость"
    print(f"\nПроцент выживших: {survival_rate:.2f}% ({status})")

    return df


data = load_data("titanic.csv")
analyze_titanic(data)
