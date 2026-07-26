import random
import os

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

pedidos = {}
entregadores = {}
ids_pedidos_usados = []
ids_entregadores_usados = []

LIMITE_VEICULO = {"Moto": 2, "Carro": 4, "Van": 6}
OPCAO_PRIORIDADE = {"1": "Alta", "2": "Normal"}
OPCAO_VEICULO = {"1": "Carro", "2": "Van", "3": "Moto"}
OPCAO_STATUS = {"1": "Pendente", "2": "Em Rota", "3": "Entregue"}

def gerar_id_pedido():
    numero = random.randint(1000, 9999)
    id_gerado = "P" + str(numero)
    while id_gerado in ids_pedidos_usados:
        numero = random.randint(1000, 9999)
        id_gerado = "P" + str(numero)
    ids_pedidos_usados.append(id_gerado)
    return id_gerado

def buscar_pedido_por_id(id_pedido):
    return pedidos.get(id_pedido)

def buscar_entregador_por_id(id_entregador):
    return entregadores.get(id_entregador)

def exibir_cabecalho():
    print("=" * 50)
    print("{:^50}".format("FLUXONORTE"))
    print("{:^50}".format("SISTEMA OPERACIONAL DE ENTREGAS"))
    print("=" * 50)

def exibir_pedido(pedido, resumido=False):
    if resumido:
        print(f"   ID: {pedido['id']} | Cliente: {pedido['nome_cliente']} | Endereco: {pedido['endereco']} | Prioridade: {pedido['prioridade']}")
    else:
        print(f"\n>>> DADOS DO PEDIDO:")
        print(f"   ID:           {pedido['id']}")
        print(f"   Cliente:      {pedido['nome_cliente']}")
        print(f"   Endereco:     {pedido['endereco']}")
        print(f"   Prioridade:   {pedido['prioridade']}")
        print(f"   Descricao:    {pedido['descricao']}")
        print(f"   Status:       {pedido['status']}")
        entregador_info = pedido["id_entregador"] if pedido["id_entregador"] else "Nao associado"
        print(f"   Entregador:   {entregador_info}")

def ordenar_por_prioridade(lista_pedidos):
    alta = []
    for p in lista_pedidos:
        if p["prioridade"] == "Alta":
            alta.append(p)
    normal = []
    for p in lista_pedidos:
        if p["prioridade"] == "Normal":
            normal.append(p)
    return alta + normal

def cadastrar_pedido():
    print("\n---------- CADASTRO DE PEDIDO ----------")
    id_pedido = gerar_id_pedido()
    print(f">>> ID do pedido gerado automaticamente: {id_pedido}")
    nome_cliente = input(">>> Nome do cliente: ").strip()
    if nome_cliente == "":
        print(">>> Nome nao pode ser vazio. Cadastro cancelado.")
        ids_pedidos_usados.remove(id_pedido)
        return
    endereco = input(">>> Endereco de entrega: ").strip()
    if endereco == "":
        print(">>> Endereco nao pode ser vazio. Cadastro cancelado.")
        ids_pedidos_usados.remove(id_pedido)
        return
    print(">>> Prioridade: 1 - Alta  |  2 - Normal")
    prioridade = OPCAO_PRIORIDADE.get(input(">>> Escolha a prioridade: ").strip())
    if prioridade is None:
        print(">>> Opcao invalida. Cadastro cancelado.")
        ids_pedidos_usados.remove(id_pedido)
        return
    descricao = input(">>> Descricao do pedido: ").strip()
    if descricao == "":
        print(">>> Descricao nao pode ser vazia. Cadastro cancelado.")
        ids_pedidos_usados.remove(id_pedido)
        return
    pedidos[id_pedido] = {
        "id": id_pedido,
        "nome_cliente": nome_cliente,
        "endereco": endereco,
        "prioridade": prioridade,
        "descricao": descricao,
        "status": "Pendente",
        "id_entregador": None
    }
    print(f"\n>>> Pedido {id_pedido} cadastrado com sucesso!")

