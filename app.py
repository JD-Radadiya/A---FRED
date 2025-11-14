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
    page_title="A-FRED: Artificial Feedback, Recommendation, Evaluation and Diagnosis",
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
    if 'use_default_voice' not in st.session_state:
        st.session_state.use_default_voice = True
    if 'selected_default_voice' not in st.session_state:
        st.session_state.selected_default_voice = "Rachel"
    if 'instructions_file_id' not in st.session_state:
        st.session_state.instructions_file_id = None
    if 'instructions_content' not in st.session_state:
        st.session_state.instructions_content = ""
    if 'selected_files_multi_kb' not in st.session_state:
        st.session_state.selected_files_multi_kb = []
    if 'just_processed' not in st.session_state:
        st.session_state.just_processed = False


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
            if not tamu_key:
                st.error("❌ Please provide your TAMU AI API key (the ElevenLabs key is optional)")
            else:
                # Save required TAMU key
                st.session_state.tamu_api_key = tamu_key
                st.session_state.api_keys_set = True

                # Handle optional ElevenLabs key
                if elevenlabs_key:
                    st.session_state.elevenlabs_api_key = elevenlabs_key
                    st.session_state.elevenlabs_configured = True
                    st.success("✅ TAMU AI key saved! ElevenLabs key saved, audio features enabled.")
                    logger.info("TAMU + ElevenLabs API keys configured")
                else:
                    st.session_state.elevenlabs_api_key = ""
                    st.session_state.elevenlabs_configured = False
                    st.success("✅ TAMU AI key saved!")
                    st.info("You can add an ElevenLabs API key later to enable audio features.")
                    logger.info("TAMU API key configured; ElevenLabs key not set")
        
        st.divider()
        
        # Voice Selection Section
        st.subheader("🎤 Voice Selection")
        
        if st.session_state.api_keys_set:
            if not st.session_state.elevenlabs_api_key:
                st.info("Add an ElevenLabs API key above to enable voice selection and audio generation.")
            else:
                voice_option = st.radio(
                    "Voice Option",
                    ["Use Default Voice", "Clone My Voice"],
                    index=0 if st.session_state.use_default_voice else 1,
                    help="Choose between pre-made voices or clone your own"
                )
                
                if voice_option == "Use Default Voice":
                    st.session_state.use_default_voice = True
                    st.session_state.selected_default_voice = st.selectbox(
                        "Select Default Voice",
                        list(ElevenLabsClient.DEFAULT_VOICES.keys()),
                        index=list(ElevenLabsClient.DEFAULT_VOICES.keys()).index(
                            st.session_state.selected_default_voice
                        ),
                        help="Choose from pre-made ElevenLabs voices"
                    )
                    st.info(f"✓ Using default voice: {st.session_state.selected_default_voice}")
                else:
                    st.session_state.use_default_voice = False
                    voice_name = st.text_input(
                        "Voice Name",
                        value="My Cloned Voice",
                        help="Name for your cloned voice"
                    )
                    
                    voice_files = st.file_uploader(
                        "Upload Voice Samples",
                        type=["mp3", "wav", "m4a"],
                        accept_multiple_files=True,
                        help="Upload 1-3 audio samples (each 30s–5min) for best results"
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
            st.info("💡 Save your TAMU AI API key first to enable voice selection")

        
        st.divider()
        
        # Session Info
        st.subheader("📊 Session Info")
        st.metric("Files Processed", len(st.session_state.processing_history))
        
        if st.button("🗑️ Clear History"):
            st.session_state.processing_history = []
            st.rerun()


def render_main_content():
    """Render main content area."""
    st.title("🎙️ A-FRED: Artificial Feedback, Recommendation, Evaluation and Diagnosis")
    st.markdown("Process files with AI and generate emotional audio responses")
    
    if not st.session_state.tamu_api_key:
        st.warning(
            "⚠️ Please configure your TAMU AI API key in the sidebar to get started. "
            "The ElevenLabs key is optional and only needed for audio."
        )
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["📁 Process Files", "📜 History"])
    
    with tab1:
        render_processing_tab()
    
    with tab2:
        render_history_tab()

