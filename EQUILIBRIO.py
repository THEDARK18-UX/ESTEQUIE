import re

# Función para analizar la fórmula química y obtener la cantidad de átomos por elemento
def parse_formula(formula):
    # Expresión regular para extraer el elemento y su cantidad
    elementos = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    resultado = {}
    for elemento, cantidad in elementos:
        cantidad = int(cantidad) if cantidad else 1
        resultado[elemento] = resultado.get(elemento, 0) + cantidad
    return resultado

# Función para calcular la masa molar de una sustancia
def calcular_masa_molar(formula):
    masas_molares = {
        "H": 1.008, "O": 16.00, "C": 12.01, "N": 14.01,
        "Cl": 35.45, "Na": 22.99, "K": 39.10, "Mg": 24.31,
        "Ca": 40.08, "S": 32.07, "Fe": 55.85, "Zn": 65.38
    }
    elementos = parse_formula(formula)
    # Sumamos las masas molares de los elementos según su cantidad
    return sum(masas_molares.get(el, 0) * cant for el, cant in elementos.items())

# Función para realizar el cálculo estequiométrico
def calcular_estequiometria(reactivos, productos, coef_reactivos, coef_productos, sust_dada, gramos_dados, sust_obj):
    sustancias = reactivos + productos

    # Encontrar el índice de las sustancias en la lista
    idx_dada = sustancias.index(sust_dada)
    idx_obj = sustancias.index(sust_obj)

    # Calcular la masa molar de las sustancias
    masa_dada = calcular_masa_molar(sust_dada)
    masa_obj = calcular_masa_molar(sust_obj)

    # Calcular los moles de la sustancia dada
    moles_dada = gramos_dados / masa_dada

    # Calcular la proporción estequiométrica entre los coeficientes
    proporcion = coef_productos[idx_obj - len(reactivos)] / coef_reactivos[idx_dada]
    moles_obj = moles_dada * proporcion

    # Calcular los gramos de la sustancia a calcular
    gramos_obj = moles_obj * masa_obj

    return gramos_obj, moles_dada, masa_obj

# Función principal
def main():
    print("⚗️ Bienvenido a la aplicación de Cálculo Estequiométrico ⚗️")
    print("--------------------------------------------------------")

    # Entrada de reactivos y productos
    reactivos = input("Ingrese los reactivos (separados por coma, ej: H2, O2): ").replace(" ", "").split(",")
    productos = input("Ingrese los productos (separados por coma, ej: H2O): ").replace(" ", "").split(",")

    # Coeficientes balanceados (debes ingresarlos manualmente, por ejemplo, para la ecuación H2 + O2 → H2O)
    print("\n⚠️ Ingrese los coeficientes balanceados para la ecuación química.")
    print("Por ejemplo, para H2 + O2 → H2O, ingresa: 2 1 2 (correspondiente a 2 H2 + 1 O2 → 2 H2O)")

    coef_entrada = input(f"Ingrese los coeficientes balanceados para las sustancias: {reactivos + productos}: ")
    coef_balanceados = list(map(int, coef_entrada.split()))

    # Separar los coeficientes en reactivos y productos
    coef_reactivos = coef_balanceados[:len(reactivos)]
    coef_productos = coef_balanceados[len(reactivos):]

    # Mostrar la ecuación balanceada
    ecuacion = " + ".join(f"{c} {r}" for c, r in zip(coef_reactivos, reactivos))
    ecuacion += " → "
    ecuacion += " + ".join(f"{c} {p}" for c, p in zip(coef_productos, productos))

    print("\nEcuación balanceada:")
    print(ecuacion)

    # Cálculo estequiométrico
    sustancias = reactivos + productos
    sust_dada = input(f"Seleccione la sustancia conocida (en gramos) de las siguientes: {sustancias}: ")
    gramos_dados = float(input(f"Ingrese la cantidad (g) de {sust_dada}: "))
    sust_obj = input(f"Seleccione la sustancia a calcular (en gramos) de las siguientes: {sustancias} (excepto {sust_dada}): ")

    # Realizamos los cálculos
    gramos_obj, moles_dada, masa_obj = calcular_estequiometria(
        reactivos, productos, coef_reactivos, coef_productos, sust_dada, gramos_dados, sust_obj
    )

    print("\n📊 Resultado:")
    print(f"- Moles de {sust_dada}: {moles_dada:.4f} mol")
    print(f"- Masa molar de {sust_obj}: {masa_obj:.2f} g/mol")
    print(f"- Gramos producidos de {sust_obj}: {gramos_obj:.2f} g")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
