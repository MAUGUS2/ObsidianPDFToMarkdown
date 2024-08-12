# crew.py 
import logging
from crewai import Crew, Process

logger = logging.getLogger(__name__)

def create_crew(agent_leitor, task_leitor, agent_revisor, task_revisor):
    """
    Cria uma equipe (Crew) composta pelos agentes leitor e revisor, e define
    as tarefas que cada um deles deve realizar, seguindo um processo sequencial.

    Parâmetros:
    - agent_leitor: O agente responsável por ler e extrair informações do PDF.
    - task_leitor: A tarefa atribuída ao agente leitor.
    - agent_revisor: O agente responsável por revisar o conteúdo gerado.
    - task_revisor: A tarefa atribuída ao agente revisor.

    Retorna:
    - Crew: Uma instância configurada da equipe pronta para executar o processo.
    """
    logger.info("Criando a equipe (Crew) para processamento de PDFs")

    # Criação da Crew com os agentes e tarefas
    crew = Crew(
        agents=[agent_leitor, agent_revisor],  # Lista dos agentes que fazem parte da equipe
        tasks=[task_leitor, task_revisor],  # Lista das tarefas que cada agente irá realizar
        process=Process.sequential  # Definindo o processo como sequencial, onde as tarefas são realizadas uma após a outra
    )

    logger.info("Equipe (Crew) criada com sucesso")

    return crew
