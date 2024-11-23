from datetime import datetime

# Classe que representa um usuário genérico
class Usuario:
    def __init__(self, nome_usuario, senha, nome, email, telefone):
        self.nome_usuario = nome_usuario  # Armazena o nome de usuário
        self.senha = senha  # Armazena a senha
        self.nome = nome  # Armazena o nome completo
        self.email = email  # Armazena o email
        self.telefone = telefone  # Armazena o telefone

    def fazer_login(self, email, senha):
        return (self.email == email and self.senha == senha) # Verifica se email e senha correspondem

# Classe que representa um cliente, herda de Usuario
class Cliente(Usuario):
    def __init__(self, nome_usuario, senha, nome, email, telefone):
        super().__init__(nome_usuario, senha, nome, email, telefone) # Chama o construtor da classe pai (Usuario)
        self.historico_reservas = [] # Inicializa o histórico de reservas como uma lista vazia

    def visualizar_reservas(self):
        print("\n--- Minhas Reservas ---")
        if not self.historico_reservas: # Verifica se o histórico está vazio
            print("Nenhuma reserva encontrada.")
        else:
            for reserva in self.historico_reservas: # Itera sobre as reservas no histórico
                print(f"Quarto {reserva['quarto']}, Check-in: {reserva['checkin']}, "
                      f"Check-out: {reserva['checkout']}") # Imprime informações da reserva

# Classe que representa um quarto
class Quarto:
    def __init__(self, numero, tipo, preco):
        self.numero = numero  # Número do quarto
        self.tipo = tipo  # Tipo do quarto (ex: "Solteiro", "Duplo")
        self.preco = preco  # Preço do quarto
        self.disponivel = True  # Indica se o quarto está disponível

class Reserva:
    def __init__(self, cliente, quarto, data_checkin, data_checkout):
        self.cliente = cliente  # Cliente que fez a reserva
        self.quarto = quarto  # Quarto reservado
        self.data_checkin = data_checkin  # Data de check-in
        self.data_checkout = data_checkout  # Data de check-out
        self.preco_total = self.calcular_preco_total() # Calcula o preço total da reserva

    def calcular_preco_total(self):
        dias = (self.data_checkout - self.data_checkin).days # Calcula a quantidade de dias da reserva
        return self.quarto.preco * dias # Retorna o preço total (preço do quarto * dias)

    def confirmar_reserva(self):
        print(f"Reserva confirmada para {self.cliente.nome}. Quarto: {self.quarto.numero}")
        # Lógica adicional para confirmação (ex: enviar email)

    def cancelar_reserva(self):
        print(f"Reserva cancelada para {self.cliente.nome}. Quarto: {self.quarto.numero}")
        self.quarto.disponivel = True  # Define o quarto como disponível novamente

class Pagamento:
    def __init__(self, reserva, valor, data_pagamento):
        self.reserva = reserva   # Reserva associada ao pagamento
        self.valor = valor       # Valor do pagamento
        self.data_pagamento = data_pagamento # Data do pagamento

    def processar_pagamento(self):
        print(f"Pagamento de R${self.valor:.2f} processado para a reserva de {self.reserva.cliente.nome}.")

class Relatorio:
    def __init__(self, tipo_relatorio, data_geracao, dados):
        self.tipo_relatorio = tipo_relatorio # Tipo do relatório
        self.data_geracao = data_geracao   # Data de geração do relatório
        self.dados = dados             # Dados do relatório


    def gerar_relatorio(self):
        print(f"Gerando relatório '{self.tipo_relatorio}' - {self.data_geracao.strftime('%Y-%m-%d')}")
        for item in self.dados: # Itera sobre os dados do relatório
            print(item) # Imprime cada item

# Função para criar uma nova conta de cliente
def criar_conta_clientes(clientes):
    print("\n--- Criar Conta ---")
    nome_usuario = input("Escolha um nome de usuário: ")
    senha = input("Escolha uma senha: ")
    nome = input("Digite seu nome completo: ")
    email = input("Digite seu e-mail: ")
    telefone = input("Digite seu telefone: ") 

    cliente = Cliente(nome_usuario, senha, nome, email, telefone)  
    clientes.append(cliente)
    print("Conta criada com sucesso!")

# Função para realizar o login do cliente
def fazer_login_clientes(clientes):
    print("\n--- Login ---")
    email = input("Digite seu e-mail: ")  # email 
    senha = input("Digite sua senha: ")  # senha 

    for cliente in clientes:  # Itera sobre a lista de clientes
        if cliente.fazer_login(email, senha):  # Verifica se as credenciais correspondem
            print(f"Bem-vindo(a), {cliente.nome}!")
            return cliente  # Retorna o objeto Cliente se o login for bem-sucedido
    print("E-mail ou senha incorretos.")
    return None  # Retorna None se o login falhar

