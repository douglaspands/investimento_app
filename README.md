# App para controle de investimentos
Aplicação para controle de investimentos.

## Requisitos

- Python >= 3.12

## Instalação

1. Clone o repositório: `git clone https://github.com/douglaspands/investimento_app.git`
2. Acesse a pasta do projeto: `cd investimento_app`
3. Crie um ambiente virtual (opcional): `python -m venv venv`
4. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No macOS/Linux: `source venv/bin/activate`
5. Instale o Poetry: `pip install poetry`
6. Instale as dependências: `poetry install`

## Execução

1. Execute a aplicação:
```sh
python main.py stock list BBAS3 VALE3

# Output:
 TICKER  NAME          PRICE  UPDATED_AT                 
 BBAS3   BANCO BRASIL  27.61  2025-02-04T01:11:37.913804 
 VALE3   VALE          54.21  2025-02-04T01:11:38.385332
```
> `python main.py --help` para ver os argumentos disponíveis.

## Contribuição

Para contribuir, faça o fork do repositório, crie uma nova branch com suas alterações e envie um pull request.



