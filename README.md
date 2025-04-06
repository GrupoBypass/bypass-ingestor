
# IoT Sensor Data Ingestor

Este projeto tem como objetivo simular a captura de dados de diversos sensores, processar esses dados e armazená-los em um banco de dados e/ou sistema de arquivos. Utilizamos o Python, Docker, MySQL, e ferramentas como Pandas e Grafana para visualização.

## Estrutura do Projeto

A estrutura do projeto foi organizada de maneira a ser modular e escalável, permitindo facilmente adicionar novos sensores e lógicas para coleta de dados. Abaixo está um resumo das principais pastas e arquivos:

```
ingestor/
├── sensors/                  # Lógica de cada tipo de sensor
│   ├── __init__.py
│   ├── base_sensor.py        # Classe base compartilhada entre todos os sensores
│   ├── sensor_gps.py         # Sensor GPS (exemplo)
│   ├── sensor_temp.py        # Sensor de Temperatura (exemplo)
│   └── ...
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── test_sensor_gps.py    # Testes específicos para o sensor GPS
│   ├── test_sensor_temp.py   # Testes para o sensor de Temperatura
│   └── ...
├── config/                   # Configurações e variáveis do projeto
│   └── settings.py           # Configurações gerais como banco de dados e diretórios
├── main.py                   # Código principal para executar o processo
├── requirements.txt          # Dependências do projeto
└── Dockerfile                # Definição do container Docker
```

## Como Funciona

### 1. **Sensores**

Cada sensor é representado por uma classe que herda da classe base `BaseSensor`. Essa classe base já cuida de toda a parte de criação de diretórios e formatação do arquivo. O desenvolvedor é responsável apenas por implementar a lógica específica de cada sensor.

Por exemplo:

- **SensorGPS**: Gera dados de posição em 3D e calcula a distância entre pontos.
- **SensorTemp**: Gera dados de temperatura aleatórios.

### 2. **Criação de Novos Sensores**

Para adicionar um novo sensor, basta criar uma nova classe dentro da pasta `sensors/` que herda de `BaseSensor`. Abaixo está o exemplo de como criar um novo sensor.

#### Passos para criar um novo sensor:

1. Crie uma nova classe em `sensors/` (exemplo: `sensor_light.py` para um sensor de luz).
2. Implemente o método `generate_data()` para gerar os dados simulados do seu sensor.
3. O método `save_data()` já está implementado na classe base, e irá salvar os dados gerados automaticamente no diretório adequado, com o formato correto.
4. Adicione um arquivo de teste em `tests/` para garantir que os dados do sensor estão sendo gerados corretamente.

### 3. **Diretório de Dados**

Cada sensor tem seu próprio diretório dentro do caminho `/data/{sensor_name}/`. O nome da pasta corresponde ao nome do sensor (por exemplo, `/data/gps/` ou `/data/temp/`). Dentro de cada diretório, os arquivos serão salvos com a data de execução, por exemplo:

```
/data/gps/2025-04-05/14-25-30-gps.csv
```

Se o diretório correspondente à data atual não existir, ele será criado automaticamente.

### 4. **Banco de Dados**

Os dados também podem ser salvos em um banco de dados MySQL, caso desejado. As configurações de banco de dados são armazenadas no arquivo `.env` e são carregadas automaticamente através da biblioteca `python-dotenv`.

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
   Se estiver usando o banco de dados MySQL, configure as variáveis de ambiente no arquivo `.env` na raiz do projeto.

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

### 7. **Docker**

Este projeto também está configurado para rodar em containers Docker. Abaixo estão as instruções para rodar o projeto em containers Docker:

1. **Build da imagem Docker**:

   ```bash
   docker build -t ingestor-image .
   ```

2. **Subir os containers com Docker Compose**:

   ```bash
   docker-compose up
   ```

### 8. **Adicionar Novos Sensores**

Para adicionar novos sensores ao projeto, siga os seguintes passos:

1. Crie um novo arquivo em `sensors/` (por exemplo, `sensor_humidity.py`).
2. Implemente a classe do sensor, que deve herdar da classe base `BaseSensor`.
3. Defina a lógica de geração de dados no método `generate_data()`.
4. Crie um arquivo de teste correspondente em `tests/test_sensor_humidity.py`.
5. Certifique-se de que o sensor é devidamente testado e o arquivo gerado é salvo corretamente.

---

## Contribuindo

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/ingestor.git
   cd ingestor
   ```

2. Crie uma branch para suas alterações:

   ```bash
   git checkout -b feature/nome-da-feature
   ```

3. Implemente a lógica do sensor e crie os testes.
4. Commit suas alterações:

   ```bash
   git commit -m "Adiciona sensor de nome"
   ```

5. Envie para o repositório remoto:

   ```bash
   git push origin feature/nome-da-feature
   ```

6. Crie um Pull Request para revisão.

---

## Dependências

- `pandas`: Para manipulação de dados.
- `sqlalchemy` e `pymysql`: Para interação com MySQL.
- `python-dotenv`: Para carregar variáveis de ambiente.
- `pytest`: Para testes automatizados.

---

## Licença

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