# Função para pesquisar quartos disponíveis
def pesquisar_quartos(quartos):
    print("\n--- Quartos Disponíveis ---")
    disponiveis = [q for q in quartos if q.disponivel] # Cria uma lista com os quartos disponíveis

    if not disponiveis: # Verifica se há quartos disponíveis
        print("Nenhum quarto disponível no momento.")
        return [] # Retorna uma lista vazia se não houver quartos disponíveis
    
    for quarto in disponiveis: # Itera pelos quartos disponíveis
        print(f"Quarto {quarto.numero}: {quarto.tipo} - R${quarto.preco:.2f}") # Imprime informações do quarto
    return disponiveis  # Retorna a lista de quartos disponíveis

# Função para fazer uma reserva
def fazer_reserva(cliente, quartos):
    print("\n--- Fazer Reserva ---")
    quartos_disponiveis = pesquisar_quartos(quartos) # Chama a função para pesquisar quartos disponíveis
    if not quartos_disponiveis: # Verifica se há quartos disponíveis
        return # Retorna se não houver quartos disponíveis

    # Loop para obter o número do quarto válido
    while True:
        try:
            numero_quarto = int(input("Digite o número do quarto que deseja reservar: "))
            quarto_selecionado = next((q for q in quartos_disponiveis if q.numero == numero_quarto), None)
            if quarto_selecionado: # Verifica se o quarto foi encontrado e está disponível
                break # Sai do loop se o quarto for válido
            else:
                print("Quarto inválido ou não disponível. Tente novamente.") # Mensagem de erro
        except ValueError: # Captura erros de entrada inválida (não numérica)
            print("Entrada inválida. Digite um número.")

    # Loop para obter datas de check-in e check-out válidas
    while True:
        try:
            checkin_str = input("Data de check-in (YYYY-MM-DD): ")
            checkin = datetime.strptime(checkin_str, "%Y-%m-%d").date()
            checkout_str = input("Data de check-out (YYYY-MM-DD): ")
            checkout = datetime.strptime(checkout_str, "%Y-%m-%d").date()

            if checkin >= checkout: # Verifica se a data de check-in é anterior à data de check-out
                print("Data de check-out deve ser posterior ao check-in.")
            else:
                break  # Sai do loop se as datas forem válidas
        except ValueError:  # Captura erros de formato de data inválido
            print("Formato de data inválido. Use YYYY-MM-DD.")

    # Cria a reserva
    reserva = Reserva(cliente, quarto_selecionado, checkin, checkout)
    cliente.historico_reservas.append(reserva) # Adiciona a reserva ao histórico do cliente
    quarto_selecionado.disponivel = False # Define o quarto como indisponível

    # Exemplo de uso das classes Pagamento e Relatorio 
    pagamento = Pagamento(reserva, reserva.preco_total, datetime.now().date())  # Cria um objeto Pagamento
    pagamento.processar_pagamento()  # Executa a função processar_pagamento

    relatorio_dados = [f"Reserva para {reserva.cliente.nome}",
                       f"Quarto: {reserva.quarto.numero}",
                       f"Check-in: {reserva.data_checkin}",
                       f"Check-out: {reserva.data_checkout}",
                       f"Total: R${reserva.preco_total:.2f}"]  # Dados para o relatório

    relatorio = Relatorio("Detalhes da Reserva", datetime.now().date(), relatorio_dados)  # Cria um objeto Relatorio
    relatorio.gerar_relatorio()  # Executa a função gerar_relatorio
    # --- Fim do exemplo ---

    print("Reserva realizada com sucesso!") # Mensagem de sucesso
    # ... (código para escolher quarto e datas)


# Função principal do programa
def main():
    clientes = [] # Lista para armazenar os clientes
    quartos = [ # Lista de quartos disponíveis
        Quarto(101, "Solteiro", 200),
        Quarto(102, "Duplo", 350),
        Quarto(103, "Suíte", 500)
    ]

    while True:
        print("\n--- Menu Principal ---")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Sair")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        if escolha == 1:
            criar_conta_clientes(clientes)
        elif escolha == 2:
            cliente = fazer_login_clientes(clientes)
            if cliente:
                while True:
                    print("\n--- Menu Cliente ---")
                    print("1. Pesquisar quartos")
                    print("2. Fazer reserva")
                    print("3. Visualizar reservas")
                    print("4. Sair") 

                    try:
                        escolha_cliente = int(input("Escolha uma opção: "))
                    except ValueError:
                        print("Entrada inválida. Digite um número.")
                        continue

                    if escolha_cliente == 1:
                        pesquisar_quartos(quartos)
                    elif escolha_cliente == 2:
                        fazer_reserva(cliente, quartos)
                    elif escolha_cliente == 3:
                        cliente.visualizar_reservas()
                    elif escolha_cliente == 4:
                        print("Saindo da conta do cliente.")
                        break
                    else:
                        print("Opção inválida.")
        elif escolha == 3:
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":  # Verifica se o script está sendo executado como programa principal
    main()  # Chama a função principal se for o caso