def cadastrar_entregador():
    print("\n---------- CADASTRO DE ENTREGADOR ----------")

    id_valido = False
    id_entregador = ""
    while id_valido == False:
        id_entregador = input(">>> Digite o ID do entregador (4 digitos numericos): ").strip()
        if not id_entregador.isdigit() or len(id_entregador) != 4:
            print(">>> ERRO: O ID deve conter exatamente 4 numeros.")
        elif id_entregador in entregadores:
            print(f">>> ERRO: Ja existe um entregador cadastrado com o ID {id_entregador}!")
            opcao = input(">>> Deseja tentar outro ID? (S/N): ").strip().upper()
            if opcao != "S":
                return
        else:
            id_valido = True

    nome = input(">>> Nome do entregador: ").strip()
    if nome == "":
        print(">>> Nome nao pode ser vazio.")
        return

    print(">>> Veiculo: 1 - Carro  |  2 - Van  |  3 - Moto")
    veiculo = OPCAO_VEICULO.get(input(">>> Escolha o veiculo: ").strip())
    if veiculo is None:
        print(">>> Opcao de veiculo invalida.")
        return

    entregadores[id_entregador] = {
        "id": id_entregador,
        "nome": nome,
        "veiculo": veiculo,
        "disponibilidade": "Disponivel",
        "pedidos_ativos": [],
        "historico_entregas": []
    }
    print(f"\n>>> Entregador {nome} (ID: {id_entregador}) cadastrado com sucesso!")

def atualizar_pedidos():
    print("\n---------- ATUALIZACAO DE PEDIDOS ----------")
    print(" 1 - Alterar status do pedido")
    print(" 2 - Cancelar pedido")
    print(" 3 - Associar entregador a pedido")
    print(" 4 - Remover entregador de pedido")
    print(" 0 - Voltar ao menu principal")
    opcao = input(">>> Selecione a opcao: ").strip()
    if opcao == "1":
        alterar_status()
    elif opcao == "2":
        cancelar_pedido()
    elif opcao == "3":
        associar_entregador()
    elif opcao == "4":
        remover_entregador()

def _liberar_entregador_se_vazio(entregador, id_pedido):
    if id_pedido in entregador["pedidos_ativos"]:
        entregador["pedidos_ativos"].remove(id_pedido)
    if len(entregador["pedidos_ativos"]) == 0:
        entregador["disponibilidade"] = "Disponivel"

def alterar_status():
    id_pedido = input(">>> Digite o ID do pedido: ").strip()
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None:
        print(">>> Pedido nao encontrado.")
        return
    if pedido["status"] == "Cancelado":
        print(">>> Pedido cancelado nao pode ter o status alterado.")
        return
    if pedido["status"] == "Entregue":
        print(">>> Pedido ja foi entregue e nao pode ser alterado.")
        return
    print(f">>> Status atual: {pedido['status']}")
    print(" 1 - Pendente  |  2 - Em Rota  |  3 - Entregue")
    novo_status = OPCAO_STATUS.get(input(">>> Novo status: ").strip())
    if novo_status is None:
        print(">>> Opcao invalida.")
        return
    entregador = buscar_entregador_por_id(pedido["id_entregador"]) if pedido["id_entregador"] else None
    if novo_status == "Entregue":
        if entregador:
            _liberar_entregador_se_vazio(entregador, id_pedido)
            if id_pedido not in entregador["historico_entregas"]:
                entregador["historico_entregas"].append(id_pedido)
        pedido["id_entregador"] = None
    pedido["status"] = novo_status
    print(f">>> Status atualizado para: {novo_status}")

def cancelar_pedido():
    id_pedido = input(">>> Digite o ID do pedido a cancelar: ").strip()
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None:
        print(">>> Pedido nao encontrado.")
        return
    if pedido["status"] == "Entregue":
        print(">>> Nao e possivel cancelar um pedido ja entregue.")
        return
    if pedido["status"] == "Cancelado":
        print(">>> Pedido ja esta cancelado.")
        return
    if pedido["id_entregador"]:
        entregador = buscar_entregador_por_id(pedido["id_entregador"])
        if entregador:
            _liberar_entregador_se_vazio(entregador, id_pedido)
    pedido["status"] = "Cancelado"
    pedido["id_entregador"] = None
    print(">>> Pedido cancelado com sucesso.")

