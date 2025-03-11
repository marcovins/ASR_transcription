# utils/memory.py
from utils.imports import gc, torch, logging, Optional, os, shutil

async def clean_memory(device: str, model: Optional[object] = None) -> None:
    """
    Limpa a memória do sistema, remove modelos carregados e apaga arquivos da pasta temp.

    A função realiza a coleta de lixo para liberar memória no sistema e, caso a execução esteja em um dispositivo CUDA 
    (GPU), também limpa a memória da GPU. Além disso, se um modelo for fornecido, ele será removido da memória. 
    Também apaga todos os arquivos da pasta temporária `temp`.

    Parâmetros:
        device (str): O dispositivo em que o modelo está sendo executado, podendo ser "cpu" ou "cuda".
        model (object, opcional): O modelo carregado que deve ser removido da memória. O valor padrão é None.

    Retorno:
        None: Não retorna nenhum valor. A função apenas executa ações de limpeza na memória.

    Observações:
        - O parâmetro `device` deve ser "cpu" ou "cuda". Se for "cuda", a função tentará limpar a memória da GPU.
        - A função deve ser chamada após a execução de tarefas de transcrição ou alinhamento para garantir que a memória seja liberada adequadamente.

    Exemplo:
        await clean_memory("cuda", model)
        # Libera memória na GPU, remove o modelo e apaga arquivos da pasta temp.

    Possíveis erros:
        - Não há erros previstos, mas é importante garantir que a variável `model` seja válida antes de removê-la da memória.

    """
    gc.collect()

    if device == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        logging.info("🚀 Memória da GPU limpa!")

    if model:  # Só deleta o modelo se ele foi carregado
        del model
        logging.info("🧹 Modelo removido da memória.")

    # Apagar arquivos da pasta temp
    temp_dir = "temp"  # Diretório temporário onde os arquivos serão apagados

    try:
        if os.path.exists(temp_dir):
            # Itera sobre os arquivos na pasta e apaga cada um
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"🗑️ Arquivo removido: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.info(f"🗑️ Pasta removida: {file_path}")
            logging.info("🧹 Arquivos da pasta 'temp' apagados com sucesso!")
        else:
            logging.warning(f"A pasta '{temp_dir}' não foi encontrada.")
    except Exception as e:
        logging.error(f"Erro ao limpar a pasta 'temp': {e}")
