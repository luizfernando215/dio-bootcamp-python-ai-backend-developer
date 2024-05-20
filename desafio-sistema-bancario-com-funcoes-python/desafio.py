import pytz
from datetime import datetime
import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
   try:   
    if valor > 0:
        saldo += valor
        data_deposito=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_deposito} - Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato                
   
   except:
    print(f"Operação falhou! O valor informado é inválido.")

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    try:        
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques

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

        return saldo, extrato        
    
    except:
        print(f"Operação falhou! O valor informado é inválido.")      
    
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    

    while True:    
        opcao = menu()

        match opcao:
            case 'd':
                try:
                    valor = float(input("Informe o valor do depósito: "))                    
                    saldo, extrato = depositar(saldo, valor, extrato)
                except:
                    print(f"Operação falhou! O valor informado é inválido.")  # Imprime a mensagem da exceção                            
                    
            case 's':
                try:
                    valor = float(input("Informe o valor do saque: "))

                    saldo, extrato = sacar(
                        saldo=saldo,
                        valor=valor,
                        extrato=extrato,
                        limite=limite,
                        numero_saques=numero_saques,
                        limite_saques=LIMITE_SAQUES,
                    )       

                except:
                    print(f"Operação falhou! O valor informado é inválido.")  # Imprime a mensagem da exceção   
            
            case 'e':
                 exibir_extrato(saldo, extrato=extrato)   
            
            case 'nu':
                criar_usuario(usuarios)

            case 'nc':
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)

                if conta:
                    contas.append(conta)
            case 'lc':
                listar_contas(contas)

            case 'q':
                break              
            
            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()                    