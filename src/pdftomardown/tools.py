# tolls.py 
import logging
from crewai_tools import PDFSearchTool

logger = logging.getLogger(__name__)

def create_pdf_search_tool(pdf):
    """
    Cria e retorna uma instância de PDFSearchTool configurada para buscar dentro do PDF especificado.
    """
    logger.info(f"Criando ferramenta PDF para o arquivo: {pdf}")
    return PDFSearchTool(pdf=pdf)
