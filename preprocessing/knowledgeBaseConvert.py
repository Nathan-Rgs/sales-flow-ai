import json
import yaml
import logging
from pathlib import Path

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

def main():
    # Configuração do logger para informar erros e progresso
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Diretório base onde os documentos estão localizados
    base_dir = Path("C:/Users/natha/Desktop/FACENS/TCC/DocumentosJVF")
    
    # Define as extensões permitidas, mapeando os formatos suportados:
    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".docx",
        ".html",
        ".htm",
        ".pptx",
        ".asciidoc",
        ".adoc",
        ".csv",
        ".md",
    }
    
    # Coleta recursivamente os arquivos cujo sufixo esteja na lista de extensões permitidas
    input_paths = [
        file_path for file_path in base_dir.rglob('*') 
        if file_path.is_file() and file_path.suffix.lower() in allowed_extensions
    ]
    logger.info(f"Arquivos encontrados para processamento: {[str(p) for p in input_paths]}")
    
    # Configuração personalizada do conversor com os formatos permitidos e opções de processamento
    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE,
            InputFormat.DOCX,
            InputFormat.HTML,
            InputFormat.PPTX,
            InputFormat.ASCIIDOC,
            InputFormat.CSV,
            InputFormat.MD,
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline,
                backend=PyPdfiumDocumentBackend
            ),
            InputFormat.DOCX: WordFormatOption(
                pipeline_cls=SimplePipeline
            ),
        },
    )
    
    # Tenta converter todos os arquivos filtrados
    try:
        conv_results = doc_converter.convert_all(input_paths)
    except Exception as e:
        logger.error(f"Erro durante a conversão em lote: {e}")
        return

    # Cria o diretório de saída se ele não existir
    output_dir = Path("knowledge-base")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Processa cada resultado da conversão individualmente
    for res in conv_results:
        try:
            file_name = res.input.file.name
            file_stem = res.input.file.stem

            logger.info(f"Documento {file_name} convertido.")
            logger.info(f"Saída salva em: {output_dir}")

            # Exibe uma versão resumida do documento para depuração
            logger.debug(res.document._export_to_indented_text(max_text_len=16))
            
            # Exporta para Markdown
            markdown_output = res.document.export_to_markdown()
            md_path = output_dir / f"{file_stem}.md"
            with md_path.open("w", encoding="utf-8") as md_file:
                md_file.write(markdown_output)
            
            # Exporta para JSON
            json_output = json.dumps(res.document.export_to_dict(), indent=2, ensure_ascii=False)
            json_path = output_dir / f"{file_stem}.json"
            with json_path.open("w", encoding="utf-8") as json_file:
                json_file.write(json_output)
            
            # Exporta para YAML
            yaml_output = yaml.safe_dump(res.document.export_to_dict(), allow_unicode=True)
            yaml_path = output_dir / f"{file_stem}.yaml"
            with yaml_path.open("w", encoding="utf-8") as yaml_file:
                yaml_file.write(yaml_output)
        except Exception as file_error:
            logger.error(f"Erro ao processar {res.input.file}: {file_error}")

if __name__ == "__main__":
    main()
