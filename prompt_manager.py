"""
Prompt Manager for AutoPromptX

This module handles prompt storage, retrieval, and history tracking.
"""

import os
import json
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

class PromptManager:
    """Manager for handling prompt storage, history, and retrieval."""
    
    def __init__(self, data_dir: str):
        """
        Initialize the prompt manager with a data directory.
        
        Args:
            data_dir: Path to the directory for storing prompt data
        """
        self.data_dir = Path(data_dir)
        self.history_dir = self.data_dir / "history"
        self._ensure_dirs()
        self._init_database()
        
    def _ensure_dirs(self) -> None:
        """Ensure the data directories exist."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        
    def _init_database(self) -> None:
        """Initialize the SQLite database for prompt history."""
        db_path = self.history_dir / "prompt_history.db"
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            model TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            tags TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            prompt TEXT NOT NULL,
            description TEXT,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()
        
    def save(self, prompt: str, response: str, model: str, tags: Optional[List[str]] = None) -> int:
        """
        Save a prompt and its response to history.
        
        Args:
            prompt: The prompt text
            response: The response text
            model: The model used
            tags: Optional list of tags
            
        Returns:
            ID of the saved prompt
        """
        timestamp = datetime.datetime.now().isoformat()
        tags_str = ",".join(tags) if tags else ""
        
        self.cursor.execute(
            "INSERT INTO prompts (prompt, response, model, timestamp, tags) VALUES (?, ?, ?, ?, ?)",
            (prompt, response, model, timestamp, tags_str)
        )
        self.conn.commit()
        
        return self.cursor.lastrowid
        
    def get_history(self, limit: int = 10, offset: int = 0, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get prompt history.
        
        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            tags: Optional filter by tags
            
        Returns:
            List of prompt history items
        """
        query = "SELECT id, prompt, response, model, timestamp, tags FROM prompts"
        params = []
        
        if tags:
            # Build a query that checks if any of the specified tags are in the tags column
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
                
            if tag_conditions:
                query += " WHERE " + " OR ".join(tag_conditions)
                
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        result = []
        for row in rows:
            item = {
                "id": row[0],
                "prompt": row[1],
                "response": row[2],
                "model": row[3],
                "timestamp": row[4],
                "tags": row[5].split(",") if row[5] else []
            }
            result.append(item)
            
        return result
        
    def save_prompt(self, name: str, prompt: str, description: Optional[str] = None, tags: Optional[List[str]] = None) -> int:
        """
        Save a prompt to the library.
        
        Args:
            name: Name for the saved prompt
            prompt: The prompt text
            description: Optional description
            tags: Optional list of tags
            
        Returns:
            ID of the saved prompt
            
        Raises:
            ValueError: If a prompt with the same name already exists
        """
        timestamp = datetime.datetime.now().isoformat()
        tags_str = ",".join(tags) if tags else ""
        
        try:
            self.cursor.execute(
                "INSERT INTO saved_prompts (name, prompt, description, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (name, prompt, description, tags_str, timestamp, timestamp)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"A prompt with the name '{name}' already exists")
            
    def update_saved_prompt(self, name: str, prompt: Optional[str] = None, 
                           description: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Update a saved prompt.
        
        Args:
            name: Name of the prompt to update
            prompt: New prompt text (if None, keeps existing)
            description: New description (if None, keeps existing)
            tags: New tags (if None, keeps existing)
            
        Returns:
            True if updated, False if not found
        """
        # First, get the existing prompt
        self.cursor.execute("SELECT prompt, description, tags FROM saved_prompts WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        
        if not row:
            return False
            
        current_prompt, current_description, current_tags = row
        
        # Use new values or fall back to current values
        new_prompt = prompt if prompt is not None else current_prompt
        new_description = description if description is not None else current_description
        new_tags_str = ",".join(tags) if tags is not None else current_tags
        updated_at = datetime.datetime.now().isoformat()
        
        self.cursor.execute(
            "UPDATE saved_prompts SET prompt = ?, description = ?, tags = ?, updated_at = ? WHERE name = ?",
            (new_prompt, new_description, new_tags_str, updated_at, name)
        )
        self.conn.commit()
        
        return True
        
    def get_saved_prompt(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a saved prompt by name.
        
        Args:
            name: Name of the prompt
            
        Returns:
            Prompt data or None if not found
        """
        self.cursor.execute(
            "SELECT id, name, prompt, description, tags, created_at, updated_at FROM saved_prompts WHERE name = ?",
            (name,)
        )
        row = self.cursor.fetchone()
        
        if not row:
            return None
            
        return {
            "id": row[0],
            "name": row[1],
            "prompt": row[2],
            "description": row[3],
            "tags": row[4].split(",") if row[4] else [],
            "created_at": row[5],
            "updated_at": row[6]
        }
        
    def list_saved_prompts(self, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List all saved prompts.
        
        Args:
            tags: Optional filter by tags
            
        Returns:
            List of saved prompts
        """
        query = "SELECT id, name, description, tags FROM saved_prompts"
        params = []
        
        if tags:
            # Build a query that checks if any of the specified tags are in the tags column
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
                
            if tag_conditions:
                query += " WHERE " + " OR ".join(tag_conditions)
                
        query += " ORDER BY name"
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        
        result = []
        for row in rows:
            item = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "tags": row[3].split(",") if row[3] else []
            }
            result.append(item)
            
        return result
        
    def delete_saved_prompt(self, name: str) -> bool:
        """
        Delete a saved prompt.
        
        Args:
            name: Name of the prompt to delete
            
        Returns:
            True if deleted, False if not found
        """
        self.cursor.execute("DELETE FROM saved_prompts WHERE name = ?", (name,))
        self.conn.commit()
        
        return self.cursor.rowcount > 0
        
    def close(self) -> None:
        """Close the database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()
