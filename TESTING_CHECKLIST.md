# FRED Testing Checklist

Use this checklist to verify all features are working correctly.

## ✅ Pre-Testing Setup

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] TAMU AI API key available
- [ ] ElevenLabs API key available
- [ ] At least one knowledge base with files in TAMU
- [ ] 1-3 voice sample files ready (mp3/wav/m4a, 30s-5min each)

## 🔧 Initial Setup Tests

### API Key Configuration
- [ ] App launches successfully (`streamlit run app.py`)
- [ ] Sidebar displays API key input fields
- [ ] Can enter TAMU API key
- [ ] Can enter ElevenLabs API key
- [ ] "Save API Keys" button works
- [ ] Success message appears after saving
- [ ] Warning appears if keys are missing

### Voice Cloning
- [ ] Voice cloning section appears after API keys saved
- [ ] Can enter voice name
- [ ] Can upload single voice sample
- [ ] Can upload multiple voice samples (2-3)
- [ ] "Clone Voice" button works
- [ ] Success message with voice ID appears
- [ ] Voice status shows as ready
- [ ] Error handling for invalid audio files

## 📁 File Processing Tests

### Knowledge Base Selection
- [ ] Knowledge bases load in dropdown
- [ ] Can select a knowledge base
- [ ] Files from selected KB appear in multiselect
- [ ] Can select single file
- [ ] Can select multiple files
- [ ] Empty KB shows appropriate message

### Prompt Configuration
- [ ] System prompt text area works
- [ ] User prompt text area works
- [ ] Default prompts are pre-filled
- [ ] Can modify prompts
- [ ] Prompts persist during session

### Model Settings
- [ ] Model dropdown shows available models
- [ ] Can select different models
- [ ] Temperature slider works (0.0 - 1.0)
- [ ] Default temperature is 0.2

### Processing
- [ ] "Process Files" button is visible
- [ ] Warning appears if no files selected
- [ ] Progress bar appears during processing
- [ ] Status text updates for each file
- [ ] Success message for each processed file
- [ ] Results expand automatically
- [ ] File name, KB name, and model displayed
- [ ] AI response is readable and formatted

## 📄 Document Generation Tests

### Word Documents
- [ ] "Download Word Document" button appears
- [ ] Clicking downloads a .docx file
- [ ] File name includes sanitized original name
- [ ] File name includes timestamp
- [ ] Document opens correctly in Word/LibreOffice
- [ ] Document contains title
- [ ] Document contains timestamp
- [ ] Document contains AI response
- [ ] Document formatting is clean
- [ ] Multiple files generate separate documents

## 🎵 Audio Generation Tests

### Audio Creation
- [ ] Emotion selector appears (if voice cloned)
- [ ] All 7 emotions available (neutral, happy, sad, angry, fearful, disgusted, surprised)
- [ ] "Generate Audio" button works
- [ ] Loading spinner appears during generation
- [ ] Success message after generation
- [ ] Audio player appears
- [ ] Audio plays correctly
- [ ] "Download Audio" button appears
- [ ] Downloaded audio file plays correctly
- [ ] File name includes emotion and timestamp

### Emotion Variations
- [ ] Neutral emotion sounds neutral
- [ ] Happy emotion sounds upbeat
- [ ] Sad emotion sounds somber
- [ ] Angry emotion sounds intense
- [ ] Different emotions produce different audio

## 📜 History Tab Tests

### History Display
- [ ] History tab is accessible
- [ ] Shows "No files processed" when empty
- [ ] Processed files appear in history
- [ ] Files shown in reverse chronological order
- [ ] Each entry shows file name and timestamp
- [ ] Entries are collapsible/expandable

### History Actions
- [ ] Can download Word doc from history
- [ ] Can generate audio from history
- [ ] Emotion selector works in history
- [ ] Multiple history entries work independently
- [ ] "Clear History" button works
- [ ] History persists during session
- [ ] History clears on browser refresh

## 🔄 Session Management Tests

