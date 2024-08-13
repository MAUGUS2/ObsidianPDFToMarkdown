
# Projeto: Leitor e Revisor de PDFs para Formatação em Markdown com Obsidian

## Descrição

Este projeto utiliza a framework CrewAI para criar uma equipe (crew) de agentes especializados em leitura e revisão de arquivos PDF. Os agentes extraem e formatam o conteúdo dos PDFs, produzindo arquivos Markdown prontos para serem usados no Obsidian, uma ferramenta de organização e anotação.

O projeto inclui dois agentes principais:

- **Agente Leitor:** Responsável por ler o conteúdo dos PDFs e gerar um arquivo Markdown com base em solicitações específicas.
- **Agente Revisor:** Revisa o Markdown gerado para garantir que o conteúdo esteja bem formatado e pronto para uso no Obsidian.

Além disso, o projeto permite que os usuários personalizem o comportamento dos agentes e o formato de saída por meio de arquivos de configuração, como `instructions.yaml`, `template.md`, e `obsidianTolls.yaml`.

## Estrutura do Projeto

```
src/
├── pdfs/                   # Diretório onde os arquivos PDF são armazenados.
├── markdowns/              # Diretório onde os arquivos Markdown gerados são salvos.
├── pdfTomarkdown/          # Diretório contendo os módulos principais do projeto.
│   ├── agents.py           # Criação dos agentes (Leitor e Revisor).
│   ├── tasks.py            # Criação das tarefas atribuídas aos agentes.
│   ├── tools.py            # Ferramentas utilizadas pelos agentes para processar PDFs.
│   ├── crew.py             # Configuração da equipe (crew) e orquestração das tarefas.
│   ├── main.py             # Script principal que executa o processamento dos PDFs.
│   └── instructions/       # Diretório contendo as instruções configuráveis pelos usuários.
│       ├── instructions.yaml # Instruções de solicitações, restrições e controles.
│       ├── templates.md      # Template para o arquivo Markdown gerado.
│       └── obsidiantolls.yaml # Ferramentas de formatação disponíveis para os agentes.
├── .env                    # Arquivo contendo variáveis de ambiente, como chaves de API.
└── pyproject.toml          # Arquivo de configuração do Poetry para gerenciar dependências.
```

## Pré-requisitos

Antes de iniciar, você precisará ter as seguintes ferramentas instaladas no seu sistema:

- Python 3.8+
- Poetry para gerenciar as dependências.
- Brew para instalações no macOS.

## Instruções de Instalação

### macOS

1. Instalar Homebrew (caso ainda não esteja instalado):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Instalar Python e Poetry usando Brew:
    ```bash
    brew install python
    brew install poetry
    ```
3. Clonar o repositório e instalar as dependências:
    ```bash
    git clone https://github.com/MAUGUS2/ObsidianPDFToMarkdown.git
    cd ObsidianPDFToMarkdown
    poetry install
    ```
4. Configurar as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API, seguindo o modelo abaixo:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

### Linux

1. Instalar Python e Poetry:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    pip install --user poetry
    ```
2. Clonar o repositório e instalar as dependências:
    ```bash
    git clone https://github.com/MAUGUS2/ObsidianPDFToMarkdown.git
    cd ObsidianPDFToMarkdown
    poetry install
    ```
3. Configurar as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API, seguindo o modelo abaixo:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

### Windows

1. Instalar Python:
    Baixe e instale Python.
2. Instalar Poetry:
    Abra o terminal (cmd, PowerShell, ou terminal do Windows) e execute:
    ```bash
    pip install poetry
    ```
3. Clonar o repositório e instalar as dependências:
    ```bash
    git clone https://github.com/MAUGUS2/ObsidianPDFToMarkdown.git
    cd ObsidianPDFToMarkdown
    poetry install
    ```
4. Configurar as variáveis de ambiente:
    Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API, seguindo o modelo abaixo:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Personalização

Este projeto permite que os usuários personalizem o comportamento dos agentes e o formato do arquivo de saída. Abaixo estão as principais áreas que podem ser configuradas:

1. **Instruções para os Agentes (`instructions.yaml`)**

No arquivo `instructions.yaml`, você pode definir:

- `requests`: As solicitações ou demandas específicas que o agente leitor deve extrair do PDF.
- `constraints`: Restrições que devem ser seguidas durante a extração do conteúdo.
- `controls`: Controles que garantem a qualidade e a conformidade do conteúdo gerado.

Exemplo:
```yaml
requests: |
  1. Extraia o título completo do documento e um resumo detalhado da introdução.
  2. Liste e descreva detalhadamente cada um dos temas das aulas presentes no documento.

constraints: |
  1. Mantenha termos técnicos em inglês.
  2. Não traduza nomes de ferramentas e tecnologias.

controls: |
  1. Use um tom formal e acadêmico.
  2. Escreva em Português do Brasil, utilizando a norma culta.
```

2. **Template para o Markdown (`template.md`)**

O arquivo `template.md` permite que você defina como o conteúdo extraído será estruturado no arquivo Markdown final. Você pode personalizar a ordem dos elementos, adicionar cabeçalhos e seções adicionais, e ajustar a formatação.

Exemplo:
```markdown
# {{ titulo }}
{{ descricao_da_aula }}

---

## Temas
{{ liste todos os temas }}

---

3. **Ferramentas de Formatação (`obsidiantolls.yaml`)**

No arquivo `obsidiantolls.yaml`, você pode definir quais ferramentas de formatação do Obsidian estarão disponíveis para os agentes utilizarem durante o processamento do conteúdo.

Exemplo:
```yaml
- Markdown Básico
- Tabelas
- Blocos de Código
- Citações
- Links e Imagens
```

## Executando o Projeto

1. Coloque os arquivos PDF que deseja processar na pasta `src/pdfs`.
2. Execute o script principal:
    ```bash
    poetry run python src/main.py
    ```
3. Verifique os arquivos Markdown gerados na pasta `src/markdowns`.

### Considerações Finais

Este projeto é um exemplo de aplicação da framework CrewAI para automatizar o processamento e a formatação de conteúdo acadêmico extraído de PDFs. A modularidade do código permite fácil expansão para outros tipos de documentos ou formatos de saída.
