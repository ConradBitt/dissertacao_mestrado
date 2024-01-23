# Repositorio: Dissertação de Mestrado
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10557254.svg)](https://doi.org/10.5281/zenodo.10557254)

O objetivo é disponibilizar resultados, arquivos e algorítmos utilizados na dissertação de mestrado.

## Começando
### Pré-requisitos

Este repositório possui dependências com as linguagens C e Python (versão a definir). É aconselhável [criar um ambiente virtual python exclusivo](https://docs.python.org/3.10/library/venv.html) para usar os pacotes necessários. Se preferir, você pode usar [ambiente conda](https://conda.io/projects/conda/en/latest/user-guide/index.html). Este projeto depende do Open MPI, uma implementação de interface de passagem de mensagens de código aberto, para tarefas de computação paralela. Você pode instalar o Open MPI usando o gerenciador de pacotes específico do seu sistema operacional.

Após a criação do ambiente, os pacotes podem ser instalados da forma padrão a partir do Python Package Index (PyPI).

Você pode ver a versão individual de cada pacote no arquivo [requirements.txt](requirements.txt).

Alguns resultados são mostrados através do [Jupyter Notebook](https://jupyter.org/install), por isso é importante tê-lo instalado.

### Instalação

1. Crie um ambiente virtual com o pacote python [venv](https://docs.python.org/3.10/library/venv.html) ou [conda](https://conda.io/projects/conda/en/latest/user-guide/index.html). Ative o ambiente virtual e instale os pacotes com pip:

         pip install -r requirements.txt
        
2. Para computação paralela, instale o MPI: [Início rápido: Instalando o Open MPI](https://docs.open-mpi.org/en/v5.0.x/installing-open-mpi/quickstart.html)


## Como usar
Primeiro, na pasta “sim”, execute “nrnivmodl” no terminal para compilar os arquivos NEURON. Isto só deve ser feito uma vez.

# Simulações e Modificações

## Simulação 
As modificações nos parâmetros de simulação podem ser feitas através do arquivo [cfg.py](/sim/cfg.py). 

## Network
As modificações na rede podem ser feitas através do arquivo [netParams.py](/sim/netParams.py). 

## Run
A execução de uma simulação pode ser feita de duas maneiras:
1. Executando o arquivo [init.py](/sim/init.py)
3. Executando o arquivo [batch.py](/sim/batch.py)

**Observação:** Ao executar [batch.py](/sim/batch.py) é necessario definir a quantidade de lotes de redes que serão simuladas. O arquivo [batch.py](/sim/batch.py) escolhe uma ou mais variáveis definidas no arquivo [cfg.py](/sim/cfg.py) para variar. Por exemplo, o arquivo [cfg.py](/sim/cfg.py) tem a variável `amp` que se refere a amplitude da corrente externa aplicada na rede, com [batch.py](/sim/batch.py) podemos executar uma lista de aplitudes adicionando `params[('IClamp0', 'amp')] = [0.08, 0.10, 0.12]` dentro da função `custom()` de [batch.py](/sim/batch.py).

## Resultados
Os resultados das simulações são salvos de acordo com o que foi definido em [cfg.py](/sim/cfg.py), por padrão salva na pasta [data](/data/)

## PyCodes
Na pasta [PyCodes](/pycodes/) estão os scripts utilizados para produzir figuras. Por padrão a imagem `.png` gerada tem o mesmo nome do arquivo que o código `.py` que a gerou.

### Disparos Neuronais modelo HH e de Yamada
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/dinamica_HH_Yamamada.png" width="750">

### Reobase e Chronaxia
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/reobase_chronaxia.png" width="400">

### Exemplos de Rede
#### Matriz de Adjacência 
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/matrizAdjacencia.png" width="750">

#### Grafo da Rede
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/exemplo_rede.png" width="750">

### Potencial de Membrana e Parâmetro de Ordem Local
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/plotLOP_Potencial.png" width="750">

### Dinâmica da Rede
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/figures/v2_batch1_9_27_data_regiao_III_RSeChimera.png" width="750">

### Espaços de Parâmetro 
#### Raio de Acoplamento pela Condutância Sináptica Excitatória
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/space_param_v1_batch1.png" width="450">

#### Corrente Externa Aplicada pela Condutância Sináptica Excitatória
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/space_param_v2_batch1_2.png" width="450">

#### Quantidade de Elementos Incoerentes: Corrente Externa Aplicada pela Condutância Sináptica Excitatória 
<img src="https://github.com/ConradBitt/dissertacao_mestrado/blob/main/pycodes/space_param_v2_batch1_counts.png" width="450">





# Contribuidores do repositório
* [Conrado F. Bittencourt](https://github.com/ConradBitt/)


