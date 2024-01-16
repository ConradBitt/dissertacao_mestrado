"""
rodarLotes.py

    - Este arquivo é um script para executar os lotes de simulações.
    - Primeiro executa-se o arquivo batch.py para criar os parâmetros dentro da pasta data.
    - É importante criar um grid de parâmetros, por exemplo, 16x16, 32x32, etc.
    - Com os arquivos criados altere o valor da variável 'grid' compativel ao numero de pastas criadas em data.
    - execute o arquivo rodarLotes.py

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""


import os
import re
import time 
import datetime
import numpy as np


rodar = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=2:50:00
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end


"""

grid = 32

arquivos = [(i,j) for i in range(grid) for j in range(grid)]

#########################
#   versão a simulação
#########################
v = 3


#########################
# Tarefas para executar 
#########################
# init = lambda i, j: f'mpiexec -n 1 nrniv -python -mpi init.py simConfig=../data/v{v}_batch1/v{v}_batch1_{i}_{j}_cfg.json netParams=../data/v{v}_batch1/v{v}_batch1_netParams.py'
init = lambda i, j: f'python init.py simConfig=../data/v{v}_batch1/v{v}_batch1_{i}_{j}_cfg.json netParams=../data/v{v}_batch1/v{v}_batch1_netParams.py'


#############################
# Cria os lotes para executar
#############################
lotes = np.array_split(arquivos, 1)
rodar_lote = len(lotes)*[rodar]
for indice_lote, lote in enumerate(lotes):
    for l in lote:
        i, j = l
        rodar_lote[indice_lote] += f'{init(i,j)} &\n'
    rodar_lote[indice_lote] = rodar_lote[indice_lote][:-3]

#############################
# Cria os arquivos bash com 
# os lotes para rodar
#############################
for indice_lote,rodar in enumerate(rodar_lote):
    with open(f'rodar{indice_lote}.sh', 'w+') as rodar_sh:
        rodar_sh.writelines(rodar)
    print(rodar)

#############################
# Executa os comandos
#############################
def executar_comandos(passo, wait_seconds=3600*2):
    comandos = [f'sbatch rodar{indice_lote}.sh' for indice_lote,rodar in enumerate(rodar_lote)]

    inicio = datetime.datetime.now()
    # Itera pelos comandos em grupos de 8
    for i in range(0, len(comandos), passo):
        lote_comandos = comandos[i:i+passo]
        # Executa cada comando no grupo
        for comando in lote_comandos:
            os.system(comando)

        # Se não for o último grupo, aguarda 30 minutos
        if i + passo < len(comandos):
            print(f"Aguardando {wait_seconds/60} minutos antes do próximo lote...")
            
            time.sleep(int(wait_seconds))

    fim = datetime.datetime.now()
    print(20*'=--=')
    print(10*' ' + f'Total time running batches: {fim - inicio}')
    print(20*'----')

executar_comandos(passo = 8, wait_seconds=3600)