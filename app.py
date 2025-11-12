"""
FRED - File Response & Emotion-based Delivery
A Streamlit app for processing files with TAMU Chat API and generating audio with ElevenLabs.
"""

import streamlit as st
import logging
from datetime import datetime
import os
from typing import List, Dict, Optional
import traceback

from tamu_client import TAMUClient
from elevenlabs_client import ElevenLabsClient
from utils import setup_logging, create_word_document, sanitize_filename

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="FRED - File Response & Emotion Delivery",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, minimalistic design
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #500000;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #700000;
    }
    .result-card {
        background-color: #f8f9fa;
        border-left: 4px solid #500000;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-message {
        color: #28a745;
        font-weight: 500;
    }
    .error-message {
        color: #dc3545;
        font-weight: 500;
    }
    h1 {
        color: #500000;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'api_keys_set' not in st.session_state:
        st.session_state.api_keys_set = False
    if 'tamu_api_key' not in st.session_state:
        st.session_state.tamu_api_key = ""
    if 'elevenlabs_api_key' not in st.session_state:
        st.session_state.elevenlabs_api_key = ""
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    if 'voice_id' not in st.session_state:
        st.session_state.voice_id = None
    if 'voice_cloned' not in st.session_state:
        st.session_state.voice_cloned = False


def render_sidebar():
    """Render sidebar with API key inputs and voice cloning."""
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # API Keys Section
        st.subheader("API Keys")
        
        tamu_key = st.text_input(
            "TAMU AI API Key",
            type="password",
            value=st.session_state.tamu_api_key,
            help="Enter your TAMU AI API key"
        )
        
        elevenlabs_key = st.text_input(
            "ElevenLabs API Key",
            type="password",
            value=st.session_state.elevenlabs_api_key,
            help="Enter your ElevenLabs API key"
        )
        
        if st.button("💾 Save API Keys"):
            if tamu_key and elevenlabs_key:
                st.session_state.tamu_api_key = tamu_key
                st.session_state.elevenlabs_api_key = elevenlabs_key
                st.session_state.api_keys_set = True
                st.success("✅ API keys saved!")
                logger.info("API keys configured")
            else:
                st.error("❌ Please provide both API keys")
        
        st.divider()
        
        # Voice Cloning Section
        st.subheader("🎤 Voice Cloning")
        
        if st.session_state.api_keys_set:
            voice_name = st.text_input(
                "Voice Name",
                value="My Cloned Voice",
                help="Name for your cloned voice"
            )
            
            voice_files = st.file_uploader(
                "Upload Voice Samples",
                type=["mp3", "wav", "m4a"],
                accept_multiple_files=True,
                help="Upload 1-3 audio samples (each 30s-5min) for best results"
            )
            
            if st.button("🎙️ Clone Voice"):
                if voice_files:
                    try:
                        with st.spinner("Cloning voice..."):
                            elevenlabs_client = ElevenLabsClient(st.session_state.elevenlabs_api_key)
                            voice_bytes = [f.read() for f in voice_files]
                            voice_id = elevenlabs_client.clone_voice(
                                name=voice_name,
                                voice_files=voice_bytes,
                                description=f"Cloned voice created on {datetime.now().strftime('%Y-%m-%d')}"
                            )
                            st.session_state.voice_id = voice_id
                            st.session_state.voice_cloned = True
                            st.success(f"✅ Voice cloned successfully! ID: {voice_id[:8]}...")
                            logger.info(f"Voice cloned: {voice_id}")
                    except Exception as e:
                        st.error(f"❌ Error cloning voice: {str(e)}")
                        logger.error(f"Voice cloning error: {traceback.format_exc()}")
                else:
                    st.warning("⚠️ Please upload at least one voice sample")
            
            if st.session_state.voice_cloned:
                st.info(f"✓ Voice ready: {voice_name}")
        else:
            st.info("💡 Save API keys first to enable voice cloning")
        
        st.divider()
        
        # Session Info
        st.subheader("📊 Session Info")
        st.metric("Files Processed", len(st.session_state.processing_history))
        
        if st.button("🗑️ Clear History"):
            st.session_state.processing_history = []
            st.rerun()


def render_main_content():
    """Render main content area."""
    st.title("🎙️ FRED - File Response & Emotion-based Delivery")
    st.markdown("Process files with AI and generate emotional audio responses")
    
    if not st.session_state.api_keys_set:
        st.warning("⚠️ Please configure your API keys in the sidebar to get started")
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["📁 Process Files", "📜 History"])
    
    with tab1:
        render_processing_tab()
    
    with tab2:
        render_history_tab()


