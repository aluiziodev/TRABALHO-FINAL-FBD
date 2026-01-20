# TRABALHO-FINAL-FBD (BDSpotPer)
Trabalho final da disciplina de Fundamentos de Bancos de Dados 2025.2, ministrada pelo professor Ângelo Brayner, Professor do Departamento de Computaçao da Universidade Federal do Ceara (UFC-DC).

---

## Equipe

- Jonathan Duarte Uchoa
- Aluizio Pereira Almendra Neto

---
## Requisitos
- Acesso ao SQL Server (sgbd utilizado)
- Python instalado no ambiente de execução
- Instalação dos frameworks python:
 - Tkinter (Nativo do python)
 - pymssql
- Sistema operacional: Linux Mint
**NOTA:** Em caso de execução em um OS diferente, alguns comandos para executar podem ser diferentes!!!!
---
## Como rodar?


Passo a passo de como rodar a interface gráfica interativa do ShopPer, dado todos os requisitos listados acima.


1. Inicialize o banco de dados executando os scripts da pasta DATABASE📂, onde você pode executar um a um os scripts numerados em sequência crescente, ou executar o script no arquivo ```ScriptCriacaoBDSpotPer.sql```.
**NOTA**: Na pasta filegroups, indique o caminho em que você deseja que os arquivos sejam criados. No nosso caso, estamos executando o sql server em um container do Docker.

2. Certifique-se que o Banco de Dados está ativo.
 
3. Criar um arquivo ```.env``` no diretório SRC📂 com os seguintes comandos presentes no arquivo:
```env
export DB_HOST=localhost # Host da sua conexão ao BD
export DB_USER=USER # seu usuário da conexão ao BD
export DB_PASS=PASSWORD # sua senha da conexão ao BD
export DB_NAME=BDSpotPer # nome do banco de dados
```

4. Dentro do diretório SRC📂, execute no Terminal:
```Bash
python main.py
```










