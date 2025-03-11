# utils/audio.py
from utils.imports import Optional, os, VideoFileClip, AudioSegment, logging, BASE_PATH


async def extract_audio(path: str) -> Optional[str]:
    """
    Extrai o áudio de um arquivo de vídeo (MP4) e o converte para o formato WAV.
    A função recebe o caminho para um arquivo de vídeo MP4, extrai o áudio, converte-o para o formato WAV,
    e salva o arquivo processado em um diretório predefinido. Se houver algum erro durante o processo, 
    um log será gerado e a função retornará `None`.

    Parâmetros:
        path (str): O caminho para o arquivo de vídeo MP4 do qual o áudio será extraído.

    Retorno:
        Optional[str]: Retorna o caminho do arquivo de áudio processado em formato WAV se a extração for bem-sucedida.
        Caso contrário, retorna `None` em caso de erro.

    Exemplo:
        audio_path = await extract_audio("video.mp4")
        if audio_path:
            print(f"Áudio extraído e salvo em: {audio_path}")
        else:
            print("Erro na extração do áudio.")
    
    Observações:
        O arquivo de áudio extraído será salvo como `processed_audio.wav` no diretório especificado por `BASE_PATH`.
        Caso não exista o arquivo no caminho fornecido, a função retorna `None` e gera um log de erro.
    """
    if not os.path.exists(path):
        logging.error(f"Arquivo {path} não encontrado")
        return None

    try:
        clip = VideoFileClip(path)
        clip.audio.write_audiofile(f"{BASE_PATH}audio.mp3")
        sound = AudioSegment.from_mp3(f"{BASE_PATH}audio.mp3")
        sound = sound.set_channels(1).set_frame_rate(16000)
        output_path = f"{BASE_PATH}processed_audio.wav"
        sound.export(output_path, format="wav")
        logging.info("🎙️ Áudio extraído com sucesso")
        return output_path
    except Exception as e:
        logging.error(f"Erro na extração de áudio: {e}")
        return None
    