def associar_entregador():
    id_pedido = input(">>> Digite o ID do pedido: ").strip()
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None:
        print(">>> Pedido nao encontrado.")
        return
    if pedido["status"] != "Pendente":
        print(">>> Apenas pedidos com status 'Pendente' podem ser associados a um entregador.")
        return
    id_entregador = input(">>> Digite o ID do entregador: ").strip()
    entregador = buscar_entregador_por_id(id_entregador)
    if entregador is None:
        print(">>> Entregador nao encontrado.")
        return
    limite = LIMITE_VEICULO.get(entregador["veiculo"], 2)
    if id_pedido in entregador["pedidos_ativos"]:
        print(">>> Este pedido ja esta associado a este entregador.")
        return
    if len(entregador["pedidos_ativos"]) >= limite:
        print(f">>> Entregador atingiu o limite de carga ({limite} pedidos para {entregador['veiculo']}).")
        return
    pedido["id_entregador"] = id_entregador
    entregador["pedidos_ativos"].append(id_pedido)
    entregador["disponibilidade"] = "Indisponivel"
    pedido["status"] = "Em Rota"
    print(f">>> Entregador associado! Pedidos ativos: {len(entregador['pedidos_ativos'])}/{limite}")

def remover_entregador():
    id_pedido = input(">>> Digite o ID do pedido: ").strip()
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None:
        print(">>> Pedido nao encontrado.")
        return
    if not pedido["id_entregador"]:
        print(">>> Este pedido nao possui entregador associado.")
        return
    entregador = buscar_entregador_por_id(pedido["id_entregador"])
    if entregador:
        _liberar_entregador_se_vazio(entregador, id_pedido)
    pedido["id_entregador"] = None
    pedido["status"] = "Pendente"
    print(">>> Entregador removido. Pedido voltou para 'Pendente'.")

def consultar_informacoes():
    print("\n---------- CONSULTA DE INFORMACOES ----------")
    print(" 1 - Pedidos Pendentes")
    print(" 2 - Pedidos Entregues")
    print(" 3 - Buscar Pedido por ID")
    print(" 4 - Entregadores Disponiveis")
    print(" 5 - Todas as entregas de um entregador")
    print(" 6 - Buscar entregador por nome")
    print(" 7 - Buscar pedido por nome do cliente")
    print(" 0 - Voltar ao menu principal")
    opcao = input(">>> Selecione a opcao: ").strip()
    if opcao == "1": listar_pedidos_por_status("Pendente")
    elif opcao == "2": listar_pedidos_por_status("Entregue")
    elif opcao == "3": buscar_pedido()
    elif opcao == "4": listar_entregadores_disponiveis()
    elif opcao == "5": entregas_por_entregador()
    elif opcao == "6": buscar_id_entregador_por_nome()
    elif opcao == "7": buscar_id_pedido_por_nome_cliente()

def listar_pedidos_por_status(status_filtro):
    print(f"\n>>> Pedidos com status '{status_filtro}':")
    filtrados = []
    for p in pedidos.values():
        if p["status"] == status_filtro:
            filtrados.append(p)
    ordenados = ordenar_por_prioridade(filtrados)
    if not ordenados:
        print("   Nenhum pedido encontrado.")
    else:
        for pedido in ordenados:
            exibir_pedido(pedido, resumido=True)

def buscar_pedido():
    id_pedido = input(">>> Digite o ID do pedido: ").strip()
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido:
        exibir_pedido(pedido, resumido=False)
    else:
        print(">>> Nao encontrado.")

def listar_entregadores_disponiveis():
    print("\n>>> Entregadores Disponiveis:")
    encontrou = False
    for entregador in entregadores.values():
        if entregador["disponibilidade"] == "Disponivel":
            print(f"   ID: {entregador['id']} | Nome: {entregador['nome']} | Veiculo: {entregador['veiculo']}")
            encontrou = True
    if not encontrou:
        print("   Nenhum entregador disponivel no momento.")

