def lint(msg, M0=False):
    inp = input(msg)
    inpcheck = inp.replace("-", "")
    while not inpcheck.isnumeric() or inp.count("-") > 1 or (M0 == True and int(inp) < 0):
        if not inpcheck.isnumeric() or inp.count("-") > 1:
            print(f"\033[31m{inp} não é um número inteiro!\033[m")
        else:
            print(f"\033[31m{inp} não é um número maior que zero!\033[m")
        inp = input(msg)
        inpcheck = inp.replace("-", "")
    return int(inp)


def lflt(msg, M0=False):
    inp = input(msg)
    inp = inp.replace(",", ".")
    inpcheck1 = inp.replace(".", "")
    inpcheck2 = inpcheck1.replace("-", "")
    while not inpcheck2.isnumeric() or inp.count("-") > 1 or inp.count(".") > 1 or (M0 == True and float(inp) < 0):
        if not inpcheck2.isnumeric() or inp.count("-") > 1 or inp.count(".") > 1:
            print(f"\033[31m{inp} não é um número!\033[m")
        else:
            print(f"\033[31m{inp} não é um número maior que zero!\033[m")
        inp = input(msg)
        inp = inp.replace(",", ".")
        inpcheck1 = inp.replace(".", "")
        inpcheck2 = inpcheck1.replace("-", "")
    return float(inp)

def titulo(msg):
    print("-"*(20+len(msg)))
    print(" "*10 + msg)
    print("-"*(20+len(msg)))


def insertVector():
    vetor = []

    titulo("INSIRA UM VETOR")
    while True:
        vetor.append(lint("(999 para)> "))
        if vetor[-1] == 999:
            vetor.pop()
            break
    return(vetor)


def insertMatriz(x=0, y=0, type=int, mode=0):
    matriz = []

    if type == int:
        readFunc = lint
    elif type == float:
        readFunc = lflt
    elif type == str:
        readFunc = input



    if mode == 0:
        titulo("INSIRA UMA MATRIZ")
        for j in range(0, y):
            vetor = []
            for i in range(0, x):
                vetor.append(readFunc(f"Insira o item ({j}, {i}) >>> "))
            matriz.append(vetor)


    if mode == 1:
        titulo("INSIRA UMA MATRIZ")
        keep = "s"
        while keep in "Ss":
            
            vetor = []
            titulo("INSIRA UM VETOR")

            while True:
                vetor.append(readFunc("(999 para)> "))
                if vetor[-1] == 999 or vetor[-1] == "999":
                    vetor.pop()
                    break
            
            matriz.append(vetor)
            keep = input("Quer mais uma linha [S/N]? ")

        
    return matriz
    