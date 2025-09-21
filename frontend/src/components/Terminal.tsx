'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';

// Terminal themes
const themes = {
  dark: {
    bg: 'bg-gray-900',
    text: 'text-green-400',
    prompt: 'text-cyan-400',
    output: 'text-gray-300',
    error: 'text-red-400',
    border: 'border-gray-700',
    header: 'bg-gray-800'
  },
  light: {
    bg: 'bg-white',
    text: 'text-gray-900',
    prompt: 'text-blue-600',
    output: 'text-gray-700',
    error: 'text-red-600',
    border: 'border-gray-300',
    header: 'bg-gray-100'
  },
  matrix: {
    bg: 'bg-black',
    text: 'text-green-400',
    prompt: 'text-green-300',
    output: 'text-green-500',
    error: 'text-red-400',
    border: 'border-green-500',
    header: 'bg-gray-900'
  },
  retro: {
    bg: 'bg-blue-900',
    text: 'text-yellow-400',
    prompt: 'text-yellow-300',
    output: 'text-yellow-200',
    error: 'text-red-400',
    border: 'border-yellow-600',
    header: 'bg-blue-800'
  }
};

interface TerminalLine {
  id: string;
  type: 'input' | 'output' | 'error' | 'system';
  content: string;
  timestamp: Date;
}

interface TerminalProps {
  initialTheme?: keyof typeof themes;
  initialPrompt?: string;
  maxLines?: number;
}