def render_processing_tab():
    """Render file processing tab."""
    try:
        tamu_client = TAMUClient(st.session_state.tamu_api_key)
        
        # Knowledge Base Selection
        st.subheader("1️⃣ Select Knowledge Base & Files")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Get knowledge bases
            with st.spinner("Loading knowledge bases..."):
                kb_list = tamu_client.list_knowledge_bases()
                kb_names = [kb.get("name", "Unnamed") for kb in kb_list]
            
            if not kb_names:
                st.warning("No knowledge bases found. Please create one first.")
                return
            
            selected_kb = st.selectbox(
                "Knowledge Base",
                kb_names,
                help="Select the knowledge base containing your files"
            )
        
        with col2:
            # Get files from selected KB
            selected_kb_data = next((kb for kb in kb_list if kb.get("name") == selected_kb), None)
            
            if selected_kb_data:
                files = selected_kb_data.get("files", [])
                file_options = [f.get("meta", {}).get("name", "Unnamed") for f in files]
                
                if not file_options:
                    st.warning("No files found in this knowledge base.")
                    return
                
                selected_files = st.multiselect(
                    "Select Files",
                    file_options,
                    help="Select one or more files to process"
                )
            else:
                st.error("Could not load knowledge base data")
                return
        
        st.divider()
        
        # Prompts Section
        st.subheader("2️⃣ Configure Prompts")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            system_prompt = st.text_area(
                "System Prompt",
                value="You are a helpful teaching assistant for CS courses at Texas A&M.",
                height=100,
                help="Define the AI's role and behavior"
            )
        
        with col2:
            user_prompt = st.text_area(
                "User Prompt",
                value="Explain the content of this document in simple terms.",
                height=100,
                help="Your question or instruction for the AI"
            )
        
        st.divider()
        
        # Model Settings
        st.subheader("3️⃣ Model Settings")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            model = st.selectbox(
                "Model",
                ["protected.gpt-5", "protected.gpt-4", "protected.gpt-3.5-turbo"],
                help="Select the AI model to use"
            )
        
        with col2:
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.1,
                help="Higher values make output more random"
            )
        
        st.divider()
        
        # Process Button
        if st.button("🚀 Process Files", type="primary"):
            if not selected_files:
                st.warning("⚠️ Please select at least one file to process")
                return
            
            process_files(
                tamu_client=tamu_client,
                kb_name=selected_kb,
                file_names=selected_files,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=temperature
            )
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Processing tab error: {traceback.format_exc()}")


