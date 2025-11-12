# FRED - File Response & Emotion-based Delivery

A clean, minimalistic web application for processing files with TAMU Chat API and generating emotional audio responses using ElevenLabs voice cloning.

## Features

- 🎯 **Batch File Processing**: Process multiple files from TAMU knowledge bases with custom prompts
- 🎙️ **Voice Cloning**: Clone your voice using ElevenLabs v3 model
- 😊 **Emotional Audio**: Generate audio with 7 different emotions (neutral, happy, sad, angry, fearful, disgusted, surprised)
- 📄 **Word Export**: Download AI responses as formatted Word documents
- 📊 **Session History**: Track all processed files in your current session
- 🔒 **Secure**: API keys stored only in session state
- 📝 **Logging**: Comprehensive error logging for debugging

## Prerequisites

- Python 3.8 or higher
- TAMU AI API key
- ElevenLabs API key

## Installation

1. **Clone the repository**
   ```bash
   cd /Users/jaydeepradadiya/Documents/GitHub/A---FRED
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API Keys**
   - Enter your TAMU AI API key in the sidebar
   - Enter your ElevenLabs API key in the sidebar
   - Click "Save API Keys"

3. **Clone Your Voice** (Optional but recommended for audio generation)
   - Enter a name for your voice
   - Upload 1-3 audio samples (30 seconds to 5 minutes each)
   - Click "Clone Voice"

4. **Process Files**
   - Select a knowledge base from the dropdown
   - Select one or more files to process
   - Configure your system and user prompts
   - Adjust model settings if needed
   - Click "Process Files"

5. **Download Results**
   - Download Word documents with AI responses
   - Generate and download audio with different emotions

## Project Structure

```
A---FRED/
├── app.py                      # Main Streamlit application
├── tamu_client.py              # TAMU Chat API client
├── elevenlabs_client.py        # ElevenLabs API client
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TAMU_CHAT_ENDPOINT.ipynb   # API exploration notebook
├── logs/                       # Application logs (auto-created)
└── outputs/                    # Generated files (auto-created)
    ├── *.docx                  # Word documents
    └── *.mp3                   # Audio files
```

## API Clients

### TAMU Client (`tamu_client.py`)
- List knowledge bases and files
- Upload files to knowledge bases
- Chat completions with knowledge base context
- Model management

### ElevenLabs Client (`elevenlabs_client.py`)
- Voice cloning from audio samples
- Text-to-speech with emotion control
- Support for 7 emotions using v3 model
- Voice management

## Supported Emotions

The ElevenLabs v3 model supports the following emotions:
- Neutral
- Happy
- Sad
- Angry
- Fearful
- Disgusted
- Surprised

## Logging

- Logs are stored in the `logs/` directory
- Each session creates a new log file with timestamp
- Error-level logging is enabled by default
- Logs include timestamps, module names, and detailed error traces

## Troubleshooting

### API Key Issues
- Ensure your API keys are valid and have sufficient credits
- Check that you've clicked "Save API Keys" after entering them

### Voice Cloning Issues
- Upload high-quality audio samples (clear voice, minimal background noise)
- Use 1-3 samples, each 30 seconds to 5 minutes long
- Ensure audio files are in supported formats (mp3, wav, m4a)

### File Processing Issues
- Verify the knowledge base contains the files you're trying to process
- Check the logs in the `logs/` directory for detailed error messages
- Ensure your TAMU API key has access to the selected knowledge base

## Development

To modify or extend the application:

1. **Add new features**: Edit `app.py` for UI changes
2. **Extend API clients**: Modify `tamu_client.py` or `elevenlabs_client.py`
3. **Add utilities**: Update `utils.py` for helper functions
4. **Test changes**: Run the app locally with `streamlit run app.py`

## Security Notes

- API keys are stored in session state only (not persisted to disk)
- Keys are cleared when you close the browser tab
- For production use, consider implementing proper authentication and key management

## License

This project is for educational and research purposes.

## Support

For issues or questions:
1. Check the logs in the `logs/` directory
2. Review the TAMU Chat API documentation
3. Review the ElevenLabs API documentation

## Acknowledgments

- Texas A&M University for the TAMU Chat API
- ElevenLabs for voice cloning and TTS technology
- Streamlit for the web framework
