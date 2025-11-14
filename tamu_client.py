"""
TAMU Chat API Client
Handles all interactions with the TAMU Chat API endpoints.
"""

import requests
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class TAMUClient:
    """Client for interacting with TAMU Chat API."""
    
    def __init__(self, api_key: str):
        """
        Initialize TAMU Client.
        
        Args:
            api_key: TAMU AI API key
        """
        self.api_key = api_key
        self.api_base = "https://chat-api.tamu.ai"
        self.openai_base = "https://chat-api.tamu.ai/openai"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models from TAMU API.
        
        Returns:
            List of model IDs
        """
        try:
            url = f"{self.openai_base}/models"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            models = [model['id'] for model in result['data']]
            logger.info(f"Retrieved {len(models)} available models")
            return models
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            raise
    
    def upload_file(self, file_path: str = None, file_bytes: bytes = None, 
                    filename: str = None, purpose: str = "fine-tune") -> Dict:
        """
        Upload a file to TAMU API.
        
        Args:
            file_path: Path to the file to upload (if uploading from disk)
            file_bytes: File bytes (if uploading from memory)
            filename: Filename to use (required if using file_bytes)
            purpose: Purpose of the file upload
            
        Returns:
            Upload response data
        """
        try:
            url = f"{self.api_base}/api/v1/files/"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            
            if file_path:
                with open(file_path, "rb") as f:
                    files = {
                        "file": f,
                        "purpose": (None, purpose),
                    }
                    response = requests.post(url, headers=headers, files=files)
                    response.raise_for_status()
                    data = response.json()
                    logger.info(f"Successfully uploaded file: {file_path}")
                    return data
            elif file_bytes and filename:
                files = {
                    "file": (filename, file_bytes),
                    "purpose": (None, purpose),
                }
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully uploaded file: {filename}")
                return data
            else:
                raise ValueError("Must provide either file_path or (file_bytes and filename)")
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    def find_file(self, file_name: str) -> Dict:
        """
        Search for a file by name in TAMU API.
        
        Args:
            file_name: Name of the file to search for
            
        Returns:
            File details
        """
        try:
            url = f"{self.api_base}/api/v1/files/search?filename={file_name}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Found file: {file_name}")
            return data
        except Exception as e:
            logger.error(f"Error finding file {file_name}: {e}")
            raise
    
    def create_knowledge_base(self, name: str, description: str = "") -> Dict:
        """
        Create a new knowledge base.
        
        Args:
            name: Name of the knowledge base
            description: Description of the knowledge base
            
        Returns:
            Knowledge base creation response
        """
        try:
            url = f"{self.api_base}/api/v1/knowledge/create"
            payload = {
                "name": name,
                "description": description,
            }
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Created knowledge base: {name}")
            return data
        except Exception as e:
            logger.error(f"Error creating knowledge base {name}: {e}")
            raise
    
    def add_file_to_knowledge_base(self, kb_name: str, file_id: str) -> Dict:
        """
        Add a file to a knowledge base.
        
        Args:
            kb_name: Name of the knowledge base
            file_id: ID of the file to add
            
        Returns:
            Response data
        """
        try:
            # Get KB list to find the KB ID
            kb_list = self.list_knowledge_bases()
            kb_id = None
            for kb in kb_list:
                if kb.get("name") == kb_name:
                    kb_id = kb.get("id")
                    break
            
            if not kb_id:
                raise ValueError(f"Knowledge base '{kb_name}' not found")
            
            url = f"{self.api_base}/api/v1/knowledge/{kb_id}/file/add"
            payload = {"file_id": file_id}
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Added file {file_id} to knowledge base {kb_name}")
            return data
        except Exception as e:
            logger.error(f"Error adding file to knowledge base: {e}")
            raise
    
    def list_knowledge_bases(self) -> List[Dict]:
        """
        List all knowledge bases.
        
        Returns:
            List of knowledge bases with their files
        """
        try:
            url = f"{self.api_base}/api/v1/knowledge/list"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved {len(data)} knowledge bases")
            return data
        except Exception as e:
            logger.error(f"Error listing knowledge bases: {e}")
            raise
    
    def get_file_id_from_kb(
        self,
        kb_list: List[Dict],
        kb_name: str,
        file_name: str,
    ) -> str:
        """
        Get file ID from knowledge base name and file name.
        
        Args:
            kb_list: List of knowledge bases
            kb_name: Name of the knowledge base
            file_name: Name of the file
            
        Returns:
            File ID
            
        Raises:
            ValueError: If KB or file not found
        """
        for kb in kb_list:
            if kb.get("name") == kb_name:
                for f in kb.get("files", []):
                    meta = f.get("meta", {})
                    if meta.get("name") == file_name:
                        logger.info(f"Found file ID for {file_name} in {kb_name}")
                        return f["id"]
                
                available_files = [f.get('meta', {}).get('name') for f in kb.get('files', [])]
                error_msg = f"File '{file_name}' not found in KB '{kb_name}'. Available: {available_files}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        available_kbs = [kb.get('name') for kb in kb_list]
        error_msg = f"Knowledge base '{kb_name}' not found. Available: {available_kbs}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    def chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "protected.gpt-5",
        temperature: float = 0.2,
    ) -> str:
        """
        Get chat completion from TAMU API.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            model: Model to use
            temperature: Temperature for generation
            
        Returns:
            Model response content
        """
        try:
            url = f"{self.openai_base}/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
                "stream": False,
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            logger.info(f"Successfully got chat completion (length: {len(content)})")
            return content
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    def chat_with_kb_file(
        self,
        kb_name: str,
        file_name: str,
        base_system_prompt: str,
        base_user_prompt: str,
        model: str = "protected.gpt-5",
        temperature: float = 0.2,
    ) -> str:
        """
        Chat with a file from knowledge base.
        
        Args:
            kb_name: Knowledge base name
            file_name: File name in the knowledge base
            base_system_prompt: Base system prompt
            base_user_prompt: Base user prompt
            model: Model to use
            temperature: Temperature for generation
            
        Returns:
            Model response content
        """
        try:
            kb_list = self.list_knowledge_bases()
            file_id = self.get_file_id_from_kb(kb_list, kb_name, file_name)
            
            # Augment prompts with file information
            system_prompt = (
                base_system_prompt
                + "\n\nYou have access to a knowledge-base document with:\n"
                f"- knowledge_base_name: {kb_name}\n"
                f"- file_id: {file_id}\n"
                f"- filename: {file_name}\n"
                "Use the contents of that document when answering the user."
            )
            
            user_prompt = (
                base_user_prompt
                + "\n\nThe document I want you to explain is the knowledge-base file with:\n"
                f"- knowledge_base_name: {kb_name}\n"
                f"- file_id: {file_id}\n"
                f"- filename: {file_name}\n"
                "Please base your explanation on that document."
            )
            
            logger.info(f"Processing file {file_name} from KB {kb_name}")
            return self.chat_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=temperature,
            )
        except Exception as e:
            logger.error(f"Error in chat_with_kb_file for {file_name}: {e}")
            raise
    
    def get_file_content(self, kb_name: str, file_name: str) -> str:
        """
        Get the text content of a file from knowledge base.
        
        Args:
            kb_name: Knowledge base name
            file_name: File name in the knowledge base
            
        Returns:
            File content as text
        """
        try:
            return self.chat_with_kb_file(
                kb_name=kb_name,
                file_name=file_name,
                base_system_prompt="You are a document reader. Extract and return ONLY the text content of the document without any additional commentary or formatting.",
                base_user_prompt="Please provide the complete text content of this document exactly as it appears.",
                temperature=0.0
            )
        except Exception as e:
            logger.error(f"Error getting file content for {file_name}: {e}")
            raise
