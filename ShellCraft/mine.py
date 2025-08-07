import msvcrt
import winsound
import json
from Ajuda import lint, titulo




def criar_mundo(largura=10, altura=10):

    MUNDO = []
    #Criando a matriz mundo
    for linhas in range(altura):
        linha = []
        for colunas in range(largura):
            linha.append("air")
        MUNDO.append(linha)
    
    return MUNDO


def cor(msg, cor=30, cor1=0):
    
    return f"\033[{cor1};{cor}m{msg}\033[m"


def espaxada():
    #Espaçamento pra deixar bonito
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def mostrar_mundo(MUNDO, posy=0, posx=0):
    y = 0

    #Números
    for numeracao in range(2):
        print("    ", end="")
        for c in range(len(MUNDO[0])):

            extra_size = 1 - (len(str(c))-1)#Para resolver o problema de mundos grandes

            if numeracao == 0:
                print(c, end=" "+" "*extra_size)
            else:
                print("v", end="  ")
        print()

    print()
    #Blocos
    for l in MUNDO:
        extra_size = 1-(len(str(y))-1)#Para resolver o problema de mundos grandes

        print(str(y)+" "*extra_size+">", end=" ")
        x = 0

        for c in l:

            #Mostrando os blocos
            
            if y == posy and x == posx:
                print(cor("x", 35), end="  ")

            elif c == "air":
                print(" ", end="  ", flush=True)
            
            elif c == "stone":
                print(cor("P", 30), end="  ")
            
            elif c == "grass":
                print(cor("G", 32), end="  ")

            elif "tnt" in c:
                print(cor("T", 31), end="  ")

            elif c == "water0":
                print(cor(f"{c[-1]}", 34), end="  ")

            elif "water" in c:
                print(cor(f"{c[-1]}", 34), end="  ")

            x += 1
            
        y += 1
        
        print()


def water_logic(block, level):
    #lógica da água
    if (block == "air") or level+1 < int(block[-1]):
        return "water" + str(level+1)

    else:
        return block


def block_id(id):

    if id == 0:
        return "stone"
    elif id == 1:
        return "grass"
    elif id == 2:
        return "water0"
    elif id == 3:
        return "tnt0"
    elif id == 4:
        return "air"


