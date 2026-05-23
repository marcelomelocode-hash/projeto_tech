# CREATE
# INTEGRACAO ENTRE O PYTHON E MYSQL
# import mysql.connector
# conexao = mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     password='root',
#     database= 'bdradar',
# )
# cursor = conexao.cursor()
# ------------------------------
# #CRUD
# nome_completo = "Marcelo Carvalho Melo"
# email= "marcelomelo@prof.educacao.sp.gov.br"
# telefone= "11 - 988468615"
# senha= "26@Calculo"
# dta_cadastro= "2026-04-21 19:55:00"
# comando = f'INSERT INTO tbl_usuario (nome_completo,email,telefone,senha,dta_cadastro) VALUES ("{nome_completo}","{email}", "{telefone}", "{senha}", "{dta_cadastro}")'
# cursor.execute(comando) 
# conexao.commit()
# cursor.close()
# conexao.close()

# ----------------------
# #CRUD
# #comando = '' # escreve o comando em sql que quero aqui
# #cursor.execute(comando)  # se os comandos da linha 10 e 11 editam o bd, entao, ou seja é:
# #create, update ou delete - estou editando o bd- nesse caso terei que ter uma terceira
# #linha de codigo, que é: 
# #conexao.commit()  #qdo. edito o b.d
# #resultado =cursor.fetchall() # se quero armazenar essa informacao em algum lugar- é quando estou lendo o b.d!!  
# ---------------------------

# READ - LER

# comando = f'SELECT * FROM tbl_usuario'
# cursor.execute(comando)
# resultado =cursor.fetchall()
# print(resultado)
# cursor.close()
# conexao.close()

# -----------------------------
# UPDATE - ATUALIZAR 

# nome_completo = "Marcelo carvalho Melo"
# email="marcelo.fecaf.com"
# comando = f'UPDATE tbl_usuario SET email= "{email}" WHERE nome_completo ="{nome_completo}"'
# cursor.execute(comando)
# conexao.commit()
# cursor.close()
# conexao.close()
# --------------------------
# DELETE

# idtbl_usuario = "1"
# comando = f'DELETE FROM tbl_usuario WHERE idtbl_usuario="{idtbl_usuario}"'
# cursor.execute(comando)
# conexao.commit()
# cursor.close()
# conexao.close()
