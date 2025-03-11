# main.py
from utils.transcription import transcribe_with_diarization
from utils.imports import asyncio, logging
from utils.audio import extract_audio

async def main():
    """
    Função principal que realiza o processo completo de extração de áudio, transcrição e diarização de um vídeo.

    Passos realizados:
    1. Extrai o áudio de um vídeo MP4 especificado no diretório `resources/` usando a função `extract_audio`.
    2. Caso a extração do áudio seja bem-sucedida, realiza a transcrição do áudio usando o método `transcribe_with_diarization`, que inclui a identificação dos falantes.
    3. Para cada segmento de áudio transcrito, gera uma representação textual que inclui:
       - O identificador do falante.
       - O texto transcrito.
       - O tempo de início e fim do segmento (em minutos).
       - Um separador visual entre os segmentos.
    4. A transcrição é salva em um arquivo de texto (`transcription_{video_name}.txt`) no diretório `resources/`.
    
    Exceções tratadas:
    - Se o áudio não for extraído com sucesso, um erro é registrado.
    - Se a transcrição falhar ou não gerar resultados, um erro é registrado.
    - Caso haja problemas ao salvar o arquivo de transcrição, o erro é capturado e registrado.

    Requisitos:
    - Funções auxiliares como `extract_audio` e `transcribe_with_diarization` devem estar corretamente implementadas e disponíveis no módulo `Utils.utils`.
    - O arquivo de vídeo (`{video_name}.mp4`) deve estar presente no diretório `resources/`.

    Parâmetros:
    Nenhum. A função opera com um nome de vídeo hardcoded (`discussao_senado`).

    Retorna:
    Nenhum. A função realiza operações assíncronas de extração, transcrição e salvamento de dados.
    """
    video_name = "Como divulgar as informações geradas pelo observatório_190424"
    logging.info("Iniciando extração de áudio...")

    audio_file = await extract_audio(f"resources/{video_name}.mp4")

    if audio_file:
        logging.info("Áudio extraído com sucesso! Iniciando transcrição...")
        result = await transcribe_with_diarization(audio_file)

        if result:
            logging.info("Transcrição concluída. Escrevendo segmentos...")
            transcription = ""
            for sentence in result['segments']:
                start_min = sentence["start"] / 60
                end_min = sentence["end"] / 60
                transcription += "\n".join([f"🔉 Falante: {sentence['speaker']}",
                                            f"📄 Frase: {sentence['text']}",
                                            f"⏳ Início: {start_min:.2f} min",
                                            f"⏳ Fim: {end_min:.2f} min",
                                            "-" * 40]) + "\n"
            try:
                with open(f"resources/transcription_{video_name}.txt", "w", encoding="utf-8") as arq:
                    arq.write(transcription)
                logging.info("Arquivo de transcrição salvo com sucesso!")
            except Exception as e:
                logging.error(f"Erro ao salvar arquivo: {e}")
        else:
            logging.error("❌ Falha na transcrição. Não foi possível obter resultados.")
    else:
        logging.error("❌ Falha na extração do áudio. Arquivo de áudio não encontrado.")

asyncio.run(main())
