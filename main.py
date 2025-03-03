def is_leap_year(year):
    """
    Devuelve True si el año es bisiesto.
    Regla:
      - Divisible entre 4, excepto si es divisible entre 100,
        a menos que también sea divisible entre 400.
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0

def month_day_sum(month, year):
    """
    Retorna la suma de días de los meses anteriores al mes dado.
    Se ajusta febrero a 29 días si la fecha es posterior a febrero en un año bisiesto.
    """
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month > 2 and is_leap_year(year):
        month_days[1] = 29
    return sum(month_days[:month - 1])

def day_of_week(day, month, year):
    """
    Calcula el día de la semana para fechas de los siglos XX y XXI según el método
    de "El calendario Occidental". La fórmula básica es:
    
        D = (año + [año/4] + suma_días_meses + día + siglo - corrección) mod 7
    
    donde:
      - Para años del siglo XX se usa el año = últimos dos dígitos,
        y el término 'siglo' se calcula con: siglo = 6 - 2 * ((año completo // 100) mod 4).
      - Para el siglo XXI, en el caso especial del año 2000 se aplica:
           * Si el mes es enero o febrero: se usa un "año efectivo" = 100 y se considera el siglo 19.
           * Si el mes es posterior a febrero: se usa el año efectivo = 0 y se resta 1 al total.
    El resultado se mapea a:
         0: Sunday, 1: Monday, 2: Tuesday, 3: Wednesday,
         4: Thursday, 5: Friday, 6: Saturday.
    """
    # Caso especial para el año 2000
    if year == 2000:
        if month <= 2:
            effective_yy = 100          # Se "trata" 2000 como 0100
            century = 19                # Se usa siglo 19 para la corrección
            correction = 0
        else:
            effective_yy = 0             # Para meses posteriores a febrero
            century = 20                # Siglo 20 (2000) normal
            correction = 1              # Se resta 1 para compensar el salto
    else:
        effective_yy = year % 100
        century = year // 100
        # Para meses de enero y febrero, se cuenta (effective_yy - 1)//4; para el resto, effective_yy//4.
        correction = 0

    if month <= 2:
        leap_count = (effective_yy - 1) // 4 if effective_yy > 0 else 0
    else:
        leap_count = effective_yy // 4

    m_sum = month_day_sum(month, year)
    # Cálculo de la corrección de siglo:
    # Para el siglo XX (1900-1999): siglo = 6 - 2 * ((19 mod 4)=3) = 6 - 6 = 0.
    # Para el siglo XXI (2000-2099): si century=20, entonces 20 mod 4 = 0, y siglo = 6.
    siglo = 6 - 2 * (century % 4)

    total = effective_yy + leap_count + m_sum + day + siglo - correction
    D = total % 7

    days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    return days[D]

def run_tests():
    """Ejecuta casos de prueba para verificar el código."""
    test_cases = [
        {"date": (1, 1, 2000),  "expected": "Sábado"},
        {"date": (29, 2, 2000), "expected": "Martes"},
        {"date": (31, 12, 1999), "expected": "Viernes"},
        {"date": (29, 2, 1996), "expected": "Jueves"},
        {"date": (8, 6, 1939),  "expected": "Jueves"},
        {"date": (1, 1, 2002),  "expected": "Martes"},
        {"date": (23, 1, 1900), "expected": "Martes"},
        {"date": (2, 3, 2025), "expected": "Domingo"},
        {"date": (31, 12, 2099), "expected": "Jueves"},
    ]
    print("\nEjecutando pruebas...")
    for test in test_cases:
        d, m, y = test["date"]
        expected = test["expected"]
        result = day_of_week(d, m, y)
        print(f"Fecha: {d}/{m}/{y} | Esperado: {expected} | Resultado: {result}")

if __name__ == "__main__":
    print("Calculadora de Fechas para los Siglos XX y XXI")
    mode = input("Escriba 't' para ejecutar pruebas, o cualquier otra tecla para usar el modo interactivo: ").strip().lower()
    if mode == 't':
        run_tests()
    else:
        try:
            d = int(input("Ingresar día (1-31): "))
            m = int(input("Ingresar mes (1-12): "))
            y = int(input("Ingresar año (1900-2099): "))
            if not (1900 <= y <= 2099 and 1 <= m <= 12 and 1 <= d <= 31):
                print("Fecha no válida. Asegúrese de que el año esté entre 1900 y 2099, el mes entre 1 y 12, y el día entre 1 y 31.")
            else:
                print(f"El día de la semana para {d}/{m}/{y} es {day_of_week(d, m, y)}.")
        except ValueError:
            print("Entrada no válida. Asegúrese de ingresar valores numéricos para día, mes y año.")
