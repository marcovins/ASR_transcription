<div align="center">
  <h1>🎤 Projeto de Transcrição e Diarização de Áudio</h1>
  <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWN0MTBwMmFpeGl2cjJmZ2VwZnQweDFleWtyNmkwOHVmeHRxNG4zdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/X0iqiPHFdrEctzDKMU/giphy.gif" alt="Transcrição em ação">
</div>

<div align="center">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-orange" alt="Build Status"> 
  <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Dependencies-Required-brightgreen" alt="Dependencies">
  <img src="https://img.shields.io/badge/Hugging%20Face-Access-orange" alt="Hugging Face">
</div>


## 📌 Descrição
Este projeto tem como objetivo realizar a extração de áudio de um vídeo, transcrevê-lo utilizando o modelo WhisperX e identificar diferentes falantes (diarização). O resultado final é um arquivo de texto contendo a transcrição organizada e identificada por falante.

## 🚀 Funcionalidades
✅ Extração de áudio de arquivos MP4.  
✅ Transcrição automática do áudio extraído.  
✅ Diarização para identificar diferentes falantes.  
✅ Geração de um arquivo de transcrição formatado.


## 📂 Estrutura do Projeto
```
/
│   .gitignore
│   ffmpeg.exe
│   ffplay.exe
│   ffprobe.exe
│   LICENSE
│   main.py
│   README.md
│   requirements.txt
││
├───cache
│       removePycache.ps1
│
├───model
│   ├───.locks
│   │   └───models--Systran--faster-whisper-small
│   └───models--Systran--faster-whisper-small
│       ├───blobs
│       ├───refs
│       │       main
│       │
│       └───snapshots
│           └───536b0662742c02347bc0e980a01041f333bce120
│                   config.json
│                   model.bin
│                   tokenizer.json
│                   vocabulary.txt
│
├───resources
│       📹 [Flow](resources/flow.mp4)
│       📄 [Transcrição gerada](resources/transcription_flow.txt)
│
├───temp
└───utils
        audio.py
        device.py
        imports.py
        memory.py
        transcription.py
```

## 🔧 Requisitos
🛠 Python 3.12 ou superior.<br>
🛠 Dependências: Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`.<br>
🛠 WhisperX: Biblioteca para transcrição de áudio.<br>
🛠 MoviePy e Pydub: Para manipulação de áudio e vídeo.<br>
🛠 Chave da Hugging Face: Necessária para acessar modelos pré-treinados.<br>

## 📥 Instalação
1️⃣ Clone o repositório:
   ```bash
   git clone https://github.com/marcosbelo-fiepb/automated-speech-recognition.git
   cd automated-speech-recognition
   ```
2️⃣ Instale as dependências com pip:
   ```bash
   pip install -r requirements.txt
   ```
3️⃣ Configure a chave de autenticação da Hugging Face:

- Crie um arquivo `.env` na raiz do projeto e adicione:
   ```bash
   HUGGING=<sua-chave-hugging-face>
   ```
- Ou exporte a variável de ambiente no terminal:
   ```bash
   export HUGGING=<sua-chave-hugging-face>
   ```

## ▶️ Execução
Para iniciar o processo de transcrição e diarização, execute o script principal:
```bash
python -m main
```

## 📜 Exemplo de Saída
```
🔉 Falante: Speaker_1
📄 Frase: Bom dia a todos.
⏳ Início: 0.05 min
⏳ Fim: 0.10 min
----------------------------------------
🔉 Falante: Speaker_2
📄 Frase: Vamos começar a reunião.
⏳ Início: 0.12 min
⏳ Fim: 0.18 min
----------------------------------------
```

📂 [Clique aqui para visualizar um exemplo de transcrição completa](resources/transcription_flow.txt)<br>
📂 [Clique aqui para visualizar o vídeo original](resources/flow.mp4)

## ❗ Possíveis Erros e Soluções
❌ **Erro ao carregar o modelo**: Verifique se a chave da Hugging Face está configurada corretamente.
❌ **Erro ao extrair o áudio**: Confirme que o arquivo MP4 está na pasta `resources/`.
❌ **Alto consumo de memória**: Certifique-se de rodar a limpeza de memória após a execução.

## 🤝 Contribuição
Contribuições são bem-vindas! Siga os passos abaixo:

1️⃣ Faça um fork do repositório.

2️⃣ Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-feature
   ```

3️⃣ Commit suas alterações:
   ```bash
   git commit -m 'Adiciona nova feature'
   ```

4️⃣ Envie para a branch:
   ```bash
   git push origin feature/nova-feature
   ```

5️⃣ Abra um Pull Request.

Para relatar problemas, acesse a seção [Issues](https://github.com/marcosbelo-fiepb/automated-speech-recognition/issues).

## 📜 Licença
Este projeto está licenciado sob a MIT License. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato
👤 **Autor**: Marcos Belo
📧 **E-mail**: [marcosbelods@gmail.com](mailto:marcosbelods@gmail.com)