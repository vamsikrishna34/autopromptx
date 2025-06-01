"""
Model Manager for AutoPromptX (Test Version)

This module handles model configuration, API interactions, and response generation.
This version is modified for testing without an actual API key.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class ModelManager:
    """Manager for handling AI model configurations and API calls."""
    
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_PARAMS = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    
    def __init__(self, config_dir: str):
        """
        Initialize the model manager with a configuration directory.
        
        Args:
            config_dir: Path to the directory for storing configurations
        """
        self.config_dir = Path(config_dir)
        self._ensure_config_dir()
        self.current_model = self.DEFAULT_MODEL
        self.current_params = self.DEFAULT_PARAMS.copy()
        # No API key loading in test version
        
    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)
        
    def _load_api_key(self) -> None:
        """Mock API key loading for testing."""
        pass
        
    def set_model(self, model_name: str) -> None:
        """
        Set the current model.
        
        Args:
            model_name: Name of the model to use
        """
        self.current_model = model_name
        
    def get_model(self) -> str:
        """
        Get the current model name.
        
        Returns:
            Current model name
        """
        return self.current_model
        
    def set_parameter(self, param_name: str, param_value: Any) -> None:
        """
        Set a model parameter.
        
        Args:
            param_name: Name of the parameter
            param_value: Value for the parameter
        
        Raises:
            ValueError: If the parameter name is invalid
        """
        if param_name not in self.DEFAULT_PARAMS:
            raise ValueError(f"Invalid parameter: {param_name}")
        
        self.current_params[param_name] = param_value
        
    def get_parameter(self, param_name: str) -> Any:
        """
        Get a model parameter value.
        
        Args:
            param_name: Name of the parameter
            
        Returns:
            Current value of the parameter
            
        Raises:
            ValueError: If the parameter name is invalid
        """
        if param_name not in self.current_params:
            raise ValueError(f"Invalid parameter: {param_name}")
            
        return self.current_params[param_name]
        
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all current parameters.
        
        Returns:
            Dictionary of all parameters
        """
        return self.current_params.copy()
        
    def save_profile(self, profile_name: str, params: Optional[Dict[str, Any]] = None) -> None:
        """
        Save the current configuration as a profile.
        
        Args:
            profile_name: Name for the profile
            params: Optional parameters to override current settings
        """
        if params is None:
            params = {}
            
        profile = {
            "model": self.current_model,
            "parameters": {**self.current_params, **params}
        }
        
        profile_path = self.config_dir / f"{profile_name}.json"
        
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
            
    def load_profile(self, profile_name: str) -> bool:
        """
        Load a saved profile.
        
        Args:
            profile_name: Name of the profile to load
            
        Returns:
            True if loaded successfully, False if not found
        """
        profile_path = self.config_dir / f"{profile_name}.json"
        
        if not profile_path.exists():
            return False
            
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        self.current_model = profile.get("model", self.DEFAULT_MODEL)
        self.current_params = profile.get("parameters", self.DEFAULT_PARAMS.copy())
        
        return True
        
    def list_profiles(self) -> List[str]:
        """
        List all available profiles.
        
        Returns:
            List of profile names (without file extensions)
        """
        return [f.stem for f in self.config_dir.glob("*.json")]
        
    def generate_response(self, prompt: str) -> str:
        """
        Generate a mock response for testing.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated mock response text
        """
        return f"[TEST RESPONSE] This is a mock response for: {prompt[:50]}..."