### Session Persistence
- [ ] API keys persist during session
- [ ] Voice ID persists during session
- [ ] Processing history persists during session
- [ ] Prompts persist during session
- [ ] Selected KB/files reset appropriately

### Session Clearing
- [ ] Closing browser tab clears session
- [ ] Reopening requires re-entering API keys
- [ ] New session starts fresh
- [ ] No data leakage between sessions

## 🐛 Error Handling Tests

### API Errors
- [ ] Invalid TAMU API key shows error
- [ ] Invalid ElevenLabs API key shows error
- [ ] Network errors handled gracefully
- [ ] API rate limit errors shown clearly
- [ ] Errors don't crash the app

### File Errors
- [ ] Non-existent file handled gracefully
- [ ] Empty file handled gracefully
- [ ] Large file processing works or shows appropriate error
- [ ] Invalid file format rejected

### Voice Errors
- [ ] Invalid audio format rejected
- [ ] Too short audio sample shows error
- [ ] Too large audio file handled
- [ ] Voice cloning failure shows error message

## 📊 Logging Tests

### Log Files
- [ ] `logs/` directory created automatically
- [ ] Log file created with timestamp
- [ ] Errors logged to file
- [ ] Log format is readable
- [ ] Stack traces included for errors
- [ ] No sensitive data in logs (API keys)

### Console Output
- [ ] Errors appear in terminal
- [ ] Info messages appear appropriately
- [ ] No excessive logging noise

## 🎨 UI/UX Tests

### Visual Design
- [ ] Clean, minimalistic appearance
- [ ] Texas A&M maroon color scheme
- [ ] Proper spacing and alignment
- [ ] Responsive layout
- [ ] Buttons styled consistently
- [ ] Text is readable

### User Experience
- [ ] Intuitive workflow
- [ ] Clear instructions
- [ ] Helpful tooltips
- [ ] Appropriate loading indicators
- [ ] Success/error messages clear
- [ ] No confusing error messages

## 🚀 Performance Tests

### Speed
- [ ] App loads quickly
- [ ] Knowledge bases load in reasonable time
- [ ] File processing completes in reasonable time
- [ ] Audio generation completes in reasonable time
- [ ] UI remains responsive during processing

### Resource Usage
- [ ] Memory usage reasonable
- [ ] No memory leaks during extended use
- [ ] CPU usage acceptable
- [ ] Disk space managed (outputs folder)

## 📱 Edge Cases

### Boundary Conditions
- [ ] Processing 1 file works
- [ ] Processing 10+ files works
- [ ] Very long prompts work
- [ ] Very short prompts work
- [ ] Special characters in file names handled
- [ ] Unicode in responses handled

### Unusual Scenarios
- [ ] Switching KB mid-session works
- [ ] Changing prompts between batches works
- [ ] Re-cloning voice works
- [ ] Processing same file twice works
- [ ] Rapid clicking doesn't break app

## 🔒 Security Tests

### Data Protection
- [ ] API keys not visible in logs
- [ ] API keys not in downloaded files
- [ ] API keys cleared on session end
- [ ] No API keys in error messages
- [ ] File paths sanitized

## 📝 Documentation Tests

### README
- [ ] Installation instructions work
- [ ] Usage examples are accurate
- [ ] All features documented
- [ ] Troubleshooting section helpful

### Code Documentation
- [ ] Functions have docstrings
- [ ] Complex logic commented
- [ ] Module purposes clear
- [ ] Type hints present

## ✅ Final Verification

- [ ] All critical features working
- [ ] No blocking bugs
- [ ] Error handling robust
- [ ] User experience smooth
- [ ] Documentation complete
- [ ] Ready for deployment

## 📋 Test Results

**Date Tested**: _______________
**Tested By**: _______________
**Version**: 1.0.0 MVP
**Overall Status**: ⬜ Pass / ⬜ Fail

**Notes**:
_______________________________________
_______________________________________
_______________________________________

**Issues Found**:
1. _______________________________________
2. _______________________________________
3. _______________________________________

**Recommendations**:
1. _______________________________________
2. _______________________________________
3. _______________________________________
