# FluxoNorte – Sistema Operacional de Entregas

Projeto desenvolvido para a disciplina de Algoritmos de Programação da PUC-Campinas.

## Sobre o projeto

A **FluxoNorte** é uma empresa de logística urbana que enfrentava dificuldades no gerenciamento de pedidos, entregadores e rotas devido ao uso de registros manuais e planilhas descentralizadas. Essas inconsistências comprometiam o controle operacional e dificultavam o acompanhamento das entregas.

Para solucionar esse problema, foi desenvolvido o **FluxoNorte – Sistema Operacional de Entregas**, uma aplicação em Python que centraliza as informações da operação por meio de um menu interativo em terminal.

O sistema permite cadastrar pedidos e entregadores, atualizar o status das entregas, realizar consultas em tempo real e gerar relatórios operacionais, oferecendo uma solução simples, organizada e preparada para futuras expansões.

---

## Funcionalidades

- Cadastro de pedidos
- Cadastro de entregadores
- Atualização do status dos pedidos
- Associação e remoção de entregadores em pedidos
- Consulta de pedidos e entregadores
- Geração de relatórios operacionais
- Validação de entradas e tratamento de erros
- Controle automático da disponibilidade dos entregadores

---

## Tecnologias utilizadas

- Python 3.x
- Visual Studio Code (VS Code)

Bibliotecas utilizadas:

- `random`
- `os`

> O projeto foi desenvolvido utilizando apenas módulos nativos da linguagem Python.

---

## Estruturas de dados

### Dicionários (`dict`)

Utilizados para armazenar os pedidos e entregadores utilizando seus respectivos IDs como chave, permitindo acesso rápido, atualização eficiente e garantia de unicidade dos registros.

### Listas (`list`)

Utilizadas para armazenar:

- Pedidos ativos de cada entregador;
- Histórico de entregas concluídas;
- Controle dos IDs de pedidos gerados durante a execução.

### Dicionários de constantes

Utilizados para mapear:

- Tipos de veículo;
- Prioridades;
- Status dos pedidos;
- Limites de carga.

Essa abordagem centraliza as regras de negócio e facilita futuras alterações.

---

## Funcionalidades implementadas

### Cadastro de pedidos

- Geração automática de IDs únicos;
- Cadastro de cliente, endereço, prioridade e descrição;
- Validação dos dados informados.

### Cadastro de entregadores

- Validação do formato do ID;
- Verificação de duplicidade;
- Cadastro do tipo de veículo e disponibilidade.

### Atualização de pedidos

- Alteração de status;
- Cancelamento de pedidos;
- Associação e remoção de entregadores.

### Consultas

O sistema permite:

- Listar pedidos por status;
- Buscar pedido por ID;
- Buscar pedidos pelo nome do cliente;
- Listar entregadores disponíveis;
- Buscar entregadores por nome;
- Consultar histórico de entregas.

### Relatórios

São apresentados indicadores como:

- Total de pedidos cadastrados;
- Quantidade por status;
- Pedidos com prioridade alta;
- Entregador com maior número de entregas concluídas.

---

## Decisões de modelagem

Durante o desenvolvimento foram adotadas algumas decisões importantes:

- Utilização do ID como chave dos dicionários para garantir unicidade;
- Validação dos IDs antes do cadastro;
- Definição de limites de carga conforme o tipo de veículo:
  - Moto: até 2 pedidos;
  - Carro: até 4 pedidos;
  - Van: até 6 pedidos;
- Exibição prioritária dos pedidos urgentes;
- Bloqueio da alteração de pedidos já entregues;
- Impossibilidade de reativar pedidos cancelados;
- Atualização automática da disponibilidade dos entregadores.

---

## Como executar

### Pré-requisitos

- Python 3.x
- Visual Studio Code (VS Code)

### Passos

Clone este repositório:

```bash
git clone https://github.com/seu-usuario/FluxoNorte.git
```

Acesse a pasta do projeto:

```bash
cd FluxoNorte
```

Execute o programa:

```bash
python fluxonorte.py
```

Ou abra o projeto no VS Code e pressione **F5**.

---
