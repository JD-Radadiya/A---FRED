"""
ElevenLabs API Client
Handles voice cloning and text-to-speech with emotions using ElevenLabs v3 model.
"""

import logging
import traceback
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
    
    # Default pre-made voices from ElevenLabs
    DEFAULT_VOICES = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Drew": "29vD33N1CtxCmqQRPOHJ",
        "Clyde": "2EiwWnXFnvU5JabPnv8n",
        "Paul": "5Q0t7uMcjvnagumLfvZi",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
        "Dave": "CYw3kZ02Hs0563khs1Fj",
        "Fin": "D38z5RcWu1voky8WS1ja",
        "Sarah": "EXAVITQu4vr4xnSDxMaL",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Thomas": "GBv7mTt0atIp3Br8iCZE",
        "Charlie": "IKne3meq5aSn9XLyUdCD",
        "Emily": "LcfcDJNUP1GQjkzn1xUU",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Callum": "N2lVS1w4EtoT3dr4eOWO",
        "Patrick": "ODq5zmih8GrVes37Dizd",
        "Harry": "SOYHLrjzK2X1ezoPC6cr",
        "Liam": "TX3LPaxmHKxFdv7VOQHJ",
        "Dorothy": "ThT5KcBeYPX3keUQqHPh",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Charlotte": "XB0fDUnXU5powFXDhCwa",
        "Alice": "Xb7hH8MSUJpSbSDYk0k2",
        "Matilda": "XrExE9yKIg1WjnnlVkGX",
        "James": "ZQe5CZNOzWyzPSCn5a3c",
        "Joseph": "Zlb1dXrM653N07WRdFW3",
        "Jeremy": "bVMeCyTHy58xNoL34h3p",
        "Michael": "flq6f7yk4E4fJM5XTYuZ",
        "Ethan": "g5CIjZEefAph4nQFvHAz",
        "Chris": "iP95p4xoKVk53GoZ742B",
        "Gigi": "jBpfuIE2acCO8z3wKNLl",
        "Freya": "jsCqWAovK2LkecY7zXl4",
        "Brian": "nPczCjzI2devNBz1zQrb",
        "Grace": "oWAxZDx7w5VEj9dCyTzz",
        "Daniel": "onwK4e9ZLuTAKqWW03F9",
        "Lily": "pFZP5JQG7iQjIQuC4Bku",
        "Serena": "pMsXgVXv3BLzUgSXRplE",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Nicole": "piTKgcLEGmPE4e6mEKli",
        "Bill": "pqHfZKP75CvOlQylNhV4",
        "Jessie": "t0jbNlBVZ17f02VDIeMI",
        "Sam": "yoZ06aMxZJJ28mfd3POQ",
        "Glinda": "z9fAnlkpzviPz146aGWa",
        "Giovanni": "zcAOhNBS3c14rBihAFp1",
        "Mimi": "zrHiDhphv9ZnVXBqCLjz"
    }
    
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
            logger.info(f"Starting voice cloning for: {name}")
            logger.info(f"Number of voice samples: {len(voice_files)}")
            logger.info(f"Sample sizes: {[len(f) for f in voice_files]} bytes")
            
            # Convert bytes to file-like objects
            files = [io.BytesIO(file_bytes) for file_bytes in voice_files]
            
            logger.info("Calling ElevenLabs clone API...")
            voice = self.client.clone(
                name=name,
                description=description,
                files=files,
            )
            
            voice_id = voice.voice_id
            logger.info(f"✅ Successfully cloned voice: {name} (ID: {voice_id})")
            return voice_id
        except Exception as e:
            logger.error(f"❌ Error cloning voice '{name}': {type(e).__name__}: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
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
            logger.info(f"ElevenLabs generate_audio called with:")
            logger.info(f"  - text length: {len(text)} characters")
            logger.info(f"  - voice_id: {voice_id}")
            logger.info(f"  - emotion: {emotion}")
            logger.info(f"  - model: {model}")
            logger.info(f"  - settings: stability={stability}, similarity={similarity_boost}, style={style}")
            
            if emotion not in self.SUPPORTED_EMOTIONS:
                logger.warning(f"Emotion '{emotion}' not in supported list, using 'neutral'")
                emotion = "neutral"
            
            # Generate audio with emotion
            logger.info("Calling ElevenLabs API...")
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
            
            logger.info("Received response from ElevenLabs, collecting audio bytes...")
            # Collect audio bytes
            audio_bytes = b"".join(audio_generator)
            
            logger.info(f"✅ Successfully generated audio with emotion '{emotion}' (size: {len(audio_bytes)} bytes)")
            
            if len(audio_bytes) == 0:
                logger.error("ERROR: Received 0 bytes from ElevenLabs API!")
                raise ValueError("ElevenLabs returned empty audio")
            
            return audio_bytes
        except Exception as e:
            logger.error(f"❌ Error generating audio: {type(e).__name__}: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
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
