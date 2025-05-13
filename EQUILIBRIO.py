import re
from sympy import symbols, Eq, solve

# Función para analizar la fórmula química y obtener la cantidad de átomos por elemento
def parse_formula(formula):
    elementos = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    resultado = {}
    for elemento, cantidad in elementos:
        cantidad = int(cantidad) if cantidad else 1
        resultado[elemento] = resultado.get(elemento, 0) + cantidad
    return resultado

# Función para balancear la ecuación química
def balancear_ecuacion(reactivos, productos):
    todos = reactivos + productos
    elementos = sorted(set(e for f in todos for e in parse_formula(f)))
    n = len(todos)
    x = symbols(f'x1:{n+1}')
    ecuaciones = []

    for el in elementos:
        izq = sum(parse_formula(f).get(el, 0) * x[i] for i, f in enumerate(reactivos))
        der = sum(parse_formula(f).get(el, 0) * x[i + len(reactivos)] for i, f in enumerate(productos))
        ecuaciones.append(Eq(izq, der))

    ecuaciones.append(Eq(x[0], 1))  # Normalizamos el primer coeficiente
    solucion = solve(ecuaciones, x, dict=True)[0]
    return [solucion.get(var, 1) for var in x]

# Función para calcular la masa molar de una sustancia
def calcular_masa_molar(formula):
    masas_molares = {
        "H": 1.008, "O": 16.00, "C": 12.01, "N": 14.01,
        "Cl": 35.45, "Na": 22.99, "K": 39.10, "Mg": 24.31,
        "Ca": 40.08, "S": 32.07, "Fe": 55.85, "Zn": 65.38
    }
    elementos = parse_formula(formula)
    return sum(masas_molares.get(el, 0) * cant for el, cant in elementos.items())

# Función principal para pedir datos al usuario y realizar el cálculo
def main():
    print("⚗️ Bienvenido a la aplicación de Cálculo Estequiométrico ⚗️")
    print("--------------------------------------------------------")

    # Entrada de reactivos y productos
    reactivos = input("Ingrese los reactivos (separados por coma, ej: H2, O2): ").replace(" ", "").split(",")
    productos = input("Ingrese los productos (separados por coma, ej: H2O): ").replace(" ", "").split(",")
    
    # Balanceo de la ecuación
    coef = balancear_ecuacion(reactivos, productos)
    n_reac = len(reactivos)
    coef_reactivos = coef[:n_reac]
    coef_productos = coef[n_reac:]

    # Mostrar la ecuación balanceada
    ecuacion = " + ".join(f"{int(c)} {r}" for c, r in zip(coef_reactivos, reactivos))
    ecuacion += " → "
    ecuacion += " + ".join(f"{int(c)} {p}" for c, p in zip(coef_productos, productos))
    
    print("\nEcuación balanceada:")
    print(ecuacion)

    # Cálculo estequiométrico
    sustancias = reactivos + productos
    sust_dada = input(f"Seleccione la sustancia conocida (en gramos) de las siguientes: {sustancias}: ")
    gramos_dados = float(input(f"Ingrese la cantidad (g) de {sust_dada}: "))
    sust_obj = input(f"Seleccione la sustancia a calcular (en gramos) de las siguientes: {sustancias} (excepto {sust_dada}): ")

    # Realizamos los cálculos
    idx_dada = sustancias.index(sust_dada)
    idx_obj = sustancias.index(sust_obj)
    
    masa_dada = calcular_masa_molar(sust_dada)
    masa_obj = calcular_masa_molar(sust_obj)
    
    # Moles de la sustancia dada
    moles_dada = gramos_dados / masa_dada
    
    # Proporción entre los coeficientes de la ecuación balanceada
    proporcion = coef[idx_obj] / coef[idx_dada]
    moles_obj = moles_dada * proporcion
    gramos_obj = moles_obj * masa_obj

    print("\n📊 Resultado:")
    print(f"- Moles de {sust_dada}: {moles_dada:.4f} mol")
    print(f"- Masa molar de {sust_obj}: {masa_obj:.2f} g/mol")
    print(f"- Gramos producidos de {sust_obj}: {gramos_obj:.2f} g")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