def process_files(
    tamu_client: TAMUClient,
    kb_name: str,
    file_names: List[str],
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float
):
    """Process selected files with TAMU API."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(file_names)
    
    for idx, file_name in enumerate(file_names):
        try:
            status_text.text(f"Processing {idx + 1}/{total_files}: {file_name}")
            
            # Get AI response
            with st.spinner(f"Getting AI response for {file_name}..."):
                response = tamu_client.chat_with_kb_file(
                    kb_name=kb_name,
                    file_name=file_name,
                    base_system_prompt=system_prompt,
                    base_user_prompt=user_prompt,
                    model=model,
                    temperature=temperature
                )
            
            # Create Word document
            safe_filename = sanitize_filename(file_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_filename = f"{safe_filename}_{timestamp}"
            
            with st.spinner("Creating Word document..."):
                doc_path = create_word_document(response, doc_filename)
            
            # Add to history
            history_entry = {
                "timestamp": datetime.now(),
                "kb_name": kb_name,
                "file_name": file_name,
                "response": response,
                "doc_path": doc_path,
                "model": model,
            }
            st.session_state.processing_history.append(history_entry)
            
            # Display result
            st.success(f"✅ Processed: {file_name}")
            
            with st.expander(f"📄 View Response - {file_name}", expanded=True):
                st.markdown(f"**File:** {file_name}")
                st.markdown(f"**Knowledge Base:** {kb_name}")
                st.markdown(f"**Model:** {model}")
                st.divider()
                st.markdown(response)
                
                # Download buttons
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    with open(doc_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Word Document",
                            data=f.read(),
                            file_name=f"{doc_filename}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                
                with col2:
                    if st.session_state.voice_cloned:
                        emotion = st.selectbox(
                            "Select Emotion",
                            ElevenLabsClient.SUPPORTED_EMOTIONS,
                            key=f"emotion_{idx}_{file_name}"
                        )
                        
                        if st.button(f"🎵 Generate Audio", key=f"audio_{idx}_{file_name}"):
                            generate_audio_for_response(response, file_name, emotion)
                    else:
                        st.info("💡 Clone your voice in the sidebar to enable audio generation")
            
            logger.info(f"Successfully processed file: {file_name}")
            
        except Exception as e:
            st.error(f"❌ Error processing {file_name}: {str(e)}")
            logger.error(f"Error processing {file_name}: {traceback.format_exc()}")
        
        # Update progress
        progress_bar.progress((idx + 1) / total_files)
    
    status_text.text("✅ All files processed!")
    st.balloons()


def generate_audio_for_response(response: str, file_name: str, emotion: str):
    """Generate audio for a response."""
    try:
        with st.spinner(f"Generating audio with {emotion} emotion..."):
            elevenlabs_client = ElevenLabsClient(st.session_state.elevenlabs_api_key)
            
            audio_bytes = elevenlabs_client.generate_audio(
                text=response,
                voice_id=st.session_state.voice_id,
                emotion=emotion
            )
            
            # Save audio file
            os.makedirs("outputs", exist_ok=True)
            safe_filename = sanitize_filename(file_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"{safe_filename}_{emotion}_{timestamp}.mp3"
            audio_path = os.path.join("outputs", audio_filename)
            
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)
            
            st.success(f"✅ Audio generated with {emotion} emotion!")
            
            # Audio player
            st.audio(audio_bytes, format="audio/mp3")
            
            # Download button
            st.download_button(
                label="📥 Download Audio",
                data=audio_bytes,
                file_name=audio_filename,
                mime="audio/mp3"
            )
            
            logger.info(f"Generated audio for {file_name} with {emotion} emotion")
    
    except Exception as e:
        st.error(f"❌ Error generating audio: {str(e)}")
        logger.error(f"Audio generation error: {traceback.format_exc()}")


def render_history_tab():
    """Render processing history tab."""
    st.subheader("📜 Processing History")
    
    if not st.session_state.processing_history:
        st.info("No files processed yet. Process some files to see them here!")
        return
    
    # Display history in reverse chronological order
    for idx, entry in enumerate(reversed(st.session_state.processing_history)):
        with st.expander(
            f"📄 {entry['file_name']} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}",
            expanded=False
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**File:** {entry['file_name']}")
                st.markdown(f"**Knowledge Base:** {entry['kb_name']}")
                st.markdown(f"**Model:** {entry['model']}")
                st.markdown(f"**Timestamp:** {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col2:
                # Download Word document
                if os.path.exists(entry['doc_path']):
                    with open(entry['doc_path'], "rb") as f:
                        st.download_button(
                            label="📥 Download Word",
                            data=f.read(),
                            file_name=os.path.basename(entry['doc_path']),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"download_history_{idx}"
                        )
                
                # Generate audio
                if st.session_state.voice_cloned:
                    emotion = st.selectbox(
                        "Emotion",
                        ElevenLabsClient.SUPPORTED_EMOTIONS,
                        key=f"history_emotion_{idx}"
                    )
                    
                    if st.button("🎵 Generate Audio", key=f"history_audio_{idx}"):
                        generate_audio_for_response(
                            entry['response'],
                            entry['file_name'],
                            emotion
                        )
            
            st.divider()
            st.markdown("**Response:**")
            st.markdown(entry['response'])


def main():
    """Main application entry point."""
    initialize_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
