import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from simplepdfreader.agents import create_agent_leitor, create_agent_revisor
from simplepdfreader.tasks import leitor_task, revisor_task
from simplepdfreader.tools import create_pdf_search_tool
from simplepdfreader.crew import create_crew

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

# Definições de solicitações, restrições e controles
solicitacoes = """
1. Título e Introdução: Extraia o título completo do documento e um resumo detalhado da introdução. O resumo deve capturar o objetivo principal do aula e fornecer uma visão geral clara da aula abordada.

2. Conteúdo das Aulas: Liste e descreva detalhadamente cada um dos temas das aulas presentes no documento. Para cada tema, identifique os tópicos principais discutidos e seus respectivos subtópicos, assim como os métodos de ensino utilizados (como exemplos práticos, estudos de caso, etc.), e qualquer outra informação relevante que ajude a enriquecer o nosso conteúdo

3. Resumo do conteudo: Identifique e extraia todos os conceitos-chave e definições apresentados nos temas, tópicos e subtópicos. Para cada temas, tópicos e subtópicos, forneça um resumo completo e, se possível, relacione-o com exemplos ou aplicações práticas.

4. Técnicas: Utilize técnicas de estudo comprovadas para ajudar na retenção e compreensão do conteúdo. Inclua técnicas como aprendizagem ativa, repetição espaçada, prática intercalada, auto-teste, mapas conceituais, codificação dupla, elaboração, gerenciamento de distrações, revisão de erros passados e trabalho profundo.

5. Exemplos e Estudos de Caso: Identifique e resuma todos os exemplos práticos e estudos de caso presentes no documento. Se necessario traga exemplos para enriquecer o nosso conteúdo.

6. Conclusões e Relevância: Extraia as conclusões finais apresentadas no documento. Destaque quaisquer insights ou descobertas importantes que possam ser relevantes para enriquecer nosso resumo.

7. Adição de conteúdo: Se necessário, adicione temas, tópicos, subtópicos e informações adicionais que possam enriquecer o conteúdo.

8. Formatação adicional: Quando necessário, podemos fugir um pouco do tamplate definido em <template> e utilizar as ferramentas do obsidan de formatação como as listadas em <obsidianTolls> para enriquecer o nosso conteúdo. {obsidianTolls}.

9. Referências e Leituras Recomendadas: Liste todas as referências citadas no documento e, se houver, as leituras recomendadas para aprofundamento do conteúdo. Inclua detalhes como autores, títulos, e onde podem ser encontradas.

"""

restricoes = """
1. Manter Termos Técnicos em Inglês: Não traduza termos técnicos amplamente reconhecidos em inglês, como "software engineering", "agile methodology", etc.

2. Nome de Ferramentas e Tecnologias: Não traduza nomes de ferramentas, tecnologias, frameworks ou linguagens de programação mencionados no documento, como "Git", "Python", "Scrum".

3. Fidelidade ao Conteúdo: O conteúdo extraído deve ser fiel ao documento original. Evite interpretações ou reformulações que possam alterar o significado original.

4. Não Use Jargões Desconhecidos: O foco deve ser em transmitir o conteúdo de maneira clara e precisa.

5. Formatação Estrutural: Mantenha a estrutura hierárquica e de formatação do documento original ao descrever tópicos e sub-tópicos. Utilize o mesmo estilo de título e numeração presente no PDF, quando aplicável.

6. Nome de Autores e Referências: Não traduza ou altere os nomes dos autores e as referências bibliográficas.
"""

controles = """
1. Estilo e Tom: Use um tom formal e acadêmico, apropriado para documentos de ensino superior em Engenharia de Software.

2. Foco no Conteúdo: A extração deve estar 100% focada no conteúdo do documento. Se necessario adicione informações externas ou opiniões pessoais, desde que sejam comprovadas cientificamente.

3. Linguagem: Escreva em Português do Brasil, utilizando a norma culta da língua. A linguagem deve ser clara e objetiva, sem ambiguidades.

4. Sentimento e Neutralidade: Mantenha um tom neutro e científico. Não adicione adjetivos ou superlativos desnecessários.

5. Originalidade: As informações extraídas devem ser apresentadas de forma original, mantendo a integridade do conteúdo.

6. Nível de Detalhe: As respostas devem ser detalhadas, mas concisas. Não ultrapasse o necessário para transmitir as informações essenciais e contextualizar os conceitos importantes.

7. Tempo Verbal: Use o tempo verbal adequado ao contexto, resultados e estudos de caso.
"""