def entregas_por_entregador():
    id_entregador = input(">>> Digite o ID do entregador: ").strip()
    entregador = buscar_entregador_por_id(id_entregador)
    if entregador is None:
        print(">>> Entregador nao encontrado.")
        return
    print(f"\n>>> Entregas concluidas por {entregador['nome']}:")
    if not entregador["historico_entregas"]:
        print("   Nenhuma entrega concluida.")
        return
    for id_p in entregador["historico_entregas"]:
        p = buscar_pedido_por_id(id_p)
        if p:
            exibir_pedido(p, resumido=True)

def buscar_id_entregador_por_nome():
    nome_busca = input(">>> Digite o nome: ").strip().lower()
    encontrados = []
    for e in entregadores.values():
        if nome_busca in e["nome"].lower():
            encontrados.append(e)
    if not encontrados:
        print(">>> Nenhum entregador encontrado.")
        return
    for e in encontrados:
        print(f"   ID: {e['id']} | Nome: {e['nome']} | Veiculo: {e['veiculo']} | Disponibilidade: {e['disponibilidade']}")

def buscar_id_pedido_por_nome_cliente():
    nome_busca = input(">>> Nome do cliente: ").strip().lower()
    encontrados = []
    for p in pedidos.values():
        if nome_busca in p["nome_cliente"].lower():
            encontrados.append(p)
    if not encontrados:
        print(">>> Nenhum pedido encontrado.")
        return
    ordenados = ordenar_por_prioridade(encontrados)
    for p in ordenados:
        exibir_pedido(p, resumido=True)

def gerar_relatorio():
    print("\n---------- RELATORIO OPERACIONAL ----------")
    total = len(pedidos)
    print(f"\nTotal de pedidos cadastrados: {total}")

    if total == 0:
        print("   Nenhum pedido registrado.")
        return

    print("\n--- Pedidos por Status ---")
    contagem = {"Pendente": 0, "Em Rota": 0, "Entregue": 0, "Cancelado": 0}
    for p in pedidos.values():
        if p["status"] in contagem:
            contagem[p["status"]] += 1
    for s, q in contagem.items():
        print(f"   {s}: {q}")

    print("\n--- Pedidos com Alta Prioridade ---")
    alta_prioridade = []
    for p in pedidos.values():
        if p["prioridade"] == "Alta":
            alta_prioridade.append(p)
    if not alta_prioridade:
        print("   Nenhum pedido com alta prioridade.")
    else:
        print(f"   Total: {len(alta_prioridade)}")
        for p in alta_prioridade:
            print(f"   ID: {p['id']} | Cliente: {p['nome_cliente']} | Status: {p['status']}")

    print("\n--- Entregador com Maior Numero de Entregas ---")
    if not entregadores:
        print("   Nenhum entregador cadastrado.")
        return
    maior_quantidade = -1
    melhor_entregador = None
    for e in entregadores.values():
        total_entregas = len(e["historico_entregas"])
        if total_entregas > maior_quantidade:
            maior_quantidade = total_entregas
            melhor_entregador = e
    if melhor_entregador is None or maior_quantidade == 0:
        print("   Nenhuma entrega concluida ainda.")
    else:
        print(f"   Nome: {melhor_entregador['nome']} | ID: {melhor_entregador['id']} | Entregas concluidas: {maior_quantidade}")

def menu():
    sistema_ativo = True
    while sistema_ativo:
        exibir_cabecalho()
        print("\n================ MENU PRINCIPAL ================")
        print(" 1 - Cadastro de Pedidos")
        print(" 2 - Cadastro de Entregadores")
        print(" 3 - Atualizacao dos Pedidos")
        print(" 4 - Consulta de Informacoes")
        print(" 5 - Relatorios Operacionais")
        print(" 6 - Finalizar o Sistema")
        print("================================================")
        opcao = input(">>> Selecione a opcao desejada: ").strip()
        if opcao == "1": cadastrar_pedido()
        elif opcao == "2": cadastrar_entregador()
        elif opcao == "3": atualizar_pedidos()
        elif opcao == "4": consultar_informacoes()
        elif opcao == "5": gerar_relatorio()
        elif opcao == "6":
            print("\n>>> Encerrando o sistema FluxoNorte...")
            sistema_ativo = False
        if sistema_ativo:
            input("\n>>> Pressione ENTER para continuar...")
            limpar_terminal()

menu()