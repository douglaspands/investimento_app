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

1. Execute a aplicação para listar o preços das ações:

```sh
python main.py stock list ITSA3 BBDC3 VALE3 ABEV3 PETR4 WEGE3 IGTA3 B3SA3

# Output:
 TICKER  NAME                                  PRICE  UPDATED_AT                 
 ITSA3   ITAUSA                                9.50   2025-02-04T02:15:50.935630 
 BBDC3   BRADESCO                              11.01  2025-02-04T02:15:50.897907 
 VALE3   VALE                                  54.21  2025-02-04T02:15:50.918082 
 ABEV3   AMBEV                                 11.03  2025-02-04T02:15:51.064169 
 PETR4   PETROBRAS                             37.50  2025-02-04T02:15:51.378713 
 WEGE3   WEG                                   53.90  2025-02-04T02:15:51.478451 
 IGTA3   IGUATEMI EMPRESA DE SHOPPING CENTERS  33.00  2025-02-04T02:15:51.396419 
 B3SA3   B3                                    11.16  2025-02-04T02:15:51.461526 
```

2. Execute a aplicação para listar o preços dos Fiis:

```sh
python main.py reit list MXRF11 XPML11 GARE11 HGLG11 VGHF11

# Output:
 TICKER  NAME                ADMIN                                      SEGMENT                        PRICE   UPDATED_AT                 
 MXRF11  Maxi Renda          BTG PACTUAL SERVIÇOS FINANCEIROS S/A DTVM  Híbrido                        9.03    2025-02-04T02:19:41.390377 
 XPML11  XP Malls            XP INVESTIMENTOS CCTVM S.A.                Shoppings                      97.45   2025-02-04T02:19:41.436584 
 GARE11  GUARDIAN LOGISTICA  BANCO DAYCOVAL S.A.                        Híbrido                        7.80    2025-02-04T02:19:41.088916 
 HGLG11  CGHG Logística      PLURAL S.A. BANCO MÚLTIPLO                 Logística                      149.60  2025-02-04T02:19:41.239980 
 VGHF11  VALORA HEDGE FUND   BANCO DAYCOVAL S.A.                        Títulos e Valores Mobiliários  7.00    2025-02-04T02:19:41.476547
```

> `python main.py --help` para ver os argumentos disponíveis.

## Contribuição

Para contribuir, faça o fork do repositório, crie uma nova branch com suas alterações e envie um pull request.



