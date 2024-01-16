# Repositorio: Dissertação de Mestrado
O objetivo é disponibilizar resultados, arquivos e algorítmos utilizados na dissertação de mestrado.

## Começando
### Pré-requisitos

Este repositório possui dependências com as linguagens C e Python (versão a definir). É aconselhável [criar um ambiente virtual python exclusivo](https://docs.python.org/3.10/library/venv.html) para usar os pacotes necessários. Se preferir, você pode usar [ambiente conda](https://conda.io/projects/conda/en/latest/user-guide/index.html). Este projeto depende do Open MPI, uma implementação de interface de passagem de mensagens de código aberto, para tarefas de computação paralela. Você pode instalar o Open MPI usando o gerenciador de pacotes específico do seu sistema operacional.

Após a criação do ambiente, os pacotes podem ser instalados da forma padrão a partir do Python Package Index (PyPI).

Você pode ver a versão individual de cada pacote no arquivo [requirements.txt](requirements.txt).

Alguns resultados são mostrados através do [Jupyter Notebook](https://jupyter.org/install), por isso é importante tê-lo instalado.

### Instalação

1. Crie um ambiente virtual com o pacote python [venv](https://docs.python.org/3.10/library/venv.html) ou [conda](https://conda.io/projects/conda/en/latest/user-guide/index.html). Ative o ambiente virtual e instale os pacotes com pip:

         pip instalar -r requisitos.txt
        
2. Para computação paralela, instale o MPI: [Início rápido: Instalando o Open MPI](https://docs.open-mpi.org/en/v5.0.x/installing-open-mpi/quickstart.html)


## Como usar
Primeiro, na pasta “simulations_one_cell” ou “simulations_network”, execute “nrnivmodl” no terminal para compilar os arquivos NEURON. Isto só deve ser feito uma vez.

# Primeiro resultado
![img](https://github.com/ConradBitt/hh_ring/blob/main/data/v0_batch0/v0_batch0_raster.png)
