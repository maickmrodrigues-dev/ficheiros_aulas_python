numeros = [4, 8, 15, 16, 23, 42]

numero_digitado = int(input("Digite um número: "))

if numero_digitado in numeros:
    print(f"O número {numero_digitado} está na lista")
else:
    print(f"O número {numero_digitado} não está na lista")