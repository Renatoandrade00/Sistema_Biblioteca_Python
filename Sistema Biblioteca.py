import json
import os
from datetime import datetime, timedelta

# --- CLASSES BASE E HERANÇA ---

class ItemBiblioteca:
    def __init__(self, titulo, ano, esta_emprestado=False, data_devolucao=None):
        self.titulo = titulo
        self.ano = ano
        self.esta_emprestado = esta_emprestado
        
        # CORREÇÃO AQUI: Garante que self.data_devolucao seja sempre um objeto datetime ou None
        if isinstance(data_devolucao, str) and data_devolucao.strip():
            try:
                self.data_devolucao = datetime.strptime(data_devolucao, '%Y-%m-%d')
            except ValueError:
                self.data_devolucao = None
        else:
            self.data_devolucao = data_devolucao

    def to_dict(self):
        """Converte o objeto para um dicionário compatível com JSON"""
        # Verificamos se é um objeto datetime antes de chamar o strftime
        data_str = None
        if isinstance(self.data_devolucao, datetime):
            data_str = self.data_devolucao.strftime('%Y-%m-%d')
        
        return {
            'tipo': self.__class__.__name__,
            'titulo': self.titulo,
            'ano': self.ano,
            'esta_emprestado': self.esta_emprestado,
            'data_devolucao': data_str
        }

    def calcular_prazo(self):
        raise NotImplementedError("Subclasses devem implementar o cálculo de prazo.")

class Livro(ItemBiblioteca):
    def __init__(self, titulo, ano, autor, **kwargs):
        super().__init__(titulo, ano, **kwargs)
        self.autor = autor

    def calcular_prazo(self):
        return 15  # Prazo para livros: 15 dias

    def to_dict(self):
        d = super().to_dict()
        d['autor'] = self.autor
        return d

class Revista(ItemBiblioteca):
    def __init__(self, titulo, ano, **kwargs):
        super().__init__(titulo, ano, **kwargs)

    def calcular_prazo(self):
        return 3   # Prazo para revistas: 3 dias

# --- CLASSE USUÁRIO ---

class Usuario:
    def __init__(self, nome, itens_comigo=None):
        self.nome = nome
        self.itens_comigo = itens_comigo if itens_comigo else []

    def to_dict(self):
        return {
            'nome': self.nome,
            'itens_comigo': [item.titulo for item in self.itens_comigo]
        }

# --- CLASSE PRINCIPAL (GESTÃO) ---

class Biblioteca:
    def __init__(self, arquivo_dados='biblioteca.json'):
        self.arquivo_dados = arquivo_dados
        self.catalogo = []
        self.usuarios = {} # Dicionário para busca rápida por nome
        self.carregar_dados()

    def adicionar_item(self, item):
        self.catalogo.append(item)
        self.salvar_tudo()

    def salvar_tudo(self):
        """Salva todo o estado do sistema no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            dados = {
                'itens': [i.to_dict() for i in self.catalogo],
                'usuarios': [u.to_dict() for u in self.usuarios.values()]
            }
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar_dados(self):
        """Carrega e reconecta os objetos do arquivo JSON"""
        if not os.path.exists(self.arquivo_dados):
            return

        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                conteudo = json.load(f)
                
                # 1. Recriar itens do catálogo
                for i in conteudo.get('itens', []):
                    tipo = i.pop('tipo')
                    if tipo == 'Livro':
                        self.catalogo.append(Livro(**i))
                    elif tipo == 'Revista':
                        self.catalogo.append(Revista(**i))
                
                # 2. Recriar usuários e reconectar empréstimos
                for u in conteudo.get('usuarios', []):
                    novo_usuario = Usuario(u['nome'])
                    for titulo_salvo in u['itens_comigo']:
                        item_real = next((it for it in self.catalogo if it.titulo == titulo_salvo), None)
                        if item_real:
                            novo_usuario.itens_comigo.append(item_real)
                    self.usuarios[u['nome']] = novo_usuario
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def realizar_emprestimo(self, nome_usuario, titulo_item):
        usuario = self.usuarios.get(nome_usuario)
        item = next((i for i in self.catalogo if i.titulo.lower() == titulo_item.lower()), None)

        if not usuario or not item:
            print("Erro: Usuário ou Item não encontrado.")
            return

        if item.esta_emprestado:
            print(f"Erro: '{item.titulo}' já está com alguém.")
            return

        item.esta_emprestado = True
        item.data_devolucao = datetime.now() + timedelta(days=item.calcular_prazo())
        usuario.itens_comigo.append(item)
        self.salvar_tudo()
        print(f"Empréstimo de '{item.titulo}' para {usuario.nome} realizado com sucesso!")

    def realizar_devolucao(self, nome_usuario, titulo_item):
        usuario = self.usuarios.get(nome_usuario)
        if not usuario:
            print("Erro: Usuário não encontrado.")
            return

        item = next((i for i in usuario.itens_comigo if i.titulo.lower() == titulo_item.lower()), None)

        if item:
            # Lógica de Multa
            hoje = datetime.now()
            if hoje > item.data_devolucao:
                atraso = (hoje - item.data_devolucao).days
                print(f"ATENÇÃO: Multa de R$ {atraso * 2.0:.2f} (Atraso de {atraso} dias).")

            item.esta_emprestado = False
            item.data_devolucao = None
            usuario.itens_comigo.remove(item)
            self.salvar_tudo()
            print(f"Item '{item.titulo}' devolvido por {usuario.nome}.")
        else:
            print(f"Erro: {usuario.nome} não tem o item '{titulo_item}'.")

    def listar_status(self):
        print("\n--- STATUS DO CATÁLOGO ---")
        if not self.catalogo:
            print("Nenhum item cadastrado.")
        for i in self.catalogo:
            tipo = i.__class__.__name__
            status = "Disponível" if not i.esta_emprestado else f"Emprestado (Devolva em: {i.data_devolucao.strftime('%d/%m/%Y')})"
            print(f"[{tipo}] {i.titulo} ({i.ano}) - {status}")

# --- MENU DE INTERAÇÃO ---

def menu():
    biblio = Biblioteca()
    
    while True:
        print("\n--- SISTEMA DE BIBLIOTECA (POO + JSON) ---")
        print("1. Cadastrar Livro/Revista")
        print("2. Cadastrar Usuário")
        print("3. Emprestar Item")
        print("4. Devolver Item")
        print("5. Listar Tudo")
        print("0. Sair")
        
        op = input("Escolha uma opção: ")

        if op == "1":
            tipo = input("1 para Livro, 2 para Revista: ")
            t = input("Título: ")
            a = input("Ano: ")
            if tipo == "1":
                aut = input("Autor: ")
                biblio.adicionar_item(Livro(t, a, aut))
            else:
                biblio.adicionar_item(Revista(t, a))
            print("Item cadastrado!")
        
        elif op == "2":
            nome = input("Nome do usuário: ")
            if nome and nome not in biblio.usuarios:
                biblio.usuarios[nome] = Usuario(nome)
                biblio.salvar_tudo()
                print("Usuário cadastrado!")
            else:
                print("Nome inválido ou já existente.")

        elif op == "3":
            u = input("Nome do Usuário: ")
            i = input("Título do Item: ")
            biblio.realizar_emprestimo(u, i)

        elif op == "4":
            u = input("Nome do Usuário: ")
            i = input("Título do Item: ")
            biblio.realizar_devolucao(u, i)

        elif op == "5":
            biblio.listar_status()
            print("\nUsuários cadastrados:", list(biblio.usuarios.keys()))

        elif op == "0":
            print("Saindo e salvando dados...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()