# Defina aqui o template que será utilizado no processamento dos dados
template = """
# {{ titulo }}
{{ descricao_da_aula }}

---

## Temas
{{ liste todos os temas }}

---

{% for tema in temas %}
## {{ tema.nome }}

**Descrição Geral:**
{{ tema.descricao }}

### Tópicos e Subtópicos

{% for tópico in tema.topicos %}
#### {{ tópico.nome }}

**Descrição Geral:**
{{ tópico.descricao }}

##### Tópicos e Subtópicos

{% for subtópico in tópico.subtopicos %}
##### {{ subtópico.nome }}

**Descrição do Subtópico:**
{{ subtópico.descricao }}

**Conteúdo Detalhado:**
{{ subtópico.conteudo }}

**Explicação Didática:**
{{ subtópico.explicacao_didatica }}

**Exemplos Práticos:**
{{ subtópico.exemplos_praticos }}

> [!tip] **Dica:**
> {{ subtópico.dica }}

> [!info] **Aviso:** {{ subtópico.aviso | default('Nenhum aviso adicional') }}

**Técnicas de Estudo Aplicadas:**
- **Aprendizagem ativa:** {{ subtópico.tecnicas.aprendizagem_ativa | default('Não aplicada') }}
- **Repetição espaçada:** {{ subtópico.tecnicas.repeticao_espacada | default('Não aplicada') }}
- **Prática intercalada:** {{ subtópico.tecnicas.pratica_intercalada | default('Não aplicada') }}
- **Auto-teste:** {{ subtópico.tecnicas.auto_teste | default('Não aplicada') }}
- **Mapas conceituais:** {{ subtópico.tecnicas.mapas_conceituais | default('Não aplicada') }}
- **Codificação dupla:** {{ subtópico.tecnicas.codificacao_dupla | default('Não aplicada') }}
- **Elaboração:** {{ subtópico.tecnicas.elaboracao | default('Não aplicada') }}
- **Gerenciamento de distrações:** {{ subtópico.tecnicas.gerenciamento_de_distracoes | default('Não aplicada') }}
- **Revisão de erros passados:** {{ subtópico.tecnicas.revisao_de_erros_passados | default('Não aplicada') }}
- **Trabalho profundo:** {{ subtópico.tecnicas.trabalho_profundo | default('Não aplicada') }}

---

{% endfor %}
{% endfor %}
{% endfor %}

## Conclusão da Aula
{{ conclusao_da_aula }}

---

## Referências e Leituras Recomendadas
{{ referencias_e_leituras }}


"""

obsidianTolls = """"
"1. Markdown Básico: Utilize **negrito** (`**negrito**`), *itálico* (`*itálico*`), listas não ordenadas (`- item`), listas ordenadas (`1. item`), e cabeçalhos (`# Cabeçalho 1`, `## Cabeçalho 2`).",
"2. Tabelas: Crie tabelas para organizar dados usando a estrutura:\n   ```markdown\n   | Coluna 1 | Coluna 2 |\n   |----------|----------|\n   | Valor 1  | Valor 2  |\n   ```",
"3. Blocos de Código: Insira blocos de código com sintaxe específica:\n   - Bloco:\n     ```markdown\n     ```python\n     def exemplo():\n         pass\n     ```\n     ```\n   - Código em Linha: ``código em linha``",
"4. Citações: Adicione citações com o formato:\n   ```markdown\n   > Citação\n   ```",
"5. Links e Imagens: Inclua links e imagens com:\n   - Internos: `[[Nome do Arquivo]]`\n   - Externos: `[Texto do Link](URL)`\n   - Imagens: `![Texto Alternativo](URL_da_Imagem)`",
"6. Tarefas e Checklists: Crie checklists para gerenciamento de tarefas:\n   ```markdown\n   - [ ] Tarefa 1\n   - [x] Tarefa 2\n   ```",
"7. Notas e Anexos: Utilize notas de rodapé e anexos:\n   - Notas de Rodapé:\n     ```markdown\n     Texto[^1].\n     \n     [^1]: Nota de rodapé.\n     ```",
"8. Blocos de Citação e Tabelas Dinâmicas: Use citações e tabelas dinâmicas conforme necessário:\n   - Citação:\n     ```markdown\n     > \"Texto da citação\"\n     ```",
"9. Links de Referência e Metadados: Adicione links de referência e metadados YAML:\n   - Links de Referência:\n     ```markdown\n     [Texto do Link][nome]\n     [nome]: URL\n     ```\n   - Metadados YAML:\n     ```markdown\n     ---\n     tags: [exemplo]\n     date: 2024-08-10\n     ---\n     ```",
"10. Gráficos e Diagramas: Insira gráficos e diagramas usando Mermaid:\n    ```mermaid\n    graph TD\n        A --> B\n    ```",
"11. Blocos de Código Expandidos: Utilize blocos de código aninhados para detalhes:\n    ```markdown\n    ```markdown\n    # Título\n    - Lista\n      ```python\n      print(\"Exemplo\")\n      ```\n    ```\n    ```",
"12. Estilo de Texto: Use texto destacado e subscrito/sobrescrito:\n    - Texto Destacado: `==Texto Destacado==`\n    - Subscrito e Sobrescrito: `H~2~O`, `X^2^`",
"13. Estrutura de Conteúdo e Navegação: Organize sumários e navegação com plugins.",
"14. Embutindo Conteúdo: Incorpore notas e arquivos diretamente:\n    ```markdown\n    ![[nome do arquivo]]\n    ```"

"""

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

    print(results)
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