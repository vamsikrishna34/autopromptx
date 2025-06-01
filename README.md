# AutoPromptX Enhanced - User Guide

## Overview

AutoPromptX Enhanced is a powerful command-line tool for prompt engineering with GPT models. This enhanced version builds upon the original AutoPromptX with several new features:

1. **Template System**: Fully functional template management with variable substitution
2. **Prompt Management**: Save, categorize, and track prompt history
3. **Enhanced CLI**: Improved command structure and colorized output
4. **Model Configuration**: Support for different models and customizable parameters
5. **Advanced Features**: Prompt chaining and analytics capabilities

## Installation

### Prerequisites

- Python 3.6 or higher
- OpenAI API key

### Setup

1. Unzip the package to your desired location
2. Install required dependencies:
   ```
   pip install openai
   ```
3. Set your OpenAI API key as an environment variable:
   ```
   # On Linux/Mac
   export OPENAI_API_KEY=your_key_here
   
   # On Windows
   set OPENAI_API_KEY=your_key_here
   ```

## Usage

### Basic Commands

```
# Show help
python autopromptx.py --help

# Run a prompt
python autopromptx.py run "Your prompt text here"

# Interactive mode
python autopromptx.py run
```

### Template Management

```
# List available templates
python autopromptx.py template list

# Show template content
python autopromptx.py template show template_name

# Create a new template
python autopromptx.py template create template_name --content "Template content with {{variables}}"

# Edit a template
python autopromptx.py template edit template_name

# Delete a template
python autopromptx.py template delete template_name
```

### Using Templates with Variables

```
# Run with a template and variables
python autopromptx.py run --template greeting --var name=John --var tone=friendly

# If variables are missing, you'll be prompted to enter them
```

### Prompt Management

```
# Save a prompt
python autopromptx.py run "Your prompt" --save prompt_name

# List saved prompts
python autopromptx.py prompt list

# Show a saved prompt
python autopromptx.py prompt show prompt_name

# Delete a saved prompt
python autopromptx.py prompt delete prompt_name
```

### Prompt History

```
# View prompt history
python autopromptx.py history list

# Limit history items
python autopromptx.py history list --limit 5
```

### Configuration

```
# Show current configuration
python autopromptx.py config show

# Set model
python autopromptx.py config set model gpt-4

# Set parameters
python autopromptx.py config set temperature 0.8
python autopromptx.py config set max_tokens 2000

# Save configuration profile
python autopromptx.py config profile save creative_mode

# Load configuration profile
python autopromptx.py config profile load creative_mode

# List available profiles
python autopromptx.py config profile list
```

## Project Structure

```
AutoPromptX/
├── autopromptx.py           # Main application entry point
├── config.py                # Configuration management
├── templates/               # Template directory
│   ├── greeting.txt
│   ├── summary.txt
│   └── ...
├── lib/                     # Core functionality modules
│   ├── template_manager.py  # Template loading and processing
│   ├── prompt_manager.py    # Prompt storage and retrieval
│   ├── model_manager.py     # Model configuration and API handling
│   └── cli_manager.py       # Enhanced CLI interface
├── data/                    # Data storage
│   ├── history/             # Prompt history storage
│   ├── config/              # User configurations
│   └── analytics/           # Usage analytics
└── utils/                   # Utility functions
```

## Testing

For development and testing without an API key, you can use the test version:

```
python autopromptx_test.py
```

This version uses mock responses instead of actual API calls.

## Troubleshooting

### API Key Issues

If you encounter errors about the API key:
- Ensure the OPENAI_API_KEY environment variable is set correctly
- Check that your API key is valid and has sufficient credits

### Template Errors

If template rendering fails:
- Check that all required variables are provided
- Verify the template syntax (variables should be in the format {{variable_name}})

### Database Errors

If you encounter database errors:
- Ensure the data directory is writable
- Try deleting the database file in data/history/ to reset (this will clear history)

## Future Development

The architecture is designed to allow for future extensions:
- GUI integration with Streamlit
- VS Code extension for inline prompt testing
- Prompt version control & analytics
- Support for multiple AI providers

## Support

For issues, questions, or feature requests, please contact the developer.
