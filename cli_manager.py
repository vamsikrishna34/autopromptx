"""
CLI Manager for AutoPromptX

This module handles the command-line interface and user interaction.
"""

import os
import sys
import argparse
import textwrap
from typing import Dict, List, Optional, Any, Callable

class ColorFormatter:
    """Utility class for colorized terminal output."""
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @staticmethod
    def format(text: str, *styles: str) -> str:
        """
        Format text with specified styles.
        
        Args:
            text: Text to format
            *styles: Style codes to apply
            
        Returns:
            Formatted text
        """
        return "".join(styles) + text + ColorFormatter.RESET
    
    @staticmethod
    def success(text: str) -> str:
        """Format text as success message."""
        return ColorFormatter.format(text, ColorFormatter.GREEN, ColorFormatter.BOLD)
    
    @staticmethod
    def error(text: str) -> str:
        """Format text as error message."""
        return ColorFormatter.format(text, ColorFormatter.RED, ColorFormatter.BOLD)
    
    @staticmethod
    def warning(text: str) -> str:
        """Format text as warning message."""
        return ColorFormatter.format(text, ColorFormatter.YELLOW, ColorFormatter.BOLD)
    
    @staticmethod
    def info(text: str) -> str:
        """Format text as info message."""
        return ColorFormatter.format(text, ColorFormatter.BLUE)
    
    @staticmethod
    def highlight(text: str) -> str:
        """Format text as highlighted."""
        return ColorFormatter.format(text, ColorFormatter.CYAN, ColorFormatter.BOLD)
    
    @staticmethod
    def title(text: str) -> str:
        """Format text as title."""
        return ColorFormatter.format(text, ColorFormatter.MAGENTA, ColorFormatter.BOLD)


