# utils/transcription.py
from utils.imports import whisperx, logging, Union, AlignedTranscriptionResult, TranscriptionResult, DiarizationPipeline, HUGGINGFACE_KEY, assign_word_speakers
from utils.memory import clean_memory, del_wav
from utils.device import get_device

async def transcribe(audio_path: str, model_path: str = "model", align: bool = False) -> Union[TranscriptionResult, AlignedTranscriptionResult]:
    """
    Realiza a transcrição de áudio usando o modelo WhisperX e oferece suporte opcional para alinhamento de transcrição.

    A função carrega o modelo WhisperX a partir de um diretório local ou remoto, realiza a transcrição do áudio
    fornecido e, se solicitado, alinha a transcrição com o áudio para fornecer timestamps mais precisos.

    Parâmetros:
        audio_path (str): O caminho para o arquivo de áudio que será transcrito.
        model_path (str, opcional): O diretório local onde o modelo WhisperX está armazenado. O valor padrão é "model".
        align (bool, opcional): Define se o áudio deve ser alinhado para fornecer timestamps mais precisos. O valor padrão é False.

    Retorno:
        Union[TranscriptionResult, AlignedTranscriptionResult, None]:
            - Se `align` for False, retorna um `TranscriptionResult` com o texto transcrito.
            - Se `align` for True, retorna um `AlignedTranscriptionResult` com a transcrição alinhada e timestamps.
            - Retorna `None` em caso de erro durante a transcrição ou alinhamento.

    Exemplo:
        result = await transcribe("audio_file.wav", align=True)
        if result:
            print(result['text'])
        else:
            print("Erro na transcrição")

    Observações:
        - O modelo utilizado é configurado para a língua portuguesa ("pt") e a arquitetura "small".
        - A função utiliza a GPU, se disponível, ou a CPU se não houver GPU.
        - A função limpa a memória após a execução, removendo o modelo carregado.

    Possíveis erros:
        - Arquivo de áudio não encontrado ou com formato inválido.
        - Erro ao carregar o modelo ou realizar a transcrição.
    """
    device = get_device()
    model = None
    try:
        model = whisperx.load_model(
            whisper_arch="small",  
            device=device,          
            compute_type="float32", 
            language="pt",          
            download_root=model_path,
        )
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=16, language="pt")

        if align:
            result = await align_audio(result, audio, device)
        return result
    except Exception as e:
        logging.error(f"Erro na transcrição: {e}")
        return None
    finally:
        if model:
            await clean_memory(device, model)

async def align_audio(data, audio, device) -> AlignedTranscriptionResult:
    """
    Realiza o alinhamento da transcrição com o áudio, retornando transcrição alinhada com timestamps precisos.

    A função usa o modelo de alinhamento do WhisperX para alinhar os segmentos transcritos com o áudio, proporcionando
    uma transcrição com maior precisão nos timestamps, o que é útil para tarefas de diarização e análise de áudio.

    Parâmetros:
        data (dict): Um dicionário contendo a transcrição e segmentos de áudio. Espera-se que o dicionário tenha
                     uma chave 'language' com o código do idioma e 'segments' com os segmentos transcritos.
        audio (np.ndarray): O áudio a ser alinhado com os segmentos de texto. Este é o áudio original carregado.
        device (str): O dispositivo (CPU ou CUDA) no qual o modelo de alinhamento será carregado e executado.

    Retorno:
        AlignedTranscriptionResult: O resultado do alinhamento, que inclui os segmentos de transcrição com timestamps
                                    mais precisos e outras informações relacionadas ao alinhamento.
        None: Caso ocorra um erro durante o processo de alinhamento.

    Exemplo:
        aligned_result = await align_audio(transcription_data, audio_data, "cuda")
        if aligned_result:
            print(aligned_result)
        else:
            print("Erro no alinhamento da transcrição")

    Observações:
        - A função carrega e usa o modelo de alinhamento do WhisperX, adequado ao idioma especificado.
        - O modelo e os metadados são carregados no dispositivo especificado (CPU ou GPU).
        - A função realiza o alinhamento dos segmentos de texto com o áudio original.

    Possíveis erros:
        - Erro ao carregar o modelo de alinhamento ou ao realizar o alinhamento dos segmentos.
    """
    try:
        model, metadata = whisperx.load_align_model(language_code=data["language"], device=device)
        result = whisperx.align(data["segments"], model, metadata, audio, device, return_char_alignments=False)
        return result
    except Exception as e:
        logging.error(f"Erro no alinhamento: {e}")
        return None

async def transcribe_with_diarization(audio_path: str, model_path: str = "model", align: bool = False) -> dict:
    """
    Realiza a transcrição de áudio com diarização de falantes, retornando uma transcrição com identificação de falantes.

    A função primeiro transcreve o áudio usando um modelo WhisperX, e em seguida realiza a diarização utilizando o pipeline 
    de diarização do Hugging Face. O resultado é uma transcrição associada a falantes específicos, permitindo a identificação 
    de quem está falando em diferentes momentos do áudio.

    Parâmetros:
        audio_path (str): O caminho para o arquivo de áudio que será transcrito e diarizado.
        model_path (str, opcional): O caminho onde o modelo de transcrição está armazenado. O valor padrão é "model".
        align (bool, opcional): Se True, ativa o alinhamento da transcrição com o áudio. O valor padrão é False.

    Retorno:
        dict: Um dicionário contendo a transcrição com identificação dos falantes, onde cada segmento de texto é associado
              a um falante. Caso ocorra um erro ou falha no processo, retorna None.

    Exemplo:
        transcription_with_speakers = await transcribe_with_diarization("audio.wav", "model_path", align=True)
        if transcription_with_speakers:
            print(transcription_with_speakers)
        else:
            print("Erro na transcrição ou diarização")

    Observações:
        - A função usa a API de diarização do Hugging Face, requerendo um token de autenticação para acesso.
        - A transcrição será enriquecida com os falantes identificados, retornando um resultado com segmentos rotulados.

    Possíveis erros:
        - Erro na transcrição do áudio ou na diarização.
    """
    transcription = await transcribe(audio_path, model_path, align)
    if transcription:
        diarization = DiarizationPipeline(use_auth_token=HUGGINGFACE_KEY, device=get_device())
        diarize_df = diarization(audio_path)
        transcription = assign_word_speakers(diarize_df, transcription)
        await del_wav()
        return transcription
    return None
