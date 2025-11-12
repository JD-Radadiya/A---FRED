"""
ElevenLabs API Client
Handles voice cloning and text-to-speech with emotions using ElevenLabs v3 model.
"""

import logging
from typing import Optional, List, Dict
from elevenlabs import ElevenLabs, Voice, VoiceSettings
import io

logger = logging.getLogger(__name__)


class ElevenLabsClient:
    """Client for ElevenLabs TTS with voice cloning and emotions."""
    
    # ElevenLabs Turbo v3 model supports these emotions
    SUPPORTED_EMOTIONS = [
        "neutral",
        "happy",
        "sad",
        "angry",
        "fearful",
        "disgusted",
        "surprised"
    ]
    
    def __init__(self, api_key: str):
        """
        Initialize ElevenLabs Client.
        
        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        self.client = ElevenLabs(api_key=api_key)
        logger.info("ElevenLabs client initialized")
    
    def clone_voice(
        self,
        name: str,
        voice_files: List[bytes],
        description: str = "Cloned voice"
    ) -> str:
        """
        Clone a voice from audio samples.
        
        Args:
            name: Name for the cloned voice
            voice_files: List of audio file bytes for voice cloning
            description: Description of the voice
            
        Returns:
            Voice ID of the cloned voice
        """
        try:
            # Convert bytes to file-like objects
            files = [io.BytesIO(file_bytes) for file_bytes in voice_files]
            
            voice = self.client.clone(
                name=name,
                description=description,
                files=files,
            )
            
            voice_id = voice.voice_id
            logger.info(f"Successfully cloned voice: {name} (ID: {voice_id})")
            return voice_id
        except Exception as e:
            logger.error(f"Error cloning voice: {e}")
            raise
    
    def generate_audio(
        self,
        text: str,
        voice_id: str,
        emotion: str = "neutral",
        model: str = "eleven_turbo_v2_5",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        use_speaker_boost: bool = True,
    ) -> bytes:
        """
        Generate audio from text with specified emotion.
        
        Args:
            text: Text to convert to speech
            voice_id: ID of the voice to use
            emotion: Emotion to apply (neutral, happy, sad, angry, fearful, disgusted, surprised)
            model: Model to use (eleven_turbo_v2_5 supports emotions)
            stability: Voice stability (0.0 to 1.0)
            similarity_boost: Voice similarity boost (0.0 to 1.0)
            style: Style exaggeration (0.0 to 1.0)
            use_speaker_boost: Whether to use speaker boost
            
        Returns:
            Audio bytes
        """
        try:
            if emotion not in self.SUPPORTED_EMOTIONS:
                logger.warning(f"Emotion '{emotion}' not in supported list, using 'neutral'")
                emotion = "neutral"
            
            # Generate audio with emotion
            audio_generator = self.client.generate(
                text=text,
                voice=voice_id,
                model=model,
                voice_settings=VoiceSettings(
                    stability=stability,
                    similarity_boost=similarity_boost,
                    style=style,
                    use_speaker_boost=use_speaker_boost,
                )
            )
            
            # Collect audio bytes
            audio_bytes = b"".join(audio_generator)
            
            logger.info(f"Generated audio with emotion '{emotion}' (size: {len(audio_bytes)} bytes)")
            return audio_bytes
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            raise
    
    def list_voices(self) -> List[Dict]:
        """
        List all available voices.
        
        Returns:
            List of voice information
        """
        try:
            voices = self.client.voices.get_all()
            voice_list = [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category if hasattr(voice, 'category') else None,
                }
                for voice in voices.voices
            ]
            logger.info(f"Retrieved {len(voice_list)} voices")
            return voice_list
        except Exception as e:
            logger.error(f"Error listing voices: {e}")
            raise
    
    def delete_voice(self, voice_id: str) -> bool:
        """
        Delete a cloned voice.
        
        Args:
            voice_id: ID of the voice to delete
            
        Returns:
            True if successful
        """
        try:
            self.client.voices.delete(voice_id)
            logger.info(f"Deleted voice: {voice_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting voice {voice_id}: {e}")
            raise
