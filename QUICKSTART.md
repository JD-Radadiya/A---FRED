# 🚀 Quick Start Guide

Get FRED up and running in 3 simple steps!

## Step 1: Install Dependencies

```bash
# Option A: Use the quick start script (recommended)
./run.sh

# Option B: Manual installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Launch the App

```bash
# If you used run.sh, the app is already running!

# Otherwise, run:
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 3: Configure & Use

### In the Sidebar:
1. **Enter API Keys**
   - TAMU AI API Key
   - ElevenLabs API Key
   - Click "Save API Keys"

2. **Clone Your Voice** (Optional)
   - Enter a voice name
   - Upload 1-3 audio samples (30s-5min each)
   - Click "Clone Voice"

### In the Main Area:
1. **Select Files**
   - Choose a knowledge base
   - Select one or more files

2. **Configure Prompts**
   - Set system prompt (AI's role)
   - Set user prompt (your question)

3. **Process**
   - Click "Process Files"
   - Wait for results

4. **Download**
   - Download Word documents
   - Generate audio with emotions
   - Download audio files

## Tips

- 📝 **Word Documents**: One file per processed document
- 🎵 **Audio**: Generate on-demand with different emotions
- 📊 **History**: Check the History tab to see all processed files
- 🔍 **Logs**: Check `logs/` folder for debugging

## Troubleshooting

**App won't start?**
```bash
# Make sure you're in the right directory
cd /Users/jaydeepradadiya/Documents/GitHub/A---FRED

# Activate virtual environment
source venv/bin/activate

# Try running again
streamlit run app.py
```

**API errors?**
- Check your API keys are correct
- Ensure you have credits/quota available
- Check the logs in `logs/` folder

**Voice cloning not working?**
- Use clear audio samples
- Upload 1-3 files
- Each file should be 30s-5min
- Supported formats: mp3, wav, m4a

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
