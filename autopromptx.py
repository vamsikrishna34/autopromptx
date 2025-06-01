"""
AutoPromptX - GPT Prompt Engineering CLI Tool

Enhanced version with template system, prompt management, and more.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import core modules
from lib.template_manager import TemplateManager
from lib.model_manager import ModelManager
from lib.prompt_manager import PromptManager
from lib.cli_manager import CLIManager, ColorFormatter

class AutoPromptX:
    """Main application class for AutoPromptX."""
    
    def __init__(self):
        """Initialize the AutoPromptX application."""
        # Set up base directories
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.templates_dir = self.base_dir / "templates"
        self.data_dir = self.base_dir / "data"
        self.config_dir = self.data_dir / "config"
        
        # Initialize managers
        self.template_manager = TemplateManager(self.templates_dir)
        self.model_manager = ModelManager(self.config_dir)
        self.prompt_manager = PromptManager(self.data_dir)
        self.cli_manager = CLIManager()
        
        # Copy existing templates if needed
        self._initialize_templates()
        
    def _initialize_templates(self):
        """Initialize template directory with existing templates."""
        # Ensure template directory exists
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Check for existing templates in the original location
        original_greeting = Path(self.base_dir.parent) / "greeting.txt"
        original_summary = Path(self.base_dir.parent) / "summary.txt"
        
        # Copy greeting template if it exists and destination doesn't
        if original_greeting.exists() and not (self.templates_dir / "greeting.txt").exists():
            with open(original_greeting, 'r') as src:
                content = src.read()
                self.template_manager.save("greeting", content)
                
        # Copy summary template if it exists and destination doesn't
        if original_summary.exists() and not (self.templates_dir / "summary.txt").exists():
            with open(original_summary, 'r') as src:
                content = src.read()
                self.template_manager.save("summary", content)
    
    def run(self, args=None):
        """
        Run the application with the given arguments.
        
        Args:
            args: Command-line arguments (if None, uses sys.argv)
        """
        # Parse arguments
        parsed_args = self.cli_manager.parse_args(args)
        
        # Show welcome message if no command specified
        if not parsed_args.command:
            self.cli_manager.print_welcome()
            self.cli_manager.parser.print_help()
            return
            
        # Handle commands
        if parsed_args.command == "run":
            self._handle_run_command(parsed_args)
        elif parsed_args.command == "template":
            self._handle_template_command(parsed_args)
        elif parsed_args.command == "prompt":
            self._handle_prompt_command(parsed_args)
        elif parsed_args.command == "history":
            self._handle_history_command(parsed_args)
        elif parsed_args.command == "config":
            self._handle_config_command(parsed_args)
        else:
            self.cli_manager.print_error(f"Unknown command: {parsed_args.command}")
            
    def _handle_run_command(self, args):
        """
        Handle the 'run' command.
        
        Args:
            args: Parsed arguments
        """
        # Apply model configuration if specified
        if args.model:
            self.model_manager.set_model(args.model)
        if args.temperature is not None:
            self.model_manager.set_parameter("temperature", args.temperature)
        if args.max_tokens is not None:
            self.model_manager.set_parameter("max_tokens", args.max_tokens)
            
        # Interactive mode if no prompt provided
        if not args.prompt and not args.template:
            self.cli_manager.interactive_mode(self._generate_response)
            return
            
        # Get prompt from template if specified
        if args.template:
            try:
                template = self.template_manager.load(args.template)
                
                # Parse variables
                variables = {}
                if args.var:
                    for var_str in args.var:
                        name, value = var_str.split("=", 1)
                        variables[name] = value
                        
                # Check for missing variables
                missing_vars = [var for var in template.get_variables() if var not in variables]
                if missing_vars:
                    for var in missing_vars:
                        variables[var] = self.cli_manager.prompt_input(f"Enter value for '{var}'")
                        
                prompt = template.render(**variables)
            except Exception as e:
                self.cli_manager.print_error(f"Template error: {str(e)}")
                return
        else:
            prompt = args.prompt
            
        # Generate response
        response = self._generate_response(prompt)
        
        # Save prompt if requested
        if args.save:
            try:
                self.prompt_manager.save_prompt(args.save, prompt)
                self.cli_manager.print_success(f"Prompt saved as '{args.save}'")
            except ValueError as e:
                self.cli_manager.print_error(str(e))
                
        # Display response
        self.cli_manager.print_response(response)
        
    def _handle_template_command(self, args):
        """
        Handle the 'template' command.
        
        Args:
            args: Parsed arguments
        """
        if not args.template_command:
            self.cli_manager.print_error("No template command specified")
            return
            
        if args.template_command == "list":
            templates = self.template_manager.list_templates()
            if templates:
                self.cli_manager.print_title("Available Templates")
                for template_name in templates:
                    print(f"- {template_name}")
            else:
                self.cli_manager.print_info("No templates available")
                
        elif args.template_command == "show":
            try:
                content = self.template_manager.get_template_content(args.name)
                if content:
                    self.cli_manager.print_title(f"Template: {args.name}")
                    print(content)
                else:
                    self.cli_manager.print_error(f"Template not found: {args.name}")
            except Exception as e:
                self.cli_manager.print_error(str(e))
                
        elif args.template_command == "create":
            try:
                content = args.content
                if not content:
                    self.cli_manager.print_info(f"Enter template content for '{args.name}' (Ctrl+D to finish):")
                    content_lines = []
                    try:
                        while True:
                            line = input()
                            content_lines.append(line)
                    except EOFError:
                        content = "\n".join(content_lines)
                        print()  # Add newline after EOF
                        
                self.template_manager.save(args.name, content)
                self.cli_manager.print_success(f"Template '{args.name}' created")
            except Exception as e:
                self.cli_manager.print_error(str(e))
                
        elif args.template_command == "edit":
            try:
                content = self.template_manager.get_template_content(args.name)
                if not content:
                    self.cli_manager.print_error(f"Template not found: {args.name}")
                    return
                    
                self.cli_manager.print_info(f"Editing template '{args.name}'. Current content:")
                print(content)
                self.cli_manager.print_info("Enter new content (Ctrl+D to finish):")
                
                content_lines = []
                try:
                    while True:
                        line = input()
                        content_lines.append(line)
                except EOFError:
                    new_content = "\n".join(content_lines)
                    print()  # Add newline after EOF
                    
                self.template_manager.save(args.name, new_content)
                self.cli_manager.print_success(f"Template '{args.name}' updated")
            except Exception as e:
                self.cli_manager.print_error(str(e))
                
        elif args.template_command == "delete":
            if self.cli_manager.prompt_confirmation(f"Are you sure you want to delete template '{args.name}'?"):
                if self.template_manager.delete(args.name):
                    self.cli_manager.print_success(f"Template '{args.name}' deleted")
                else:
                    self.cli_manager.print_error(f"Template not found: {args.name}")
        else:
            self.cli_manager.print_error(f"Unknown template command: {args.template_command}")
            
    def _handle_prompt_command(self, args):
        """
        Handle the 'prompt' command.
        
        Args:
            args: Parsed arguments
        """
        if not args.prompt_command:
            self.cli_manager.print_error("No prompt command specified")
            return
            
        if args.prompt_command == "list":
            prompts = self.prompt_manager.list_saved_prompts(args.tag)
            if prompts:
                self.cli_manager.print_title("Saved Prompts")
                for prompt in prompts:
                    tags = f" [{', '.join(prompt['tags'])}]" if prompt['tags'] else ""
                    desc = f": {prompt['description']}" if prompt['description'] else ""
                    print(f"- {prompt['name']}{tags}{desc}")
            else:
                self.cli_manager.print_info("No saved prompts available")
                
        elif args.prompt_command == "show":
            prompt_data = self.prompt_manager.get_saved_prompt(args.name)
            if prompt_data:
                self.cli_manager.print_title(f"Prompt: {prompt_data['name']}")
                if prompt_data['description']:
                    print(f"Description: {prompt_data['description']}")
                if prompt_data['tags']:
                    print(f"Tags: {', '.join(prompt_data['tags'])}")
                print(f"\nCreated: {prompt_data['created_at']}")
                print(f"Updated: {prompt_data['updated_at']}")
                print("\nContent:")
                print(prompt_data['prompt'])
            else:
                self.cli_manager.print_error(f"Prompt not found: {args.name}")
                
        elif args.prompt_command == "delete":
            if self.cli_manager.prompt_confirmation(f"Are you sure you want to delete prompt '{args.name}'?"):
                if self.prompt_manager.delete_saved_prompt(args.name):
                    self.cli_manager.print_success(f"Prompt '{args.name}' deleted")
                else:
                    self.cli_manager.print_error(f"Prompt not found: {args.name}")
        else:
            self.cli_manager.print_error(f"Unknown prompt command: {args.prompt_command}")
            
    def _handle_history_command(self, args):
        """
        Handle the 'history' command.
        
        Args:
            args: Parsed arguments
        """
        if not args.history_command:
            self.cli_manager.print_error("No history command specified")
            return
            
        if args.history_command == "list":
            history = self.prompt_manager.get_history(args.limit, args.offset, args.tag)
            if history:
                self.cli_manager.print_title("Prompt History")
                for item in history:
                    tags = f" [{', '.join(item['tags'])}]" if item['tags'] else ""
                    timestamp = item['timestamp'].split('T')[0]  # Just the date part
                    print(f"[{item['id']}] {timestamp} - {item['model']}{tags}")
                    print(f"  Prompt: {item['prompt'][:50]}..." if len(item['prompt']) > 50 else f"  Prompt: {item['prompt']}")
                    print()
            else:
                self.cli_manager.print_info("No history available")
        else:
            self.cli_manager.print_error(f"Unknown history command: {args.history_command}")
            
    def _handle_config_command(self, args):
        """
        Handle the 'config' command.
        
        Args:
            args: Parsed arguments
        """
        if not args.config_command:
            self.cli_manager.print_error("No config command specified")
            return
            
        if args.config_command == "show":
            self.cli_manager.print_title("Current Configuration")
            print(f"Model: {self.model_manager.get_model()}")
            print("\nParameters:")
            for name, value in self.model_manager.get_all_parameters().items():
                print(f"  {name}: {value}")
                
        elif args.config_command == "set":
            try:
                # Handle special case for model
                if args.name == "model":
                    self.model_manager.set_model(args.value)
                    self.cli_manager.print_success(f"Model set to '{args.value}'")
                else:
                    # Try to convert value to appropriate type
                    try:
                        value = float(args.value)
                        # Convert to int if it's a whole number
                        if value.is_integer():
                            value = int(value)
                    except ValueError:
                        # Keep as string if not a number
                        value = args.value
                        
                    self.model_manager.set_parameter(args.name, value)
                    self.cli_manager.print_success(f"Parameter '{args.name}' set to '{value}'")
            except ValueError as e:
                self.cli_manager.print_error(str(e))
                
        elif args.config_command == "profile":
            if not args.profile_command:
                self.cli_manager.print_error("No profile command specified")
                return
                
            if args.profile_command == "list":
                profiles = self.model_manager.list_profiles()
                if profiles:
                    self.cli_manager.print_title("Available Profiles")
                    for profile in profiles:
                        print(f"- {profile}")
                else:
                    self.cli_manager.print_info("No profiles available")
                    
            elif args.profile_command == "save":
                self.model_manager.save_profile(args.name)
                self.cli_manager.print_success(f"Profile '{args.name}' saved")
                
            elif args.profile_command == "load":
                if self.model_manager.load_profile(args.name):
                    self.cli_manager.print_success(f"Profile '{args.name}' loaded")
                else:
                    self.cli_manager.print_error(f"Profile not found: {args.name}")
                    
            elif args.profile_command == "delete":
                # This would require adding a delete_profile method to ModelManager
                self.cli_manager.print_error("Profile deletion not implemented yet")
            else:
                self.cli_manager.print_error(f"Unknown profile command: {args.profile_command}")
        else:
            self.cli_manager.print_error(f"Unknown config command: {args.config_command}")
            
    def _generate_response(self, prompt):
        """
        Generate a response for the given prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Generated response
        """
        try:
            # Generate response
            response = self.model_manager.generate_response(prompt)
            
            # Save to history
            self.prompt_manager.save(
                prompt=prompt,
                response=response,
                model=self.model_manager.get_model()
            )
            
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
            
    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'prompt_manager'):
            self.prompt_manager.close()


def main():
    """Main entry point."""
    app = AutoPromptX()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
