# 📚 Sistema de Gestão de Biblioteca (POO + JSON)

Este projeto é um sistema de gerenciamento de biblioteca desenvolvido em **Python**, focado na aplicação prática de **Programação Orientada a Objetos (POO)** e persistência de dados. O software permite o controle total de um catálogo de livros e revistas, gestão de usuários e um fluxo completo de empréstimos e devoluções.

## 🚀 Funcionalidades

- **Cadastro de Itens:** Suporte para Livros (com autor) e Revistas, utilizando herança.
- **Persistência em JSON:** Os dados são salvos automaticamente em um arquivo `biblioteca.json`, permitindo que as informações sejam mantidas mesmo após fechar o programa.
- **Sistema de Empréstimos:** Vinculação de itens a usuários com definição automática de data de devolução.
- **Polimorfismo de Prazos:** - **Livros:** Prazo de 15 dias.
    - **Revistas:** Prazo de 3 dias.
- **Cálculo de Multas:** O sistema verifica automaticamente se o item está sendo devolvido com atraso e calcula uma multa diária de R$ 2,00.

## 🛠️ Conceitos Técnicos Aplicados

O desenvolvimento deste sistema priorizou a organização de código e as melhores práticas de POO:

1.  **Abstração:** Classe base `ItemBiblioteca` definindo atributos comuns.
2.  **Herança:** `Livro` e `Revista` herdam de `ItemBiblioteca`, especializando o comportamento.
3.  **Polimorfismo:** O método `calcular_prazo()` é implementado de formas diferentes nas subclasses.
4.  **Serialização:** Conversão de objetos complexos para dicionários para armazenamento em formato JSON.
5.  **Tratamento de Erros:** Validação de entradas e verificação de integridade dos dados durante o carregamento.



## 📂 Estrutura do Arquivo de Dados

Os dados são estruturados no JSON da seguinte forma:

```json
{
    "itens": [
        {
            "tipo": "Livro",
            "titulo": "O Senhor dos Anéis",
            "ano": "1954",
            "esta_emprestado": true,
            "data_devolucao": "2026-05-06",
            "autor": "J.R.R. Tolkien"
        }
    ],
    "usuarios": [
        {
            "nome": "Renato",
            "itens_comigo": ["O Senhor dos Anéis"]
        }
    ]
}

```

## 📋 Como utilizar
Clone o repositório ou baixe o arquivo .py.

Certifique-se de ter o Python 3 instalado.

Execute o programa:

Utilize o menu interativo no terminal para navegar pelas funções.

## 📈 Roadmap de Evolução
[ ] Implementar interface gráfica (GUI).

[ ] Substituir o JSON por um banco de dados MySQL.

[ ] Adicionar funcionalidade de busca por autor ou ano.

[ ] Gerar recibos de empréstimo em formato .txt ou .pdf.

## 🤝 Conecte-se comigo

- **LinkedIn:** [Renato Andrade](www.linkedin.com/in/renato-andrade-a79570299)
- **DIO:** [Renato Andrade](https://web.dio.me/users/renatoandrade00)

Portfólio de Desenvolvimento Python / POO
