# InvestimentoPy [trader.exe]

É uma ferramenta projetada para auxiliar investidores de todos os níveis a tomar decisões informadas e otimizar seus portfólios. Com uma interface intuitiva e acesso a dados em tempo real, você terá as informações necessárias para acompanhar o mercado e analisar oportunidades com confiança.

**Funcionalidades Principais:**

*   **Preços de Cotas:** Acompanhe os preços de cotas de ações de diversas empresas, obtendo informações em tempo real.
*   **Preços de FIIs (Fundos de Investimento Imobiliário):** Monitore os preços dos FIIs mais populares, permitindo que você invista em imóveis de forma diversificada.
*   **Mais Populares:** Tenha acesso aos tickers e FIIs mais negociados, indicando tendências do mercado.
*   **Balanceamento de Portfólio:** Dado o valor que deseja investir, e quais tickers você deseja comprar, ele calcula a quantidade de cada ativo que deve comprar.

## Requisitos

- Python >= 3.13

## Instalação

1. Clone o repositório: `git clone https://github.com/douglaspands/investimento_app.git`
2. Acesse a pasta do projeto: `cd investimento_app`
3. Crie um ambiente virtual: `python -m venv .venv`
4. Ative o ambiente virtual:
   - No Windows: `.venv\Scripts\activate`
   - No MacOS/Linux: `source .venv/bin/activate`
5. Instale o Poetry: `pip install poetry`
6. Instale as dependências: `poetry install`

## Execução

1. Execute a aplicação para obter o preço da ação pelo ticker:

```sh
python main.py stock get ITSA3

# Output:
 FIELD        VALUE                                                                                                                                               
 TICKER       ITSA3                                                                                                                                               
 NAME         ITAUSA                                                                                                                                              
 DOCUMENT     61.532.644/0001-15                                                                                                                                  
 PRICE        9.45                                                                                                                                                
 UPDATED_AT   2025-02-05T00:16:37.406598                                                                                                                          
 DESCRIPTION  A Itaúsa S.A., mais conhecida como Itaúsa, é uma das maiores holdings do país, especialmente por sua atuação no controle de empresas da área        
              financeira, com destaque para o Banco Itaú Unibanco.                                                                                                
              Criada nos anos 1960, a Itaúsa também é responsável pela gestão de empresas ligadas a outros segmentos como papel, celulose e tecnologia, por       
              exemplo. Por anos o grupo ainda atuou como a principal frente da área de investimentos do Banco Itaú.                                               
              Além disso, a Itaúsa é constituída como sociedade anônima de capital aberto, sendo suas ações negociadas na Bolsa do Brasil, a B3, sob os códigos   
              ITSA3 e ITSA4.
```

2. Execute a aplicação para listar o preços das ações:

```sh
python main.py stock list ITSA3 BBDC3 VALE3 ABEV3 PETR4 WEGE3 IGTA3 B3SA3

# Output:
 TICKER  NAME                                  DOCUMENT            PRICE  UPDATED_AT                 
 ITSA3   ITAUSA                                61.532.644/0001-15  9.50   2025-02-04T02:32:53.190873 
 BBDC3   BRADESCO                              60.746.948/0001-12  11.01  2025-02-04T02:32:52.985194 
 VALE3   VALE                                  33.592.510/0001-54  54.21  2025-02-04T02:32:53.246695 
 ABEV3   AMBEV                                 07.526.557/0001-00  11.03  2025-02-04T02:32:53.124743 
 PETR4   PETROBRAS                             33.000.167/0001-01  37.50  2025-02-04T02:32:53.228252 
 WEGE3   WEG                                   84.429.695/0001-11  53.90  2025-02-04T02:32:53.326571 
 IGTA3   IGUATEMI EMPRESA DE SHOPPING CENTERS  51.218.147/0001-93  33.00  2025-02-04T02:32:53.307780 
 B3SA3   B3                                    09.346.601/0001-25  11.16  2025-02-04T02:32:52.652061 
```

3. Execute a aplicação para listar as ações mais populares:

```sh
python main.py stock most_popular

# Output:
 ORDER  TICKER  NAME                DOCUMENT            PRICE  UPDATED_AT                 
 1      BBAS3   BANCO BRASIL        00.000.000/0001-91  27.77  2025-02-05T00:18:29.836376 
 2      VALE3   VALE                33.592.510/0001-54  54.02  2025-02-05T00:18:30.257107 
 3      ISAE4   ISA ENERGIA BRASIL  02.998.611/0001-04  23.79  2025-02-05T00:18:29.812324 
 4      CMIG4   CEMIG               17.155.730/0001-64  11.10  2025-02-05T00:18:30.334697 
 5      BBDC4   BRADESCO            60.746.948/0001-12  12.03  2025-02-05T00:18:30.151068 
 6      BBSE3   BB SEGURIDADE       17.344.597/0001-94  38.99  2025-02-05T00:18:30.091197
```

