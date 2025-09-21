# Production Gemini API integration

import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)

def ai_process_command(raw_cmd):
    """
    Process user command with Gemini AI for translation and safety check.
    Returns: (safe_cmd, risk_level)
    """
    if not API_KEY:
        # Fallback if no API key
        return raw_cmd, False

    try:
        prompt = f"""
You are an AI command translator for a cross-platform terminal. Translate natural language to shell commands.

PLATFORM: Windows (use 'start' for apps, 'echo.' for files, 'del' for deletion, 'dir' for listing)
CONTEXT: User wants to execute terminal commands safely

COMMAND PATTERNS:
- File creation: "create/make X file" → "echo. > X"
- File listing: "list/show files" → "dir" 
- Directory change: "go to X" → "cd X"
- App launch: "open X" → "start X" (use executable names: chrome, firefox, notepad, calc, etc.)
- Deletion: "delete X" → "del X" (mark risky if broad)

RISK RULES: Mark risky if command could harm system or delete multiple files.

User input: "{raw_cmd}"

Respond ONLY with JSON:
{{"command": "shell_command", "risky": true/false, "reason": "explanation_if_risky"}}

Examples:
"create a txt file called test.txt" → {{"command": "echo. > test.txt", "risky": false, "reason": ""}}
"open google chrome" → {{"command": "start chrome", "risky": false, "reason": ""}}
"open firefox" → {{"command": "start firefox", "risky": false, "reason": ""}}
"delete all files" → {{"command": "del *", "risky": true, "reason": "Deletes all files"}}
"list files" → {{"command": "dir", "risky": false, "reason": ""}}
"create folder called mydir" → {{"command": "mkdir mydir", "risky": false, "reason": ""}}
"""

        response = model.generate_content(prompt)
        result = response.text.strip()

        # Extract JSON from markdown code blocks if present
        if result.startswith('```json'):
            result = result.replace('```json', '').replace('```', '').strip()
        elif result.startswith('```'):
            result = result.replace('```', '').strip()

        # Parse JSON response
        import json
        try:
            parsed = json.loads(result)
            return parsed["command"], parsed["risky"]
        except json.JSONDecodeError:
            # Fallback to original command if parsing fails
            return raw_cmd, False

    except Exception as e:
        print(f"AI processing error: {e}")
        return raw_cmd, False

def needs_confirmation(cmd):
    """
    Determine if a command needs user confirmation based on risk patterns.
    """
    risky_patterns = [
        "rm -rf",
        "rm -r",
        "del /f /s",
        "format",
        "fdisk",
        "dd if=",
        "mkfs",
        "sudo",
        "su",
        "chmod 777",
        "chown root",
        "passwd",
        "shutdown",
        "reboot",
        "halt",
        "poweroff"
    ]

    cmd_lower = cmd.lower()
    return any(pattern in cmd_lower for pattern in risky_patterns)
