# AI Terminal - React Frontend

A modern, fully customizable web-based terminal interface for the AI Terminal system with typing effects and multiple themes.

## ✨ Features

- **🎨 Multiple Themes**: Dark, Light, Matrix, and Retro themes
- **⚡ Typing Effects**: Realistic terminal typing animation
- **🎯 Command History**: Navigate with arrow keys
- **📝 Tab Completion**: Auto-complete common commands
- **🔧 Fully Customizable**: Change prompts, fonts, and layouts
- **📱 Responsive Design**: Works on desktop and mobile
- **🎪 Fullscreen Mode**: Immersive terminal experience
- **💻 System Monitoring**: CPU, Memory, Disk, Network commands

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saquib34/ai-py-cli.git
   cd ai-py-cli/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**
   ```
   http://localhost:3000
   ```

## 🎮 Usage

### Basic Commands
- `help` - Show all available commands
- `clear` - Clear the terminal
- `history` - View command history
- `echo <text>` - Display text
- `date` - Show current date/time
- `whoami` - Show current user

### System Monitoring
- `cpu` - Display CPU information and usage
- `mem` - Show memory usage statistics
- `ps` - List running processes
- `disk` - Display disk usage
- `network` - Show network statistics
- `sysinfo` - Display system information
- `uptime` - Show system uptime

### Customization Commands
- `theme <name>` - Change theme (dark, light, matrix, retro)
- `prompt <text>` - Change command prompt
- `fontsize <size>` - Change font size (10-24px)
- `fullscreen` - Toggle fullscreen mode

### Keyboard Shortcuts
- **↑/↓** - Navigate command history
- **Tab** - Auto-complete commands
- **Enter** - Execute command
- **Click terminal** - Focus input

## 🎨 Themes

### Dark Theme (Default)
- Background: Dark gray
- Text: Green
- Prompt: Cyan
- Perfect for late-night coding

### Light Theme
- Background: White
- Text: Dark gray
- Prompt: Blue
- Great for presentations

### Matrix Theme
- Background: Black
- Text: Bright green
- Inspired by the Matrix movie
- Classic hacker aesthetic

### Retro Theme
- Background: Dark blue
- Text: Yellow
- 80s computer terminal feel

## 🔧 Customization

### Changing Default Settings
Edit the `Terminal` component props in `src/app/page.tsx`:

```tsx
<Terminal
  initialTheme="matrix"        // Default theme
  initialPrompt="user@terminal>" // Default prompt
  maxLines={1000}              // Maximum lines to keep
/>
```

### Adding New Commands
Add commands to the `executeCommand` function in `Terminal.tsx`:

```typescript
case 'mycommand':
  return 'My custom command output';
```

### Custom Themes
Add new themes to the `themes` object:

```typescript
custom: {
  bg: 'bg-purple-900',
  text: 'text-purple-200',
  prompt: 'text-purple-400',
  output: 'text-purple-300',
  error: 'text-red-400',
  border: 'border-purple-600',
  header: 'bg-purple-800'
}
```

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Main page
│   │   └── globals.css    # Global styles
│   └── components/
│       └── Terminal.tsx   # Main terminal component
├── public/                # Static assets
├── package.json          # Dependencies
└── tailwind.config.js   # Tailwind configuration
```

## 🛠️ Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Adding New Features
1. Create new components in `src/components/`
2. Update the Terminal component as needed
3. Add new themes or commands
4. Test thoroughly

### API Integration
To connect with the Python backend:

```typescript
// Add to executeCommand function
case 'backend':
  try {
    const response = await fetch('http://localhost:5000/api/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: args })
    });
    const data = await response.json();
    return data.output;
  } catch (error) {
    return `Backend error: ${error.message}`;
  }
```

## 📱 Mobile Support

The terminal is fully responsive and works on mobile devices:
- Touch-friendly interface
- Responsive font sizes
- Optimized layouts
- Virtual keyboard support

## 🎪 Demo Features

### Typing Effects
- Realistic character-by-character typing
- Adjustable typing speed
- Smooth cursor blinking

### Interactive Elements
- Theme selector dropdown
- Fullscreen toggle button
- Font size controls
- Real-time status display

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This is a frontend interface for the AI Terminal system. Make sure the Python backend is running for full functionality.
