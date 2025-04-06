
# IoT Sensor Data Ingestor

Este projeto tem como objetivo simular a captura de dados de diversos sensores, processar esses dados e armazená-los em nosso LakeHouse.

## Estrutura do Projeto

A estrutura do projeto foi organizada de maneira a ser modular e escalável, permitindo facilmente adicionar novos sensores e lógicas para coleta de dados. Abaixo está um resumo das principais pastas e arquivos:

```
ingestor/
├── sensors/                  # Lógica de cada tipo de sensor
│   ├── __init__.py
│   ├── base_sensor.py        # Classe base compartilhada entre todos os sensores
│   ├── sensor_gps.py         # Sensor GPS (exemplo)
│   └── ...
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── test_sensor_gps.py    # Testes específicos para o sensor GPS
│   └── ...
├── config/                   # Configurações e variáveis do projeto
│   └── settings.py           # Configurações gerais como banco de dados e diretórios
├── main.py                   # Código principal para executar o processo
├── requirements.txt          # Dependências do projeto
```

## Como Funciona

### 1. **Sensores**

Cada sensor é representado por uma classe que herda da classe base `BaseSensor`. Essa classe base já cuida de toda a parte de criação de diretórios e formatação do arquivo. O desenvolvedor é responsável apenas por implementar a lógica específica de cada sensor.

Por exemplo:

- **SensorGPS**: Gera dados de posição em 3D e calcula a distância entre pontos.

### 2. **Criação de Novos Sensores**

Para adicionar um novo sensor, basta criar uma nova classe dentro da pasta `sensors/` que herda de `BaseSensor`. Abaixo está o exemplo de como criar um novo sensor.

#### Passos para criar um novo sensor:

1. Crie uma nova classe em `sensors/` (exemplo: `sensor_light.py` para um sensor de luz).
2. Implemente o método `generate_data()` para gerar os dados simulados do seu sensor.
3. O método `save_data()` já está implementado na classe base, e irá salvar os dados gerados automaticamente no diretório adequado, com o formato correto.
4. Adicione um arquivo de teste em `tests/` para garantir que os dados do sensor estão sendo gerados corretamente.

### 3. **Diretório de Dados**

Cada sensor tem seu próprio diretório dentro do caminho `/data/{sensor_name}/`. O nome da pasta corresponde ao nome do sensor (por exemplo, `/data/gps/` ou `/data/temp/`). Dentro de cada diretório, os arquivos serão salvos com a data de execução, de acordo com a especificação técnica para cada sensor, por exemplo:

```
/data/gps/2025-04-05/14-25-30-gps.csv
/data/mecanico/2025-04-05-mecanico.csv

```

### 4. **Banco de Dados**

Os dados serão salvos no nosso LakeHouse dentro de um docker. As configurações de banco de dados são armazenadas no arquivo `.env` e são carregadas automaticamente através da biblioteca `python-dotenv`.

### 5. **Testes**

Testes automatizados são armazenados na pasta `tests/`. Cada sensor deve ter um arquivo de teste correspondente que valida o comportamento do sensor, como:

- Geração de dados.
- Salvamento dos dados no diretório correto.
- Garantia de que os arquivos não estão vazios.

### 6. **Como Rodar o Projeto**

Para rodar o projeto localmente, siga os seguintes passos:

1. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuração do MySQL**:
   Suba o docker do lakehouse com o docker-compose ou utilize o sql da sua máquina local, configure as variáveis de ambiente no arquivo `.env` na raiz do projeto.

3. **Rodando o código**:
   
   Para rodar o código e simular a geração de dados dos sensores:

   ```bash
   python main.py
   ```

4. **Executando os Testes**:

   Os testes podem ser rodados com o comando:

   ```bash
   pytest tests/
   ```

### 7. **Adicionar Novos Sensores**

Para adicionar novos sensores ao projeto, siga os seguintes passos:

1. Crie um novo arquivo em `sensors/` (por exemplo, `sensor_mecanico.py`).
2. Implemente a classe do sensor, que deve herdar da classe base `BaseSensor`.
3. Defina a lógica de geração de dados no método `generate_data()`.
4. Crie um arquivo de teste correspondente em `tests/test_sensor_mecanico.py`.
5. Certifique-se de que o sensor é devidamente testado e o arquivo gerado é salvo corretamente.
