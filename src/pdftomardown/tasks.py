# tasks.py 
import logging
from crewai import Task

# Configuração do logger para capturar informações durante a criação das tarefas
logger = logging.getLogger(__name__)

def leitor_task(agent_leitor):
    """
    Cria a tarefa do agente leitor, que é responsável por ler o conteúdo do PDF
    e gerar as respostas solicitadas diretamente em formato Markdown.

    Parâmetros:
    - agent_leitor: O agente que realizará a leitura do PDF.

    Retorna:
    - Task: Uma instância da tarefa que será atribuída ao agente leitor.
    """
    logger.info("Criando a tarefa para o agente leitor")
    return Task(
        description=(
            "Leia o PDF e responda em Markdown às solicitações definidas em <solicitacoes>, "
            "usando o modelo em <template>. {solicitacoes} {template}."
            "Utilize as funcionalidades suportadas pelo Obsidian para garantir uma apresentação visual rica."
        ),
        expected_output="MARKDOWN gerado com base nas solicitações definidas em <solicitacoes>, " 
        "usando o modelo definido em <template>.",
        agent=agent_leitor
    )

def revisor_task(agent_revisor):
    """
    Cria a tarefa do agente revisor, que é responsável por revisar o Markdown
    produzido pelo agente leitor, garantindo que o conteúdo esteja correto,
    bem formatado e adequado para uso no Obsidian.

    Parâmetros:
    - agent_revisor: O agente que realizará a revisão do Markdown.

    Retorna:
    - Task: Uma instância da tarefa que será atribuída ao agente revisor.
    """
    logger.info("Criando a tarefa para o agente revisor")
    return Task(
        description=(
            "Revise o Markdown produzido pelo agente leitor para garantir que o conteúdo esteja correto e bem formatado de acordo com o template definido em <template>."
            "Verificar se cada ferramenta de formatação do Obsidian como as listadas em <obsidianTolls> foi utilizada corretamente."
            "Verificar se o arquivo contem todas as informações solicitadas em <solicitacoes>"
            "e se todos os elementos de formatação estão prontos, bem formatados e visuais, "
            "explorando os recursos das ferramentas listadas em <obsidianTolls> mais as que forem necessarias e para tornar o conteudo mais rico visualmente."
        ),
        expected_output="Markdown revisado e validado, pronto para ser utilizado diretamente no Obsidian.",
        agent=agent_revisor
    )
