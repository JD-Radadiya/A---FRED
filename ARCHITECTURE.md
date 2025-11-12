# FRED Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FRED Web Application                    │
│                        (Streamlit)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ TAMU Client  │    │  ElevenLabs  │    │   Utils      │
│              │    │   Client     │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  TAMU Chat   │    │  ElevenLabs  │    │  File System │
│     API      │    │     API      │    │   (outputs)  │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Component Details

### 1. Main Application (`app.py`)
**Responsibilities:**
- User interface rendering
- Session state management
- Workflow orchestration
- Error handling and display

**Key Features:**
- Sidebar for configuration
- Main tabs for processing and history
- Real-time progress tracking
- Download management

### 2. TAMU Client (`tamu_client.py`)
**Responsibilities:**
- TAMU Chat API integration
- Knowledge base management
- File operations
- Chat completions

**Key Methods:**
- `list_knowledge_bases()`: Get all KBs
- `get_file_id_from_kb()`: Locate files
- `chat_with_kb_file()`: Process files with AI
- `upload_file()`: Upload new files

### 3. ElevenLabs Client (`elevenlabs_client.py`)
**Responsibilities:**
- Voice cloning
- Text-to-speech generation
- Emotion control
- Voice management

**Key Methods:**
- `clone_voice()`: Create voice from samples
- `generate_audio()`: TTS with emotions
- `list_voices()`: Get available voices
- `delete_voice()`: Remove cloned voices

**Supported Emotions:**
- neutral, happy, sad, angry, fearful, disgusted, surprised

### 4. Utilities (`utils.py`)
**Responsibilities:**
- Document generation
- Logging setup
- File operations
- Helper functions

**Key Functions:**
- `create_word_document()`: Generate .docx files
- `setup_logging()`: Configure logging
- `sanitize_filename()`: Clean filenames
- `format_file_size()`: Human-readable sizes

## Data Flow

### File Processing Flow
```
1. User selects KB & files
        ↓
2. User configures prompts
        ↓
3. User clicks "Process Files"
        ↓
4. For each file:
   a. Get file_id from KB
   b. Augment prompts with file info
   c. Call TAMU Chat API
   d. Receive AI response
   e. Create Word document
   f. Add to session history
        ↓
5. Display results with download options
```

### Audio Generation Flow
```
1. User uploads voice samples
        ↓
2. Clone voice via ElevenLabs
        ↓
3. Store voice_id in session
        ↓
4. User selects emotion
        ↓
5. User clicks "Generate Audio"
        ↓
6. Generate TTS with emotion
        ↓
7. Save audio file
        ↓
8. Provide playback & download
```

## Session State Management

### Stored in `st.session_state`:
- `api_keys_set`: Boolean flag
- `tamu_api_key`: TAMU API key (session only)
- `elevenlabs_api_key`: ElevenLabs API key (session only)
- `processing_history`: List of processed files
- `voice_id`: Cloned voice ID
- `voice_cloned`: Boolean flag

### Security:
- Keys stored in memory only
- Cleared on browser close
- Not persisted to disk
- Not logged

## File Structure

```
outputs/
├── {filename}_{timestamp}.docx    # Word documents
└── {filename}_{emotion}_{timestamp}.mp3  # Audio files

logs/
└── app_{timestamp}.log            # Application logs
```

## Error Handling

### Levels:
1. **User-facing**: Streamlit error/warning messages
2. **Logging**: Detailed error logs with stack traces
3. **Graceful degradation**: Continue processing other files on error

### Logged Events:
- API calls (INFO)
- File operations (INFO)
- Errors with full stack traces (ERROR)
- Voice cloning operations (INFO)
- Audio generation (INFO)

## API Integration

### TAMU Chat API
- **Base URL**: `https://chat-api.tamu.ai`
- **OpenAI Compatible**: `/openai/chat/completions`
- **Authentication**: Bearer token
- **Features**: Knowledge bases, file management, chat

### ElevenLabs API
- **SDK**: `elevenlabs` Python package
- **Model**: Turbo v2.5 (supports emotions)
- **Features**: Voice cloning, TTS, emotion control
- **Authentication**: API key

## Performance Considerations

### Optimization:
- Progress bars for long operations
- Spinner indicators for API calls
- Batch processing with status updates
- Efficient file handling

### Limitations:
- Session-based storage (no persistence)
- Sequential file processing
- API rate limits apply
- Memory constraints for large files

## Future Enhancements

Potential improvements:
- [ ] Persistent storage (database)
- [ ] User authentication
- [ ] Parallel file processing
- [ ] Custom emotion mixing
- [ ] Batch audio generation
- [ ] Export to other formats (PDF, TXT)
- [ ] Advanced prompt templates
- [ ] File upload to KB from UI
- [ ] Voice sample preview
- [ ] Audio editing capabilities