def render_processing_results():
    """Render results (responses + downloads + audio) for processed files."""
    if not st.session_state.processing_history:
        return

    st.subheader("4️⃣ Generated Responses & Downloads")

    # Newest first (so latest processed files appear at the top)
    history = sorted(
        st.session_state.processing_history,
        key=lambda e: e["timestamp"],
        reverse=True,  # newest → oldest
    )

    # Are we on the first render right after processing at least one file?
    auto_expand_first = st.session_state.get("just_processed", False)

    for idx, entry in enumerate(history):
        label = (
            f"📄 {entry['file_name']} ({entry['kb_name']}) - "
            f"{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # 👉 Only on the FIRST render after processing:
        #     expand the top card (idx == 0).
        #    On all later renders (auto_expand_first == False),
        #     we DO NOT pass `expanded`, so Streamlit preserves
        #     the user's open/closed state.
        if auto_expand_first and idx == 0:
            expander = st.expander(label, expanded=True)
        else:
            expander = st.expander(label)

        with expander:
            st.markdown(f"**File:** {entry['file_name']}")
            st.markdown(f"**Knowledge Base:** {entry['kb_name']}")
            st.markdown(f"**Model:** {entry['model']}")
            st.markdown("---")
            st.markdown(entry["response"])

            col1, col2 = st.columns([1, 1])

            # --- Word download ---
            with col1:
                if os.path.exists(entry["doc_path"]):
                    with open(entry["doc_path"], "rb") as f:
                        doc_data = f.read()

                    st.download_button(
                        label="📥 Download Word Document",
                        data=doc_data,
                        file_name=os.path.basename(entry["doc_path"]),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_word_{idx}",  # stable within the current ordering
                        help="Download the AI response as a Word document",
                    )
                else:
                    st.error("❌ Document file not found")

            # --- Audio controls ---
            with col2:
                emotion = st.selectbox(
                    "Select Emotion",
                    ElevenLabsClient.SUPPORTED_EMOTIONS,
                    key=f"current_emotion_{idx}",
                )

                audio_style = st.selectbox(
                    "Audio Style",
                    ["Direct Response", "Feedback Style"],
                    key=f"current_style_{idx}",
                    help="Direct: Read the response as-is. Feedback: Deliver as personalized feedback.",
                )

                if st.button("🎵 Generate Audio", key=f"current_audio_{idx}"):
                    generate_audio_for_response(
                        entry["response"],
                        entry["file_name"],
                        emotion,
                        audio_style,
                    )

    # 🔁 After the first "post-processing" render, turn off auto-expand
    if auto_expand_first:
        st.session_state.just_processed = False


def render_processing_tab():
    """Render file processing tab."""
    try:
        tamu_client = TAMUClient(st.session_state.tamu_api_key)
        
        # Knowledge Base Selection
        st.subheader("1️⃣ Select Knowledge Bases & Files")
        
        # Get knowledge bases
        with st.spinner("Loading knowledge bases..."):
            kb_list = tamu_client.list_knowledge_bases()
            kb_names = [kb.get("name", "Unnamed") for kb in kb_list]
        
        if not kb_names:
            st.warning("No knowledge bases found. Please create one first.")
            return
        
        # Multi-KB selection
        selected_kbs = st.multiselect(
            "Select Knowledge Bases",
            kb_names,
            help="Select one or more knowledge bases"
        )
        
        # File upload section
        with st.expander("📤 Upload Files to Knowledge Base", expanded=False):
            upload_col1, upload_col2 = st.columns([1, 1])
            
            with upload_col1:
                target_kb = st.selectbox(
                    "Target Knowledge Base",
                    kb_names,
                    key="upload_kb",
                    help="Select KB to upload files to"
                )
            
            with upload_col2:
                uploaded_files = st.file_uploader(
                    "Choose files to upload",
                    accept_multiple_files=True,
                    type=["pdf", "txt", "docx", "doc", "pptx", "xlsx"],
                    help="Upload documents to the knowledge base"
                )
            
            if st.button("⬆️ Upload Files to KB"):
                if uploaded_files and target_kb:
                    upload_progress = st.progress(0)
                    upload_status = st.empty()
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        try:
                            upload_status.text(f"Uploading {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
                            
                            # Upload file to TAMU
                            file_bytes = uploaded_file.read()
                            upload_response = tamu_client.upload_file(
                                file_bytes=file_bytes,
                                filename=uploaded_file.name
                            )
                            
                            # Add to knowledge base
                            file_id = upload_response.get("id")
                            if file_id:
                                tamu_client.add_file_to_knowledge_base(target_kb, file_id)
                                st.success(f"✅ Uploaded: {uploaded_file.name}")
                                logger.info(f"Uploaded {uploaded_file.name} to {target_kb}")
                            
                            upload_progress.progress((idx + 1) / len(uploaded_files))
                        except Exception as e:
                            st.error(f"❌ Error uploading {uploaded_file.name}: {str(e)}")
                            logger.error(f"Upload error for {uploaded_file.name}: {traceback.format_exc()}")
                    
                    upload_status.text("✅ Upload complete!")
                    st.info("🔄 Refresh the page to see newly uploaded files")
                else:
                    st.warning("⚠️ Please select files and a target knowledge base")
        
        # File selection from multiple KBs
        if selected_kbs:
            st.markdown("**Select Files from Knowledge Bases:**")
            all_selected_files = []
            
            for kb_name in selected_kbs:
                kb_data = next((kb for kb in kb_list if kb.get("name") == kb_name), None)
                
                if kb_data:
                    files = kb_data.get("files", [])
                    file_options = [f.get("meta", {}).get("name", "Unnamed") for f in files]
                    
                    if file_options:
                        selected_files_for_kb = st.multiselect(
                            f"📁 {kb_name}",
                            file_options,
                            key=f"files_{kb_name}",
                            help=f"Select files from {kb_name}"
                        )
                        
                        # Store with KB name for later processing
                        for file_name in selected_files_for_kb:
                            all_selected_files.append({
                                "kb_name": kb_name,
                                "file_name": file_name
                            })
                    else:
                        st.info(f"No files in {kb_name}")
            
            # Store in session state
            st.session_state.selected_files_multi_kb = all_selected_files
            
            if all_selected_files:
                st.success(f"✅ {len(all_selected_files)} file(s) selected from {len(selected_kbs)} knowledge base(s)")
        else:
            st.info("👆 Select at least one knowledge base to see files")
        
        st.divider()
        
        # Prompts Section
        st.subheader("2️⃣ Configure Prompts")
        
        # Instructions Document Section
        with st.expander("📋 Use Instructions Document (Optional)", expanded=False):
            st.markdown("Upload or select an instructions document from a knowledge base to auto-populate the system prompt.")
            
            inst_col1, inst_col2 = st.columns([1, 1])
            
            with inst_col1:
                inst_kb = st.selectbox(
                    "Instructions KB",
                    kb_names,
                    key="instructions_kb",
                    help="Select KB containing instructions document"
                )
            
            with inst_col2:
                inst_kb_data = next((kb for kb in kb_list if kb.get("name") == inst_kb), None)
                if inst_kb_data:
                    inst_files = inst_kb_data.get("files", [])
                    inst_file_options = [f.get("meta", {}).get("name", "Unnamed") for f in inst_files]
                    
                    if inst_file_options:
                        selected_inst_file = st.selectbox(
                            "Instructions Document",
                            ["None"] + inst_file_options,
                            key="instructions_file",
                            help="Select instructions document"
                        )
                        
                        if selected_inst_file != "None" and st.button("📥 Load Instructions"):
                            try:
                                with st.spinner("Loading instructions..."):
                                    # Get file ID
                                    file_id = tamu_client.get_file_id_from_kb(kb_list, inst_kb, selected_inst_file)
                                    st.session_state.instructions_file_id = file_id
                                    
                                    # Fetch content using chat API
                                    instructions_content = tamu_client.chat_with_kb_file(
                                        kb_name=inst_kb,
                                        file_name=selected_inst_file,
                                        base_system_prompt="You are a document reader. Extract and return ONLY the text content of the document without any additional commentary.",
                                        base_user_prompt="Please provide the complete text content of this document.",
                                        temperature=0.0
                                    )
                                    st.session_state.instructions_content = instructions_content
                                    st.success(f"✅ Loaded instructions from {selected_inst_file}")
                                    logger.info(f"Loaded instructions from {selected_inst_file}")
                            except Exception as e:
                                st.error(f"❌ Error loading instructions: {str(e)}")
                                logger.error(f"Instructions load error: {traceback.format_exc()}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Use instructions content if available, otherwise use default
            default_system_prompt = st.session_state.instructions_content if st.session_state.instructions_content else "You are a helpful teaching assistant for CS courses at Texas A&M."
            
            system_prompt = st.text_area(
                "System Prompt",
                value=default_system_prompt,
                height=150,
                help="Define the AI's role and behavior. Auto-populated from instructions document if loaded."
            )
            
            if st.session_state.instructions_content:
                st.info("✓ Using instructions from document")
        
        with col2:
            user_prompt = st.text_area(
                "User Prompt",
                value="Explain the content of this document in simple terms.",
                height=150,
                help="Your question or instruction for the AI"
            )
        
        st.divider()
        
        # Model Settings
        st.subheader("3️⃣ Model Settings")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            model = st.selectbox(
                "Model",
                tamu_client.get_available_models(),
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
            if not st.session_state.selected_files_multi_kb:
                st.warning("⚠️ Please select at least one file to process")
            else:
                process_files_multi_kb(
                    tamu_client=tamu_client,
                    files_data=st.session_state.selected_files_multi_kb,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    model=model,
                    temperature=temperature,
                )

        # 🔹 Always render results below (for this and future reruns)
        render_processing_results()
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Processing tab error: {traceback.format_exc()}")


def process_files_multi_kb(
    tamu_client: TAMUClient,
    files_data: List[Dict],
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float
):
    """Process selected files from multiple knowledge bases with TAMU API."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(files_data)
    
    for idx, file_data in enumerate(files_data):
        kb_name = file_data["kb_name"]
        file_name = file_data["file_name"]
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
            
            # Light feedback only; detailed UI is rendered separately
            st.success(f"✅ Processed: {file_name}")
            logger.info(f"Successfully processed file: {file_name}")
            
        except Exception as e:
            st.error(f"❌ Error processing {file_name}: {str(e)}")
            logger.error(f"Error processing {file_name}: {traceback.format_exc()}")
        
        # Update progress
        progress_bar.progress((idx + 1) / total_files)
    
    st.session_state.just_processed = True
    status_text.text("✅ All files processed!")
    st.balloons()


def generate_audio_for_response(response: str, file_name: str, emotion: str, audio_style: str = "Direct Response"):
    """Generate audio for a response with optional feedback styling."""
    try:
        if not st.session_state.elevenlabs_api_key:
            st.error("❌ ElevenLabs API key is not configured. Please add it in the sidebar to generate audio.")
            logger.error("Audio generation requested but ElevenLabs API key is missing.")
            return

        logger.info(f"Starting audio generation for {file_name} with emotion={emotion}, style={audio_style}")
        
        with st.spinner(f"Generating {audio_style.lower()} audio with {emotion} emotion..."):
            # Initialize ElevenLabs client
            logger.info("Initializing ElevenLabs client")
            elevenlabs_client = ElevenLabsClient(st.session_state.elevenlabs_api_key)
            
            # Determine voice ID
            if st.session_state.use_default_voice:
                voice_id = ElevenLabsClient.DEFAULT_VOICES[st.session_state.selected_default_voice]
                voice_name = st.session_state.selected_default_voice
                logger.info(f"Using default voice: {voice_name} (ID: {voice_id})")
            elif st.session_state.voice_cloned and st.session_state.voice_id:
                voice_id = st.session_state.voice_id
                voice_name = "Cloned Voice"
                logger.info(f"Using cloned voice (ID: {voice_id})")
            else:
                # Fallback to default
                voice_id = ElevenLabsClient.DEFAULT_VOICES["Rachel"]
                voice_name = "Rachel (Default)"
                logger.info(f"Using fallback voice: {voice_name} (ID: {voice_id})")
            
            # Transform text for feedback style
            if audio_style == "Feedback Style":
                feedback_text = transform_to_feedback_style(response)
                logger.info(f"Transformed text to feedback style (length: {len(feedback_text)} chars)")
            else:
                feedback_text = response
                logger.info(f"Using direct response (length: {len(feedback_text)} chars)")
            
            # Generate audio
            logger.info(f"Calling ElevenLabs API to generate audio...")
            audio_bytes = elevenlabs_client.generate_audio(
                text=feedback_text,
                voice_id=voice_id,
                emotion=emotion
            )
            logger.info(f"Audio generation successful, received {len(audio_bytes)} bytes")
            
            # Verify we got audio data
            if not audio_bytes or len(audio_bytes) == 0:
                error_msg = "ElevenLabs returned empty audio data"
                logger.error(error_msg)
                st.error(f"❌ {error_msg}")
                return
            
            # Save audio file
            logger.info("Saving audio file to disk...")
            os.makedirs("outputs", exist_ok=True)
            safe_filename = sanitize_filename(file_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            style_suffix = "feedback" if audio_style == "Feedback Style" else "direct"
            audio_filename = f"{safe_filename}_{emotion}_{style_suffix}_{timestamp}.mp3"
            audio_path = os.path.join("outputs", audio_filename)
            
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)
            logger.info(f"Audio file saved to: {audio_path}")
            
            st.success(f"✅ Audio generated with {emotion} emotion using {voice_name}!")
            logger.info(f"✅ Successfully generated {audio_style} audio for {file_name} with {emotion} emotion using {voice_name}")
            
            # Audio player
            st.audio(audio_bytes, format="audio/mp3")
            
            # Download button with unique key
            st.download_button(
                label="📥 Download Audio",
                data=audio_bytes,
                file_name=audio_filename,
                mime="audio/mp3",
                key=f"download_audio_{safe_filename}_{timestamp}"
            )
    
    except Exception as e:
        error_msg = f"Error generating audio: {type(e).__name__}: {str(e)}"
        st.error(f"❌ {error_msg}")
        logger.error(f"❌ Audio generation error for {file_name}: {error_msg}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Show helpful debugging info
        with st.expander("🔍 Debug Information"):
            st.code(f"""
                Error Type: {type(e).__name__}
                Error Message: {str(e)}

                Voice Settings:
                - Use Default Voice: {st.session_state.use_default_voice}
                - Selected Default Voice: {st.session_state.get('selected_default_voice', 'N/A')}
                - Voice Cloned: {st.session_state.voice_cloned}
                - Voice ID: {st.session_state.get('voice_id', 'N/A')}

                Audio Settings:
                - Emotion: {emotion}
                - Style: {audio_style}
                - Text Length: {len(response)} characters

                Check the logs directory for detailed error information.
            """)


def transform_to_feedback_style(text: str) -> str:
    """
    Transform response text into feedback-style delivery.
    Adds conversational elements and personal touches.
    """
    # Add opening
    feedback = "Hi there! I've reviewed your document and here's my feedback. "
    
    # Add the main content
    feedback += text
    
    # Add closing
    feedback += " I hope this feedback is helpful. Feel free to reach out if you have any questions or need clarification on any points. Keep up the great work!"
    
    return feedback


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
                        doc_data = f.read()
                    
                    st.download_button(
                        label="📥 Download Word",
                        data=doc_data,
                        file_name=os.path.basename(entry['doc_path']),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_history_{idx}_{entry['timestamp'].strftime('%Y%m%d_%H%M%S')}"
                    )
                else:
                    st.error("❌ Document not found")
                
                # Generate audio (optional)
                if not st.session_state.elevenlabs_api_key:
                    st.info("Add an ElevenLabs API key in the sidebar to enable audio generation.")
                else:
                    emotion = st.selectbox(
                        "Emotion",
                        ElevenLabsClient.SUPPORTED_EMOTIONS,
                        key=f"history_emotion_{idx}_{entry['timestamp'].strftime('%Y%m%d_%H%M%S')}"
                    )
                    
                    audio_style = st.selectbox(
                        "Audio Style",
                        ["Direct Response", "Feedback Style"],
                        key=f"history_style_{idx}_{entry['timestamp'].strftime('%Y%m%d_%H%M%S')}"
                    )
                    
                    if st.button("🎵 Generate Audio", key=f"history_audio_{idx}"):
                        generate_audio_for_response(
                            entry["response"],
                            entry["file_name"],
                            emotion,
                            audio_style,
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
