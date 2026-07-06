# 🧠 Cognitive Agent - Interactive Learning System

A sophisticated knowledge management system with a web interface that allows you to learn, reason about, and synthesize concepts across multiple domains.

## Features

✨ **Learn** - Teach the agent new concepts in any domain  
🤔 **Reason** - Ask the agent to explain concepts it knows  
🔗 **Synthesize** - Connect concepts across different domains  
💾 **Persistent Memory** - All knowledge is saved locally  
🌐 **Web Interface** - Beautiful, interactive UI  

## Quick Start

### Option 1: Use the Web Interface (No Installation)

1. Simply open `index.html` in your web browser
2. Start learning concepts, asking the agent to reason, and synthesizing ideas
3. All your knowledge is saved in your browser's local storage

### Option 2: Run with Python Flask Server

1. **Install Flask:**
   ```bash
   pip install flask
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## How to Use

### 📖 Learn Tab
- **Domain:** Enter the category (e.g., "Biology", "Physics", "Technology")
- **Concept:** Enter the concept name (e.g., "Photosynthesis", "Gravity")
- **Definition:** Provide an explanation or definition
- Click **Learn** to integrate it into the knowledge base

Example:
- Domain: `Biology`
- Concept: `Photosynthesis`
- Definition: `The process by which plants convert light energy into chemical energy to fuel growth`

### 🤔 Reason Tab
- Enter any concept you want to understand
- The agent searches its knowledge base
- Get detailed explanations with the domain context

Example:
- Input: `DNA`
- Output: Detailed explanation from the Biology domain

### 🔗 Synthesize Tab
- Enter two different concepts
- The agent finds connections between them
- Discover how ideas relate across domains

Example:
- Concept 1: `Gravity`
- Concept 2: `Evolution`
- Output: How these concepts relate at a fundamental level

### 📚 Knowledge Base Tab
- View all learned concepts organized by domain
- See your entire knowledge base at a glance

## Built-in Knowledge

The agent comes with foundational knowledge in three domains:

### Physics
- Gravity
- Inertia
- Entropy

### Biology
- Evolution
- DNA
- Homeostasis

### Math
- Algebra
- Calculus
- Logic

## Architecture

### Frontend (`index.html`)
- Pure HTML/CSS/JavaScript
- No dependencies required
- Uses browser's localStorage for persistence
- Responsive design with gradient UI

### Backend (`app.py`)
- Flask web server (optional)
- RESTful API endpoints
- JSON-based knowledge storage
- Easy to extend and customize

### Core Engine (`agent.py` or embedded in Flask)
- Knowledge hierarchy management
- Concept reasoning and retrieval
- Concept synthesis and connection
- Persistent memory with JSON storage

## API Endpoints (When using Flask)

### POST /api/learn
Learn a new concept
```json
{
  "domain": "Biology",
  "concept": "Photosynthesis",
  "definition": "The process by which plants convert light energy..."
}
```

### POST /api/reason
Reason about a concept
```json
{
  "concept": "DNA"
}
```

### POST /api/synthesize
Synthesize two concepts
```json
{
  "concept1": "Gravity",
  "concept2": "Evolution"
}
```

### GET /api/knowledge
Get all knowledge in the system

## Data Storage

- **Web Interface:** Uses browser's `localStorage` - persists across sessions
- **Flask Server:** Uses `cognitive_nexus.json` file in the server directory

## Customization

### Add New Domains
Edit the initial `nexus` object in either `index.html` or `app.py`:
```javascript
"astronomy": {
  "stellar_fusion": "The nuclear process that powers stars...",
  "black_holes": "Regions of spacetime with extreme gravity..."
}
```

### Styling
Modify the CSS in `index.html` to customize colors, fonts, and layout

### API Integration
The Flask backend can be easily integrated with external services or databases

## Browser Compatibility

- Chrome/Edge: ✅ Fully supported
- Firefox: ✅ Fully supported
- Safari: ✅ Fully supported
- IE 11: ⚠️ Requires polyfills

## System Requirements

### Web Interface Only
- Any modern web browser
- No installation needed

### With Flask Server
- Python 3.7+
- Flask (`pip install flask`)

## Troubleshooting

### Knowledge not saving
- Check if your browser allows localStorage
- Try a different browser
- Use the Flask server option

### Flask server won't start
- Ensure Python 3.7+ is installed
- Install Flask: `pip install flask`
- Try a different port: Edit `port=5000` in `app.py`

### Concept not found
- Check spelling (case-insensitive)
- Make sure you've taught it first using the Learn tab

## Future Enhancements

- 🔍 Advanced search and filtering
- 📊 Knowledge visualization and mind maps
- 🌍 Multi-user collaboration
- 🤖 AI-powered concept suggestions
- 📱 Mobile app version
- 🔐 User accounts and cloud sync

## License

Open source - feel free to use and modify!

## Creator

Built with ❤️ by raftraders786-boop

---

**Happy Learning!** 🧠✨
