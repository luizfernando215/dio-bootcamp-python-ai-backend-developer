import pytz
from datetime import datetime


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:    
    opcao = input(menu)

    match opcao:
        case 'd':
           try:
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                data_deposito=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y %H:%M:%S")
                extrato += f"{data_deposito} - Depósito: R$ {valor:.2f}\n"
            else:
                print("Operação falhou! O valor informado é inválido.")

           except:
            print(f"Operação falhou! O valor informado é inválido.")  # Imprime a mensagem da exceção                            
            
        case 's':
            try:
             valor = float(input("Informe o valor do saque: "))

             excedeu_saldo = valor > saldo

             excedeu_limite = valor > limite

             excedeu_saques = numero_saques >= LIMITE_SAQUES

             if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")

             elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")

             elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")

             elif valor > 0:
                saldo -= valor
                data_saque=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y %H:%M")
                extrato += f"{data_saque} - Saque: R$ {valor:.2f}\n"
                numero_saques += 1

             else:
                print("Operação falhou! O valor informado é inválido.")        
            except:
             print(f"Operação falhou! O valor informado é inválido.")  # Imprime a mensagem da exceção   
        case 'e':
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
        case 'q':
            break              
        case _:
             print("Operação inválida, por favor selecione novamente a operação desejada.")
            