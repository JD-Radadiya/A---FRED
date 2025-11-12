# 🚀 Getting Started with FRED

Welcome to **FRED** - File Response & Emotion-based Delivery!

## 📋 What You've Got

Your complete MVP includes:

### 🐍 Python Modules (4 files)
- **app.py** - Main Streamlit application with clean UI
- **tamu_client.py** - TAMU Chat API integration
- **elevenlabs_client.py** - Voice cloning & TTS with emotions
- **utils.py** - Document generation & logging utilities

### 📚 Documentation (6 files)
- **README.md** - Complete setup and usage guide
- **QUICKSTART.md** - 3-step quick start
- **ARCHITECTURE.md** - System design & data flow
- **PROJECT_SUMMARY.md** - Feature overview
- **TESTING_CHECKLIST.md** - Comprehensive testing guide
- **GETTING_STARTED.md** - This file!

### ⚙️ Configuration (4 files)
- **requirements.txt** - Python dependencies
- **run.sh** - One-command launcher
- **.gitignore** - Git ignore rules
- **.env.example** - Environment template

## 🎯 Your First Run (3 Steps)

### Step 1: Install
```bash
cd /Users/jaydeepradadiya/Documents/GitHub/A---FRED
./run.sh
```

That's it! The script will:
- Create virtual environment
- Install all dependencies
- Launch the app

### Step 2: Configure (in the app)
1. **Enter API Keys** (in sidebar)
   - TAMU AI API Key
   - ElevenLabs API Key
   - Click "Save API Keys"

2. **Clone Your Voice** (optional but recommended)
   - Enter voice name
   - Upload 1-3 audio samples
   - Click "Clone Voice"

### Step 3: Process Files
1. Select knowledge base
2. Select files
3. Configure prompts
4. Click "Process Files"
5. Download Word docs & generate audio!

## 🎨 What Makes FRED Special

### ✨ Key Features
- **Batch Processing**: Handle multiple files at once
- **Voice Cloning**: Use YOUR voice for audio
- **7 Emotions**: neutral, happy, sad, angry, fearful, disgusted, surprised
- **Clean UI**: Minimalistic Texas A&M themed design
- **Session-Based**: Secure, no data persistence
- **Full Logging**: Debug-friendly error tracking

### 🔒 Security First
- API keys stored in session only
- Cleared on browser close
- Never logged or saved to disk
- Sanitized file operations

## 📊 Project Stats

```
Total Files: 15
Python Code: ~1,000+ lines
Documentation: ~500+ lines
Modules: 4
API Integrations: 2
Supported Emotions: 7
Output Formats: 2 (DOCX, MP3)
```

## 🗂️ File Organization

```
A---FRED/
│
├── 🐍 Core Application
│   ├── app.py                    # Main UI (450+ lines)
│   ├── tamu_client.py            # TAMU API (250+ lines)
│   ├── elevenlabs_client.py      # ElevenLabs (150+ lines)
│   └── utils.py                  # Utilities (100+ lines)
│
├── 📚 Documentation
│   ├── README.md                 # Full guide
│   ├── QUICKSTART.md            # Quick start
│   ├── ARCHITECTURE.md          # System design
│   ├── PROJECT_SUMMARY.md       # Overview
│   ├── TESTING_CHECKLIST.md     # Testing guide
│   └── GETTING_STARTED.md       # This file
│
├── ⚙️ Configuration
│   ├── requirements.txt          # Dependencies
│   ├── run.sh                    # Launcher
│   ├── .gitignore               # Git rules
│   └── .env.example             # Env template
│
├── 📓 Notebooks
│   └── TAMU_CHAT_ENDPOINT.ipynb # API exploration
│
└── 📁 Auto-Generated
    ├── logs/                     # Application logs
    └── outputs/                  # Generated files
        ├── *.docx               # Word documents
        └── *.mp3                # Audio files
```

## 🎓 Learning Path

### New to the Project?
1. Read **QUICKSTART.md** (2 min)
2. Run the app with `./run.sh`
3. Try processing one file
4. Check **README.md** for details

### Want to Understand the Code?
1. Read **ARCHITECTURE.md**
2. Review `app.py` for UI logic
3. Check `tamu_client.py` for API calls
4. Look at `elevenlabs_client.py` for audio

### Ready to Test?
1. Use **TESTING_CHECKLIST.md**
2. Test each feature systematically
3. Check logs in `logs/` directory
4. Report issues or improvements

### Want to Extend?
1. Review **ARCHITECTURE.md** for design
2. Add features to respective modules
3. Update documentation
4. Test thoroughly

## 🔧 Common Tasks

### Start the App
```bash
./run.sh
# or
streamlit run app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Check Logs
```bash
ls -lt logs/
tail -f logs/app_*.log
```

### Clean Outputs
```bash
rm -rf outputs/*
rm -rf logs/*
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## 🐛 Troubleshooting

### App Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for errors
streamlit run app.py --logger.level=debug
```

### API Errors
- Verify API keys are correct
- Check API quotas/credits
- Review logs in `logs/` directory
- Test API keys in notebook first

### Voice Cloning Issues
- Use clear audio (minimal background noise)
- Upload 1-3 samples
- Each sample: 30 seconds to 5 minutes
- Supported formats: mp3, wav, m4a

### Import Errors
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

## 📞 Need Help?

### Check These First
1. **Logs**: `logs/app_*.log`
2. **README.md**: Full documentation
3. **TESTING_CHECKLIST.md**: Verify setup
4. **ARCHITECTURE.md**: Understand design

### Debug Mode
```bash
# Run with debug logging
streamlit run app.py --logger.level=debug
```

## 🎯 Next Steps

### Immediate
- [ ] Run the app
- [ ] Configure API keys
- [ ] Clone your voice
- [ ] Process a test file
- [ ] Generate audio with emotions

### Short Term
- [ ] Process multiple files
- [ ] Try different emotions
- [ ] Explore different prompts
- [ ] Test with various file types
- [ ] Review processing history

### Long Term
- [ ] Consider database integration
- [ ] Add user authentication
- [ ] Implement parallel processing
- [ ] Add more export formats
- [ ] Deploy to cloud

## 🌟 Pro Tips

1. **Voice Samples**: Use consistent audio quality for best results
2. **Prompts**: Be specific for better AI responses
3. **Batch Size**: Start with 2-3 files, then scale up
4. **Emotions**: Experiment with different emotions for same text
5. **History**: Use history tab to regenerate audio with different emotions
6. **Logs**: Check logs regularly during development
7. **Session**: Remember to save important outputs before closing browser

## 📈 Success Metrics

You'll know FRED is working when:
- ✅ App launches without errors
- ✅ API keys save successfully
- ✅ Voice clones successfully
- ✅ Files process without errors
- ✅ Word documents download correctly
- ✅ Audio generates with emotions
- ✅ History tracks all processing

## 🎉 You're Ready!

Everything is set up and ready to go. Just run:

```bash
./run.sh
```

And start processing files with emotional AI responses!

---

**Questions?** Check the documentation files or review the logs.

**Found a bug?** Check TESTING_CHECKLIST.md and logs/ directory.

**Want to contribute?** Review ARCHITECTURE.md for design patterns.

**Happy Processing! 🎙️**