const Terminal: React.FC<TerminalProps> = ({
  initialTheme = 'dark',
  initialPrompt = 'ai-os>',
  maxLines = 1000
}) => {
  const [theme, setTheme] = useState<keyof typeof themes>(initialTheme);
  const [prompt, setPrompt] = useState(initialPrompt);
  const [lines, setLines] = useState<TerminalLine[]>([
    {
      id: '1',
      type: 'system',
      content: '🤖 AI Terminal v2.0 - Modern Web Interface',
      timestamp: new Date()
    },
    {
      id: '2',
      type: 'system',
      content: '📦 To get the full experience, clone the repository:',
      timestamp: new Date()
    },
    {
      id: '3',
      type: 'system',
      content: 'git clone https://github.com/saquib34/ai-py-cli.git',
      timestamp: new Date()
    },
    {
      id: '4',
      type: 'system',
      content: '💡 Try: help, cpu, mem, ps, disk, network, sysinfo, uptime',
      timestamp: new Date()
    }
  ]);
  const [currentInput, setCurrentInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [typingText, setTypingText] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [fontSize, setFontSize] = useState(14);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  const inputRef = useRef<HTMLInputElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);
  const cursorIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Cursor blinking effect
  useEffect(() => {
    cursorIntervalRef.current = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 500);

    return () => {
      if (cursorIntervalRef.current) {
        clearInterval(cursorIntervalRef.current);
      }
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [lines]);

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Typing effect function
  const typeText = useCallback(async (text: string, speed: number = 50): Promise<void> => {
    return new Promise((resolve) => {
      setIsTyping(true);
      setTypingText('');
      let index = 0;

      const typeInterval = setInterval(() => {
        if (index < text.length) {
          setTypingText(prev => prev + text[index]);
          index++;
        } else {
          clearInterval(typeInterval);
          setTimeout(() => {
            setIsTyping(false);
            setTypingText('');
            resolve();
          }, 200);
        }
      }, speed);
    });
  }, []);

  // Mock command responses (simulating backend)
  const executeCommand = async (command: string): Promise<string> => {
    const cmd = command.toLowerCase().trim();

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 300));

    switch (cmd) {
      case 'help':
        return `Available commands:
• help - Show this help
• clone - Show repository cloning instructions
• clear - Clear terminal
• history - Show command history
• theme <name> - Change theme (dark, light, matrix, retro)
• prompt <text> - Change prompt
• fontsize <size> - Change font size
• fullscreen - Toggle fullscreen
• cpu - Show CPU information
• mem - Show memory usage
• ps - List running processes
• disk - Show disk usage
• network - Show network stats
• sysinfo - Show system information
• uptime - Show system uptime
• echo <text> - Display text
• date - Show current date/time
• whoami - Show current user`;

      case 'clear':
        setLines([]);
        return '';

      case 'history':
        if (history.length === 0) return 'No command history';
        return history.map((cmd, i) => `${i + 1}. ${cmd}`).join('\n');

      case 'cpu':
        return `CPU Usage: 45.2%
Cores: 8
Frequency: 3.2 GHz
Load Average: 1.2, 1.1, 1.0`;

      case 'mem':
        return `Memory: 67.3% used
Used: 10.8 GB
Total: 16.0 GB
Available: 5.2 GB
Free: 2.1 GB`;

      case 'ps':
        return `PID    NAME                CPU%    MEM%
1      System Idle Process  0.0     0.0
4      System               0.1     0.2
123    chrome.exe          15.2    8.5
456    code.exe             8.3     4.2
789    python.exe           25.1    12.3
... (showing first 5 processes)`;

      case 'disk':
        return `Disk: 58.7% used
Used: 237 GB
Total: 512 GB
Free: 275 GB
Mount: C:\\`;

      case 'network':
        return `Network Statistics:
Bytes Sent: 1.2 GB
Bytes Received: 3.8 GB
Packets Sent: 45,231
Packets Received: 67,892
Active Connections: 23`;

      case 'sysinfo':
        return `System Information:
OS: Windows 11 Pro
Version: 23H2
Build: 22631.4169
Architecture: x64
Hostname: DESKTOP-ABC123
Uptime: 2 days, 4 hours, 23 minutes`;

      case 'uptime':
        return `System Uptime: 2 days, 4 hours, 23 minutes
Boot Time: 2025-09-19 08:37:15`;

      case 'date':
        return new Date().toString();

      case 'clone':
        return `To clone the AI Terminal repository:

GitHub: https://github.com/saquib34/ai-py-cli

Commands:
  git clone https://github.com/saquib34/ai-py-cli.git
  cd ai-py-cli

Backend Setup:
  pip install -r requirements.txt
  echo "GEMINI_API_KEY=your_key_here" > .env


Usage:
  # Terminal 1: Start backend daemon
  python main.py daemon

  # Terminal 2: Start CLI
  python main.py

  # Terminal 3: Open http://localhost:3000 for web interface`;

      default:
        if (cmd.startsWith('echo ')) {
          return command.substring(5);
        }
        if (cmd.startsWith('theme ')) {
          const newTheme = command.split(' ')[1] as keyof typeof themes;
          if (themes[newTheme]) {
            setTheme(newTheme);
            return `Theme changed to: ${newTheme}`;
          }
          return `Available themes: ${Object.keys(themes).join(', ')}`;
        }
        if (cmd.startsWith('prompt ')) {
          const newPrompt = command.split(' ').slice(1).join(' ');
          setPrompt(newPrompt);
          return `Prompt changed to: ${newPrompt}`;
        }
        if (cmd.startsWith('fontsize ')) {
          const size = parseInt(command.split(' ')[1]);
          if (size >= 10 && size <= 24) {
            setFontSize(size);
            return `Font size changed to: ${size}px`;
          }
          return 'Font size must be between 10-24px';
        }
        if (cmd === 'fullscreen') {
          setIsFullscreen(!isFullscreen);
          return `Fullscreen: ${!isFullscreen ? 'ON' : 'OFF'}`;
        }
        return `Command not found: ${command}. Type 'help' for available commands.`;
    }
  };

  const handleCommand = async (command: string) => {
    if (!command.trim()) return;

    // Add input line
    const inputLine: TerminalLine = {
      id: Date.now().toString(),
      type: 'input',
      content: `${prompt} ${command}`,
      timestamp: new Date()
    };

    setLines(prev => [...prev, inputLine]);

    // Add to history
    setHistory(prev => [...prev, command]);
    setHistoryIndex(-1);

    // Execute command
    try {
      const output = await executeCommand(command);

      if (output) {
        // Type out the response with effect
        await typeText(output, 20);

        const outputLine: TerminalLine = {
          id: (Date.now() + 1).toString(),
          type: 'output',
          content: output,
          timestamp: new Date()
        };

        setLines(prev => [...prev, outputLine]);
      }
    } catch (error) {
      const errorLine: TerminalLine = {
        id: (Date.now() + 1).toString(),
        type: 'error',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date()
      };
      setLines(prev => [...prev, errorLine]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const command = currentInput.trim();
      setCurrentInput('');
      handleCommand(command);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex === -1 ? history.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setCurrentInput(history[newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex >= 0) {
        const newIndex = historyIndex + 1;
        if (newIndex >= history.length) {
          setHistoryIndex(-1);
          setCurrentInput('');
        } else {
          setHistoryIndex(newIndex);
          setCurrentInput(history[newIndex]);
        }
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // Simple tab completion for common commands
      const completions = ['help', 'cpu', 'mem', 'ps', 'disk', 'network', 'sysinfo', 'uptime', 'clear', 'history'];
      const match = completions.find(cmd => cmd.startsWith(currentInput));
      if (match) {
        setCurrentInput(match);
      }
    }
  };

  const currentTheme = themes[theme];

  return (
    <div className={`rounded-lg border ${currentTheme.border} overflow-hidden ${isFullscreen ? 'fixed inset-0 z-50' : ''}`}>
      {/* Terminal Header */}
      <div className={`${currentTheme.header} px-4 py-2 flex items-center justify-between border-b ${currentTheme.border}`}>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-sm font-mono ml-2 text-gray-300">AI Terminal</span>
        </div>
        <div className="flex items-center space-x-4 text-xs">
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value as keyof typeof themes)}
            className="bg-gray-700 text-white px-2 py-1 rounded text-xs"
          >
            {Object.keys(themes).map(t => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="text-gray-400 hover:text-white"
          >
            {isFullscreen ? '🗗' : '🗖'}
          </button>
        </div>
      </div>

      {/* Terminal Body */}
      <div
        ref={terminalRef}
        className={`${currentTheme.bg} p-4 h-96 ${isFullscreen ? 'h-screen' : ''} overflow-y-auto font-mono`}
        style={{ fontSize: `${fontSize}px` }}
      >
        {/* Terminal Lines */}
        {lines.map((line) => (
          <div key={line.id} className="mb-1">
            {line.type === 'input' && (
              <div className={currentTheme.prompt}>{line.content}</div>
            )}
            {line.type === 'output' && (
              <div className={currentTheme.output} style={{ whiteSpace: 'pre-line' }}>
                {line.content}
              </div>
            )}
            {line.type === 'error' && (
              <div className={currentTheme.error}>{line.content}</div>
            )}
            {line.type === 'system' && (
              <div className="text-yellow-400 italic">{line.content}</div>
            )}
          </div>
        ))}

        {/* Typing Effect */}
        {isTyping && (
          <div className={currentTheme.output}>
            {typingText}
            <span className={`${currentTheme.text} ${showCursor ? 'opacity-100' : 'opacity-0'}`}>|</span>
          </div>
        )}

        {/* Input Line */}
        {!isTyping && (
          <div className="flex items-center">
            <span className={currentTheme.prompt}>{prompt}</span>
            <input
              ref={inputRef}
              type="text"
              value={currentInput}
              onChange={(e) => setCurrentInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className={`flex-1 bg-transparent outline-none ml-2 ${currentTheme.text}`}
              spellCheck={false}
              autoComplete="off"
            />
            <span className={`${currentTheme.text} ${showCursor ? 'opacity-100' : 'opacity-0'}`}>|</span>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className={`${currentTheme.header} px-4 py-1 text-xs text-gray-400 border-t ${currentTheme.border} flex justify-between`}>
        <span>Lines: {lines.length} | Theme: {theme} | Font: {fontSize}px</span>
        <span>Press ↑↓ for history, Tab for completion</span>
      </div>
    </div>
  );
};

export default Terminal;