class CLIManager:
    """Manager for handling command-line interface and user interaction."""
    
    def __init__(self):
        """Initialize the CLI manager."""
        self.parser = argparse.ArgumentParser(
            description="AutoPromptX - GPT Prompt Engineering CLI Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.subparsers = self.parser.add_subparsers(dest="command", help="Command to execute")
        self._register_commands()
        
    def _register_commands(self) -> None:
        """Register all available commands."""
        # Run command
        run_parser = self.subparsers.add_parser("run", help="Run a prompt")
        run_parser.add_argument("prompt", nargs="?", help="Prompt text (if not provided, will use interactive mode)")
        run_parser.add_argument("--template", "-t", help="Template to use")
        run_parser.add_argument("--var", "-v", action="append", help="Template variables in format name=value")
        run_parser.add_argument("--model", "-m", help="Model to use")
        run_parser.add_argument("--temperature", type=float, help="Temperature parameter")
        run_parser.add_argument("--max-tokens", type=int, help="Maximum tokens parameter")
        run_parser.add_argument("--save", "-s", help="Save the prompt with this name")
        
        # Template commands
        template_parser = self.subparsers.add_parser("template", help="Template management")
        template_subparsers = template_parser.add_subparsers(dest="template_command", help="Template command")
        
        # Template list
        template_subparsers.add_parser("list", help="List available templates")
        
        # Template show
        template_show = template_subparsers.add_parser("show", help="Show template content")
        template_show.add_argument("name", help="Template name")
        
        # Template create
        template_create = template_subparsers.add_parser("create", help="Create a new template")
        template_create.add_argument("name", help="Template name")
        template_create.add_argument("--content", "-c", help="Template content (if not provided, will open editor)")
        
        # Template edit
        template_edit = template_subparsers.add_parser("edit", help="Edit a template")
        template_edit.add_argument("name", help="Template name")
        
        # Template delete
        template_delete = template_subparsers.add_parser("delete", help="Delete a template")
        template_delete.add_argument("name", help="Template name")
        
        # Prompt commands
        prompt_parser = self.subparsers.add_parser("prompt", help="Prompt management")
        prompt_subparsers = prompt_parser.add_subparsers(dest="prompt_command", help="Prompt command")
        
        # Prompt list
        prompt_list = prompt_subparsers.add_parser("list", help="List saved prompts")
        prompt_list.add_argument("--tag", "-t", action="append", help="Filter by tag")
        
        # Prompt show
        prompt_show = prompt_subparsers.add_parser("show", help="Show saved prompt")
        prompt_show.add_argument("name", help="Prompt name")
        
        # Prompt delete
        prompt_delete = prompt_subparsers.add_parser("delete", help="Delete saved prompt")
        prompt_delete.add_argument("name", help="Prompt name")
        
        # History commands
        history_parser = self.subparsers.add_parser("history", help="Prompt history")
        history_subparsers = history_parser.add_subparsers(dest="history_command", help="History command")
        
        # History list
        history_list = history_subparsers.add_parser("list", help="List prompt history")
        history_list.add_argument("--limit", "-l", type=int, default=10, help="Maximum number of items")
        history_list.add_argument("--offset", "-o", type=int, default=0, help="Offset for pagination")
        history_list.add_argument("--tag", "-t", action="append", help="Filter by tag")
        
        # History show
        history_show = history_subparsers.add_parser("show", help="Show history item")
        history_show.add_argument("id", type=int, help="History item ID")
        
        # Config commands
        config_parser = self.subparsers.add_parser("config", help="Configuration management")
        config_subparsers = config_parser.add_subparsers(dest="config_command", help="Config command")
        
        # Config show
        config_subparsers.add_parser("show", help="Show current configuration")
        
        # Config set
        config_set = config_subparsers.add_parser("set", help="Set configuration parameter")
        config_set.add_argument("name", help="Parameter name")
        config_set.add_argument("value", help="Parameter value")
        
        # Config profile commands
        config_profile = config_subparsers.add_parser("profile", help="Configuration profile management")
        config_profile_subparsers = config_profile.add_subparsers(dest="profile_command", help="Profile command")
        
        # Config profile list
        config_profile_subparsers.add_parser("list", help="List available profiles")
        
        # Config profile save
        config_profile_save = config_profile_subparsers.add_parser("save", help="Save current configuration as profile")
        config_profile_save.add_argument("name", help="Profile name")
        
        # Config profile load
        config_profile_load = config_profile_subparsers.add_parser("load", help="Load configuration profile")
        config_profile_load.add_argument("name", help="Profile name")
        
        # Config profile delete
        config_profile_delete = config_profile_subparsers.add_parser("delete", help="Delete configuration profile")
        config_profile_delete.add_argument("name", help="Profile name")
        
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command-line arguments.
        
        Args:
            args: Command-line arguments (if None, uses sys.argv)
            
        Returns:
            Parsed arguments
        """
        return self.parser.parse_args(args)
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        welcome_text = """
        ╔═══════════════════════════════════════════════════════════╗
        ║                                                           ║
        ║   █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗██╗  ██╗   ║
        ║  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝╚██╗██╔╝   ║
        ║  ███████║██║   ██║   ██║   ██║   ██║██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║    ╚███╔╝    ║
        ║  ██╔══██║██║   ██║   ██║   ██║   ██║██╔═══╝ ██╔═══╝ ██║   ██║██║╚██╔╝██║██╔═══╝    ██║    ██╔██╗    ║
        ║  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     ██║     ╚██████╔╝██║ ╚═╝ ██║██║        ██║   ██╔╝ ██╗   ║
        ║  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝      ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝   ╚═╝  ╚═╝   ║
        ║                                                           ║
        ║                GPT Prompt Engineering CLI Tool            ║
        ║                                                           ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        print(ColorFormatter.format(welcome_text, ColorFormatter.CYAN))
        print(ColorFormatter.format("Type 'autopromptx --help' for usage information.", ColorFormatter.YELLOW))
        print()
        
    def print_success(self, message: str) -> None:
        """
        Print success message.
        
        Args:
            message: Success message
        """
        print(ColorFormatter.success(f"✓ {message}"))
        
    def print_error(self, message: str) -> None:
        """
        Print error message.
        
        Args:
            message: Error message
        """
        print(ColorFormatter.error(f"✗ {message}"), file=sys.stderr)
        
    def print_warning(self, message: str) -> None:
        """
        Print warning message.
        
        Args:
            message: Warning message
        """
        print(ColorFormatter.warning(f"⚠ {message}"))
        
    def print_info(self, message: str) -> None:
        """
        Print info message.
        
        Args:
            message: Info message
        """
        print(ColorFormatter.info(f"ℹ {message}"))
        
    def print_title(self, title: str) -> None:
        """
        Print section title.
        
        Args:
            title: Section title
        """
        print()
        print(ColorFormatter.title(f"=== {title} ==="))
        print()
        
    def print_response(self, response: str) -> None:
        """
        Print formatted response.
        
        Args:
            response: Response text
        """
        print()
        print(ColorFormatter.format("─" * 50, ColorFormatter.BLUE))
        print(response)
        print(ColorFormatter.format("─" * 50, ColorFormatter.BLUE))
        print()
        
    def prompt_input(self, prompt_text: str) -> str:
        """
        Get user input with prompt.
        
        Args:
            prompt_text: Prompt text
            
        Returns:
            User input
        """
        return input(ColorFormatter.format(f"{prompt_text}: ", ColorFormatter.CYAN))
        
    def prompt_confirmation(self, prompt_text: str) -> bool:
        """
        Get user confirmation.
        
        Args:
            prompt_text: Prompt text
            
        Returns:
            True if confirmed, False otherwise
        """
        response = input(ColorFormatter.format(f"{prompt_text} (y/n): ", ColorFormatter.YELLOW)).lower()
        return response in ("y", "yes")
        
    def interactive_mode(self, callback: Callable[[str], str]) -> None:
        """
        Run interactive prompt mode.
        
        Args:
            callback: Function to call with user input
        """
        self.print_info("Interactive mode. Type 'exit' to quit.")
        
        while True:
            try:
                user_input = self.prompt_input("Enter your prompt")
                
                if user_input.lower() in ("exit", "quit"):
                    break
                    
                if not user_input.strip():
                    continue
                    
                response = callback(user_input)
                self.print_response(response)
                
            except KeyboardInterrupt:
                print()
                self.print_warning("Interrupted by user.")
                break
                
            except Exception as e:
                self.print_error(f"Error: {str(e)}")
                
        self.print_info("Exiting interactive mode.")
