sys.path.append('/Users/maugus/Projects/MyCrews/PDFToMarkdown/src')
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
import logging
import yaml
from jinja2 import Template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pdftomarkdown.agents import create_agent_leitor, create_agent_revisor
from pdftomarkdown.tasks import leitor_task, revisor_task
from pdftomarkdown.tools import create_pdf_search_tool
from pdftomarkdown.crew import create_crew


# Configuração de logs
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Diretório que contém os arquivos PDF
pdf_folder = "src/pdfs"
# Lista de arquivos PDF no diretório
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
logger.info(f"Arquivos PDF encontrados: {pdf_files}")


# Carregar o template a partir do arquivo .md
with open('src/instructions/templates.md', 'r', encoding='utf-8') as template_file:
    template = template_file.read()

# Carregar o Obsidian Tools a partir do arquivo .yaml
with open('src/instructions/ObsidianTolls.yaml', 'r', encoding='utf-8') as tools_file:
    obsidianTolls = yaml.safe_load(tools_file)['obsidianTools']

# Carregar o arquivo instructions.yaml
with open('src/instructions/instructions.yaml', 'r', encoding='utf-8') as instructions_file:
    instructions = yaml.safe_load(instructions_file)

solicitacoes = instructions['requests']
restricoes = instructions['constraints']
controles = instructions['controls']



# Lista para armazenar os dados de todos os artigos
all_articles = []

# Percorrer todos os PDFs na pasta especificada
for pdf_file_name in pdf_files:
    logger.info(f"Processando arquivo PDF: {pdf_file_name}")
    
    # Definindo o modelo de llm
    gpt = ChatOpenAI(model="gpt-4o-mini")
    pdf = os.path.join(pdf_folder, pdf_file_name)
    pdf_tool = create_pdf_search_tool (pdf)


    # LEITOR
    # Criando agent leitor
    logger.info("Criando agente leitor")
    agent_leitor = create_agent_leitor(gpt, pdf_tool) 
    '''agent vai com os seguintes atributos:
    -pdf_tool: Ferramenta que o agente utilizará para interagir com o PDF.
    -llm: O modelo de linguagem a ser usado pelo agente.
    '''
    # Designando agent leitor a tarefa de leitura
    logger.info("Criando tarefa de leitura")
    task_leitor = leitor_task(agent_leitor)


    # REVISOR
    # Criando agente revisor
    logger.info("Criando agente revisor")
    agent_revisor = create_agent_revisor(gpt)
    '''agent vai com os seguintes atributos:
    -llm: O modelo de linguagem a ser usado pelo agente.'''

    # Designando agente revisor a tarefa de revisão
    logger.info("Criando tarefa de revisão")
    task_revisor = revisor_task(agent_revisor)

    logger.info("Criando a crew")
    crew = create_crew(agent_leitor, task_leitor, agent_revisor, task_revisor)

    # Definir as entradas
    ipt = {
        'solicitacoes': solicitacoes,
        'template': template,
        'restricoes': restricoes,
        'controles': controles,
        'obsidianTolls': obsidianTolls
    }

    # Executar a crew e processar o resultado
    logger.info("Iniciando o processamento com a crew")
    results = crew.kickoff(inputs = ipt)

   # print(results)

    with open("src/markdowns/output.md", "w") as file:
        file.write(str(results))
        file.close()

"""
    article_data = mark
    # Caminho do arquivo onde o conteúdo será salvo
    output_folder = "src/markdowns"
    # Definir o nome do arquivo de saída baseado no nome do arquivo PDF
    output_file_name = os.path.splitext(pdf_file_name)[0] + ".md"
    output_file_path = os.path.join(output_folder, output_file_name)   

    # Verificar se o resultado é válido
if results and isinstance(results, dict):
    # Supondo que o texto final revisado esteja em uma chave específica, como 'final_text'
    final_text = results.get('final_text', 'Texto não encontrado.')

    # Salvando o resultado em um arquivo .md
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_text)
    
    logger.info(f"Texto final salvo com sucesso em {output_file_path}")
else:
    logger.error("Falha ao processar o texto final. Nenhum resultado válido retornado.")

# Exibir uma mensagem final de conclusão
print(f"Processo concluído. O conteúdo foi salvo em {output_file_path}")
"""


"""
    # Inspecionar o objeto results para descobrir onde o conteúdo está armazenado
    logger.info(f"Atributos e métodos disponíveis em results: {dir(results)}")
    logger.info(f"Conteúdo de results (resumo): {str(results)[:1000]}")  # Exibe uma amostra do conteúdo
    logger.info(f"Detalhes do objeto results: {results!r}")

    # Agora, com base na inspeção, ajustaremos o código
    # Verifique se o conteúdo está em algum dos atributos comuns, por exemplo, results.outputs
    if hasattr(results, "outputs"):
        # Vamos assumir que `outputs` seja uma lista e pegue o primeiro elemento
        first_output = results.outputs[0]
        logger.info(f"Primeiro output (resumo): {str(first_output)[:500]}")  # Exibe uma amostra do conteúdo

        # Supondo que `content` seja o que estamos procurando
        if 'content' in first_output:
            final_output_text = first_output['content']
            logger.info(f"Conteúdo gerado: {final_output_text[:500]}...")  # Exibir uma amostra do conteúdo
            all_articles.append(final_output_text)
        else:
            logger.error("O primeiro output não possui 'content'.")
    else:
        logger.error("O objeto results não possui um atributo 'outputs'.")

# Combine todos os artigos em um único arquivo Markdown
if all_articles:
    logger.info("Combinando todos os artigos em um único arquivo Markdown")
    markdown_content = "\n\n".join(all_articles)
    
    # Caminho para salvar o resultado final em um arquivo Markdown na pasta "markdowns"
    output_markdown_path = os.path.join("src", "markdowns", "output.md")
    os.makedirs(os.path.dirname(output_markdown_path), exist_ok=True)
    
    # Salvar o conteúdo em um arquivo Markdown
    logger.info(f"Salvando dados em {output_markdown_path}")
    with open(output_markdown_path, 'w') as file:
        file.write(markdown_content)

    logger.info(f"Dados salvos em {output_markdown_path}")
else:
    logger.error("Nenhum artigo foi gerado para salvar.")

"""