def loop_principal(mundo, nome_do_mundo):
    
    x_pos, y_pos = 0, 0

    block_select = 0

    opcao = 0

    explode_sound = False

    while opcao != 6:#loop do jogo
        

        y_pos = y_pos%len(mundo[0])
        x_pos = x_pos%len(mundo[0])

        espaxada()
        mostrar_mundo(mundo, y_pos, x_pos)
        if explode_sound:
            winsound.PlaySound("sons\explosion.wav", winsound.SND_ASYNC)
            explode_sound = False


        all_water = []
        all_tnt = []
        
        for l in range(len(mundo)):
            for c in range(len(mundo[l])):
                #loop de lógica
                block = mundo[l][c]


                if "water" in block:
                    #informações do bloco de água
                    water_info = []

                    water_info.append(int(block[-1]))#nível da água

                    #BLOCOS COLADOS NA ÁGUA
                    try:#blocos de baixo
                        water_info.append(mundo[l+1][c])
                    except:
                        water_info.append("")
                    try:#Bloco de cima
                        water_info.append(mundo[l-1][c])
                    except:
                        water_info.append("")
                    try:#Bloco da direita
                        water_info.append(mundo[l][c+1])
                    except:
                        water_info.append("")
                    try:#Bloco da esquerda
                        water_info.append(mundo[l][c-1])
                    except:
                        water_info.append("")

                    water_info.append([l, c])#posição da água

                    all_water.append(water_info)
                
                
                elif "tnt" in block:

                    all_tnt.append([l, c, int(block[-1])])



        vanish_water = []




        """
        
        Lógica da água
        
        """
        for water_info in all_water:

            l, c = water_info[-1][0], water_info[-1][1]
            
            if water_info[0] > 0:#blocos de água que vão secar
                if "water" + str(water_info[0]-1) not in water_info:

                    vanish_water.append([l, c])
                    
                    continue#para que a água não retorne das cinzas
                    
            if water_info[0] < 3:
                #Ações da água 
                
                try:#No bloco de baixo
                    mundo[l+1][c] = water_logic(water_info[1], water_info[0])
                except:
                    True

                try:#No bloco de cima
                    if l != 0:
                        mundo[l-1][c] = water_logic(water_info[2], water_info[0])
                except:
                    True

                try:#No bloco da direita    
                    mundo[l][c+1] = water_logic(water_info[3], water_info[0])
                except:
                    True
                
                try:#No bloco da esquerda
                    if c != 0:
                        mundo[l][c-1] = water_logic(water_info[4], water_info[0])
                except:
                    True


        for water in vanish_water:

            mundo[water[0]][water[1]] = "air"


        """

        Lógica TNT

        """

        for tnt  in all_tnt:
            l, c, lvl  = tnt[0], tnt[1], tnt[2]

            if lvl > 2:
                #Blocos pra destruir
                explode_sound = True
                
                if l != 0:#Se l ou c for zero, para qua a TNT não destrua [-1] index
                    try:
                        mundo[l-1][c] = "air"
                    except:
                        True
                    try:    
                        mundo[l-1][c+1] = "air"
                    except:
                        True
                    try:
                        mundo[l-1][c-1] = "air"
                    except:
                        True
                    try:
                        mundo[l-2][c] = "air"
                    except:
                        True

                if c != 0:
                    try:
                        mundo[l][c-1] = "air"
                    except:
                        True
                    try:
                        mundo[l+1][c-1] = "air"
                    except:
                        True    
                    try:
                        mundo[l][c-2] = "air"
                    except:
                        True
                
                try:
                    mundo[l][c] = "air"
                except:
                    True
                try:
                    mundo[l+1][c] = "air"
                except:
                    True
                try:
                    mundo[l][c+1] = "air"
                except:
                    True
                try:
                    mundo[l+1][c+1] = "air"
                except:
                    True
                try:
                    mundo[l+2][c] = "air"
                except:
                    True
                try:
                    mundo[l][c+2] = "air"
                except:
                    True


            else:
                mundo[l][c] = "tnt"+str(lvl+1)

        """
        
        JOGAR
        
        """
        #SELEÇÕES
        pedra_select = block_select == 0
        grama_select = block_select == 1
        agua_select = block_select == 2
        TNT_select = block_select == 3
        AR_select = block_select == 4

        print()
        
        #Gameplay e inventário

        print(cor("[1] - Pedra", 37-(pedra_select*5)), end=" | ")
        print(cor("[2] - Grama", 37-(grama_select*5)), end=" | ")
        print(cor("[3] - Água", 37-(agua_select*5)), end=" | ")
        print(cor("[4] - TNT", 37-(TNT_select*5)), end=" | ") 
        print(cor("[5] - AR", 37-(AR_select*5)), end=" | ") 
        print(cor("[6] - Sair e salvar", 31))

        print(cor("*(wasd para se mecher)"), end="")
        print(cor("(enter pra colocar bloco)"))
        opcao = msvcrt.getch()

        if opcao == b"w":#Subir
            winsound.PlaySound("sons\walk.wav", winsound.SND_ASYNC)
            y_pos -= 1

        elif opcao == b"s":#decer
            winsound.PlaySound("sons\walk.wav", winsound.SND_ASYNC)
            y_pos += 1

        elif opcao == b"a":#esquerda
            winsound.PlaySound("sons\walk.wav", winsound.SND_ASYNC)
            x_pos -= 1

        elif opcao == b"d":#direita
            winsound.PlaySound("sons\walk.wav", winsound.SND_ASYNC)
            x_pos += 1

        elif opcao == b"1":#pedra
            block_select = 0
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)

        elif opcao == b"2":#grama
            block_select = 1
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)

        elif opcao == b"3":#água
            block_select = 2
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)

        elif opcao == b"4":#TNT
            block_select = 3  
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)

        elif opcao == b"5":#AR
            block_select = 4
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)

        elif opcao == b"6":#Sair e salvar
            break

        elif opcao == b"\r":#colocar bloco
            winsound.PlaySound(f"sons\{block_id(block_select)}.wav", winsound.SND_ASYNC)
            mundo[y_pos][x_pos] = block_id(block_select)




    #Salvando o jogo
    dicionario_dos_mundos = {}
        

    try:
        with open("saves.json", "r") as saves:#Alterando o dicionário
            dicionario_dos_mundos = saves
            dicionario_dos_mundos = json.load(dicionario_dos_mundos)
            dicionario_dos_mundos[nome_do_mundo] = mundo
            
    
    except:#Caso primeira ocorrência
        dicionario_dos_mundos[nome_do_mundo] = mundo
    
    
    dicionario_dos_mundos = json.dumps(dicionario_dos_mundos)
            

    with open("saves.json", "w") as saves:#Reescrevendo tudo por cima
        saves.write(dicionario_dos_mundos)

    
    espaxada()



while True:
    #Título
    print(cor("    --MINESHELL--\n", 30))
    print(cor("[0] - Novo Mundo\n[1] - Selecionar Mundo", 32))
    print(cor("[2] - Sair", 31))
    
    selecao = lint(">> ")
    while selecao > 3 or selecao < 0:
        print(cor("Opção inválida", 31))
        selecao = lint(">> ")
    

    if selecao == 0:#Novo mundo
        
        while True:
            try:
                nome_do_mundo = input("Nome do mundo >> ")
                largura_do_mundo = lint("Largura do mundo(evite mais de 30) >> ")
                altura_do_mundo = lint("Altura do mundo >> ")

            except:
                continue

            finally:
                novo_mundo = criar_mundo(largura_do_mundo, altura_do_mundo)
                loop_principal(novo_mundo, nome_do_mundo)
                espaxada()

                break
    

    elif selecao == 1:#Mundo que existe

        titulo(cor("Seus Mundos", 33))

        dicionario_dos_mundos = {}

        try:
            with open("saves.json", "r") as saves:
                dicionario_dos_mundos = json.load(saves)

        except:
            espaxada()
            print(cor("Você não tem mundos ainda!", 31, 1))
            continue
        
        
        mundos_selec = []
        for mundo_id, mundo in enumerate(dicionario_dos_mundos):
            print(f"{mundo_id} -", cor(mundo, 33))
            mundos_selec.append(mundo)


        mundo_escolhido_id = lint(">> ")
        while mundo_escolhido_id < 0 or mundo_escolhido_id >= len(mundos_selec):
            print(cor("MUNDO INVÁLIDO", 31))
            mundo_escolhido_id = lint(">> ")


        mundo_escolhido = mundos_selec[mundo_escolhido_id]
        
        espaxada()

        loop_principal(dicionario_dos_mundos[mundo_escolhido], mundo_escolhido)

        espaxada()

    elif selecao == 2:#FIM )=

        break