# agents.py 
import logging
from crewai import Agent

# Configuração do logger para capturar informações durante a criação dos agentes
logger = logging.getLogger(__name__)

def create_agent_leitor(llm, tool):
    """
    Cria o agente leitor, responsável por ler PDFs e extrair informações específicas
    conforme definido nas solicitações, gerando conteúdo diretamente em formato Markdown.

    Parâmetros:
    - llm: O modelo de linguagem a ser usado pelo agente.
    - tool: Ferramenta que o agente utilizará para interagir com o PDF.

    Retorna:
    - Agent: Uma instância do agente configurado para leitura de PDFs.
    """
    logger.info("Criando o agente leitor de PDFs")
    return Agent(
        role='PDF Reader',
        
        goal=("Ler PDFs e extrair informações específicas conforme definido em <solicitações>." 
        "Gerar um arquivo markdown utilizando as ferramentas de formatação do Obsidian listadas em <obsidianTolls> de acordo com a necessidade de cada subtópico, " 
        "use o o modelo especificado em <template> como base, mas não como regra, podendo ser flexivel de acordo com a necessidade de cada tema, tópico e subtópico."
        "O conteúdo gerado deve ser claro, conciso e visualmente atraente, seguindo as instruções fornecidas."
        "dentro do template com seus tema, tópicos e subtópicos podemos utilizar ferramentas de formatação do obsidian, "
        "como as listadas em <obsidianTolls> para enriquecer o conteudo e o visual do nosso arquivo markdown {solicitacoes} {template} {obsidianTolls}."),
        
        backstory="Você é um especialista em leitura e análise de aulas, com foco em gerar conteúdo bem formatado para o Obsidian."
        "Sua missão é extrair informações cruciais, compreendendo o conteúdo e organizando-o de forma clara e concisa."
        "Você deve seguir as instruções fornecidas e garantir que o conteúdo gerado seja preciso e relevante."
        "Ao responder às solicitações delimitadas em <solicitacoes></solicitacoes>,"
        "você deve levar em consideração as definições de controles em  <controles></controles>" 
        "e as restrições em <restricoes></restricoes>."
        "utilizar as ferramentas de formatação do Obsidian listadas em <obsidianTolls> de acordo com a necessidade de cada tópico, tornando assim nosso template flexivel, "
        "nosso conteúdo mais visual e rico em informações."
        "{solicitacoes} {template} {restricoes} {controles} {obsidianTolls}",
        
        llm=llm,  # Modelo de linguagem utilizado
        max_rpm=30,  # Limite de requisições por minuto para evitar sobrecarga
        verbose=True,  # Ativa logs detalhados para melhor depuração
        memory=False  # O agente não utiliza memória para manter informações entre as interações
    )

def create_agent_revisor(llm):
    """
    Cria o agente revisor, responsável por revisar o conteúdo Markdown gerado
    pelo agente leitor, garantindo que esteja bem formatado e correto para uso no Obsidian.

    Parâmetros:
    - llm: O modelo de linguagem a ser usado pelo agente.

    Retorna:
    - Agent: Uma instância do agente configurado para revisão de conteúdo Markdown.
    """
    logger.info("Criando o agente revisor de Markdown")
    return Agent(
        role="Revisor de Markdown",

        goal="Leia os dados extraidos pelo Agente Leitor e verifique se um mardown foi produzido "
        "utilizando a melhor ferramenta de formatação disponivel para cada subtópico, "
        "que a estrutura esta de acordo com o template proposto em <template>, "
        "com os dados solicitados em <solicitacoes>,"
        "Como resultado do seu trabalho, você deve retornar um markdown " 
        "revisado e validado, com a estrutura definida em template e pronto para ser utilizado no Obsidian.",

        backstory="Você é um especialista na revisão e formatação de conteúdo Markdown, " 
        "domina todos os recusos de formatação que o obsidian oferece, " 
        "Alem de conhecer os melhores metódos de estudos cientificamente comprovados." 
        "Sua função é garantir que os dados extraidos reflitam "
        "as solicitações definidas em <solicitações></solicitações> "
        "e que o markdown gerado esteja bem formatado com a estrutura do template definido em <template>."
        "voce deve garantir que todos os  temas sejam abordados, que todos os tópicos dos temas sejam abordados e que todos os subtópicos dos tópicos sejam abordados."
        "Sua atenção aos detalhes assegura que os resultados finais "
        "sejam precisos e conformes às expectativas e conforme a necessidade utilizem as melhores ferramentas de formatação, "
        "listadas em <obsidianTolls>, para cada elemento do conteudo. {solicitacoes} {template} {obsidianTolls}",

        llm=llm,  # Modelo de linguagem utilizado
        max_rpm=30,  # Limite de requisições por minuto para evitar sobrecarga
        verbose=True,  # Ativa logs detalhados para melhor depuração
        memory=False  # O agente não utiliza memória para manter informações entre as interações
    )
