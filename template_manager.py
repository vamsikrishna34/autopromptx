"""
Template Manager for AutoPromptX

This module handles loading, rendering, and managing prompt templates.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

class Template:
    """Class representing a single prompt template with variable substitution."""
    
    def __init__(self, name: str, content: str):
        """
        Initialize a template with name and content.
        
        Args:
            name: The name of the template
            content: The template content with optional variables
        """
        self.name = name
        self.content = content
        self._variable_pattern = re.compile(r'\{\{([a-zA-Z0-9_]+)\}\}')
    
    def get_variables(self) -> List[str]:
        """
        Extract all variable names from the template.
        
        Returns:
            List of variable names found in the template
        """
        return list(set(self._variable_pattern.findall(self.content)))
    
    def render(self, **variables) -> str:
        """
        Render the template by substituting variables.
        
        Args:
            **variables: Keyword arguments for variable substitution
            
        Returns:
            Rendered template with variables substituted
            
        Raises:
            ValueError: If a required variable is missing
        """
        result = self.content
        for var_name in self.get_variables():
            if var_name not in variables:
                raise ValueError(f"Missing required variable: {var_name}")
            
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, str(variables[var_name]))
            
        return result


class TemplateManager:
    """Manager for handling prompt templates."""
    
    def __init__(self, templates_dir: str):
        """
        Initialize the template manager with a templates directory.
        
        Args:
            templates_dir: Path to the directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        self._ensure_templates_dir()
        self._templates_cache: Dict[str, Template] = {}
    
    def _ensure_templates_dir(self) -> None:
        """Ensure the templates directory exists."""
        os.makedirs(self.templates_dir, exist_ok=True)
    
    def list_templates(self) -> List[str]:
        """
        List all available template names.
        
        Returns:
            List of template names (without file extensions)
        """
        return [f.stem for f in self.templates_dir.glob("*.txt")]
    
    def load(self, template_name: str) -> Template:
        """
        Load a template by name.
        
        Args:
            template_name: Name of the template to load (without extension)
            
        Returns:
            Template object
            
        Raises:
            FileNotFoundError: If the template doesn't exist
        """
        # Check cache first
        if template_name in self._templates_cache:
            return self._templates_cache[template_name]
        
        # Load from file
        template_path = self.templates_dir / f"{template_name}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        template = Template(template_name, content)
        self._templates_cache[template_name] = template
        return template
    
    def save(self, template_name: str, content: str) -> Template:
        """
        Save a template.
        
        Args:
            template_name: Name for the template (without extension)
            content: Template content
            
        Returns:
            The saved Template object
        """
        template_path = self.templates_dir / f"{template_name}.txt"
        
        with open(template_path, 'w') as f:
            f.write(content)
        
        template = Template(template_name, content)
        self._templates_cache[template_name] = template
        return template
    
    def delete(self, template_name: str) -> bool:
        """
        Delete a template.
        
        Args:
            template_name: Name of the template to delete
            
        Returns:
            True if deleted, False if not found
        """
        template_path = self.templates_dir / f"{template_name}.txt"
        
        if not template_path.exists():
            return False
        
        os.remove(template_path)
        
        if template_name in self._templates_cache:
            del self._templates_cache[template_name]
            
        return True
    
    def get_template_content(self, template_name: str) -> Optional[str]:
        """
        Get the raw content of a template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template content or None if not found
        """
        try:
            template = self.load(template_name)
            return template.content
        except FileNotFoundError:
            return None
