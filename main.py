from server import Server

def main():
    print("========================")
    print("Bem-vindo ao Comunikate!")
    print("========================")
    print("Digite:")
    print("1- Para entrar em um servidor, 2- Para criar um servidor")

    operation = int(input("Insira: "))

    if operation == 1:
        print("funcao login")
    if operation == 2:
        Server.criar_servidor()
    
if __name__ == "__main__":
    main()