4. Execute a aplicação para obter o preço do FII pelo ticker:

```sh
python main.py reit get MXRF11

# Output:
 FIELD       VALUE                                     
 TICKER      MXRF11                                    
 NAME        Maxi Renda                                
 ADMIN       BTG PACTUAL SERVIÇOS FINANCEIROS S/A DTVM 
 SEGMENT     Híbrido                                   
 PRICE       9.00                                      
 UPDATED_AT  2025-02-05T00:19:59.495299
```

5. Execute a aplicação para listar o preços dos FIIs:

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

6. Execute a aplicação para obter os FIIs mais populares:

```sh
python main.py reit most_popular

# Output:
 ORDER  TICKER  NAME                                    ADMIN                                   SEGMENT                        PRICE   UPDATED_AT                 
 1      MXRF11  Maxi Renda                              BTG PACTUAL SERVIÇOS FINANCEIROS S/A    Híbrido                        9.00    2025-02-05T00:20:52.858447 
                                                        DTVM                                                                                                      
 2      XPML11  XP Malls                                XP INVESTIMENTOS CCTVM S.A.             Shoppings                      96.50   2025-02-05T00:20:52.891974 
 3      GARE11  GUARDIAN LOGISTICA                      BANCO DAYCOVAL S.A.                     Híbrido                        7.82    2025-02-05T00:20:53.305457 
 4      BTLG11  BTG PACTUAL LOGISTICA FDO INV IMOB -    BTG PACTUAL SERVIÇOS FINANCEIROS S/A    Híbrido                        94.33   2025-02-05T00:20:53.482030 
                FII                                     DTVM                                                                                                      
 5      HGLG11  CGHG Logística                          PLURAL S.A. BANCO MÚLTIPLO              Logística                      149.79  2025-02-05T00:20:52.971735 
 6      VGHF11  VALORA HEDGE FUND                       BANCO DAYCOVAL S.A.                     Títulos e Valores Mobiliários  6.81    2025-02-05T00:20:52.911971
```

7. Criar o cache do autocomplete ao apertar a tecla Tab:

```sh
python main.py utils auto_complete

# Output:
Tickers downloaded successfully!
```

8. Execute a aplicação para balancear o portfólio entre as ações:

```sh
python main.py balance stock --amount 1000 ITSA4 CXSE3 KLBN4 SAPR4 TAEE4 BBSE3

# Output:
 TICKET  PRICE  COUNT   TOTAL  UPDATED_AT          
 BBSE3   40.26      4  161.04  2025-03-30T23:41:00 
 CXSE3   15.20     11  167.20  2025-03-30T23:41:00 
 ITSA4    9.62     18  173.16  2025-03-31T00:27:55 
 KLBN4    3.80     44  167.20  2025-03-31T00:27:55 
 SAPR4    5.48     31  169.88  2025-03-31T00:27:55 
 TAEE4   11.37     14  159.18  2025-03-31T00:27:55 

 TOTAL              VALUE 
 SHARE QUANTITY       122 
 SPENT AMOUNT      997.66 
 REMAINING AMOUNT    2.34 
```

9. Execute a aplicação para balancear o portfólio entre os FIIs:

```sh
python main.py balance reit --amount 1000 GARE11 CPTS11 VGIR11 SPXS11 CCME11 

# Output:
 TICKET  PRICE  COUNT   TOTAL  UPDATED_AT          
 CCME11   8.78     23  201.94  2025-03-31T00:52:17 
 CPTS11   7.20     28  201.60  2025-03-31T00:52:17 
 GARE11   8.60     24  206.40  2025-03-30T23:40:56 
 SPXS11   8.44     23  194.12  2025-03-31T00:52:17 
 VGIR11   9.58     20  191.60  2025-03-31T00:52:17 

 TOTAL              VALUE 
 SHARE QUANTITY       118 
 SPENT AMOUNT      995.66 
 REMAINING AMOUNT    4.34 
```

> `python main.py --help` para ver os argumentos disponíveis.

## Contribuição

Para contribuir, faça o fork do repositório, crie uma nova branch com suas alterações e envie um pull request.



