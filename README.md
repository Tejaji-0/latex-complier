# LaTeX Editor - Modern Web-Based LaTeX IDE

A modern, web-based LaTeX editor inspired by Overleaf, built with Flask. Features a beautiful orange color scheme, dark mode support, and a comprehensive project management system for creating and editing LaTeX documents with real-time preview.

## Features

### 🎨 Modern Design
- **Orange Color Palette**: Beautiful, modern orange-themed interface
- **Dark Mode Support**: Toggle between light and dark themes with persistent preference
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Settings Menu**: Convenient top-right settings dropdown with theme toggle

### 📝 Advanced Editor
- **Syntax-Highlighted Editor**: CodeMirror-powered LaTeX editor with intelligent features
- **Real-time Preview**: Live PDF preview with automatic compilation
- **Auto-save**: Automatic file saving with Ctrl+S shortcut
- **Bracket Matching**: Intelligent bracket pairing and matching
- **Code Completion**: LaTeX autocomplete and suggestions

### 🗂️ Project Management
- **Multi-Project Support**: Create and manage multiple LaTeX projects
- **File Tree Navigation**: Organized file structure with intuitive navigation
- **File Management**: Create, delete, and organize .tex, .bib, .cls, and other files
- **Project Export**: Download entire projects as ZIP files

### 🤖 AI Integration
- **AI Assistant**: Built-in AI support with Ollama integration
- **Code Generation**: Generate LaTeX code from natural language prompts
- **Error Fixing**: Automatic error detection and correction suggestions
- **Code Improvement**: AI-powered code optimization and enhancement

### ⚡ Productivity Features
- **One-click Compilation**: Instant LaTeX compilation with detailed error reporting
- **Keyboard Shortcuts**: Ctrl+Enter to compile, Ctrl+S to save, and more
- **Error Handling**: Clear error messages with syntax highlighting
- **PDF Download**: Export compiled documents directly to your device

## Prerequisites

Before running the application, ensure you have the following installed:

### Required Software

- **Python 3.6+**
- **MiKTeX** (LaTeX distribution for Windows) or **TeX Live** (cross-platform)
  - Windows: Download from <https://miktex.org/download>
  - Linux/macOS: Install TeX Live from your package manager
  - Make sure `pdflatex` is accessible in your system PATH

### Optional: AI Features

- **Ollama** (for AI assistant functionality)
  - Download from: <https://ollama.ai/>
  - Run: `ollama pull codellama` or `ollama pull llama2` for AI features

### Required Python Packages

```bash
pip install flask pillow PyMuPDF werkzeug requests
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/latex-complier.git
cd latex-complier
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure LaTeX is installed and `pdflatex` is available in your system PATH

## Usage

### Starting the Application

1. Run the web application:

```bash
python main.py
```

2. **Access the Web Interface**: Open your browser and go to `http://localhost:5000`

### Using the Editor

3. **Create/Select Project**: Use the project dropdown to select an existing project or create a new one

4. **Write LaTeX Code**: Click on files in the file tree to edit them. The interface provides syntax highlighting and intelligent features

5. **Toggle Dark Mode**: Click the settings icon (⚙️) in the top-right corner to access the dark mode toggle

6. **Compile & Preview**: Click the "Recompile" button to compile your LaTeX code and see the PDF preview

7. **Download PDF**: Use the "Download PDF" button to save your compiled document

8. **AI Assistance**: Use the AI assistant panel for code generation, error fixing, and improvements (requires Ollama)

### Sample LaTeX Document

Here's a sample document to get started:

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\title{My First Document}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This is a sample LaTeX document.

\section{Content}
You can write your content here with \textbf{bold text}, \textit{italic text}, and even mathematical equations like $E=mc^2$.

\end{document}
```

3. **Compile & Preview**: Click the "Compile & Preview" button to compile your LaTeX code and see the PDF preview
4. **Save PDF**: Use the "Save PDF" button to export your compiled document

## Project Structure

```text
latex-complier/
├── main.py                 # Main Flask application
├── templates/
│   └── index.html         # Web interface with orange theme & dark mode
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── projects/              # User projects directory
│   └── [project-name]/    # Individual project folders
│       ├── main.tex       # Main LaTeX file
│       ├── *.tex          # Additional LaTeX files
│       ├── *.bib          # Bibliography files
│       └── *.cls/*.sty    # Style and class files
└── output/                # Compilation output directory
    ├── *.pdf              # Compiled PDF files
    ├── *.aux              # LaTeX auxiliary files
    └── *.log              # Compilation logs
```

## Configuration

### Theme Customization

The application features a modern orange color palette with dark mode support. Themes are automatically saved to browser localStorage and persist across sessions.

**Color Variables:**
- Light theme: Orange primary (#FF6B35), with complementary oranges
- Dark theme: Warmer orange (#FF7F50) optimized for dark backgrounds

### AI Assistant Setup

To enable AI features:

1. Install Ollama from <https://ollama.ai/>
2. Pull a compatible model:
   ```bash
   ollama pull codellama
   # or
   ollama pull llama2
   ```
3. Start the Ollama service
4. Restart the application - AI features will be automatically detected

### LaTeX Compiler Configuration

The application automatically detects common LaTeX installations. If needed, you can customize the compiler path in `main.py`:

```python
# Update the pdflatex command if needed
subprocess.run(['pdflatex', '-interaction=nonstopmode', f"{filename}.tex"])
```

## Troubleshooting

### Common Issues

1. **"Compilation failed" Error**
   - Check that your LaTeX syntax is correct
   - Ensure LaTeX (MiKTeX/TeX Live) is properly installed
   - Verify that `pdflatex` is accessible from the command line
   - Check the compilation log in the preview panel for detailed errors

2. **Preview Not Showing**
   - Ensure the document compiled successfully (check for error messages)
   - Verify that PyMuPDF is installed correctly: `pip install PyMuPDF`
   - Check that the PDF was generated in the output directory

3. **AI Assistant Not Working**
   - Install Ollama from <https://ollama.ai/>
   - Pull a compatible model: `ollama pull codellama`
   - Ensure the Ollama service is running
   - Check the AI status indicator in the sidebar

4. **Dark Mode Not Saving**
   - Enable cookies/localStorage in your browser
   - Clear browser cache and try again
   - Check browser console for JavaScript errors

5. **LaTeX Packages Missing**
   - On first use, MiKTeX will prompt to install missing packages
   - Allow automatic package installation in MiKTeX settings
   - For TeX Live, install the full distribution or use `tlmgr install <package>`

6. **Port 5000 Already in Use**
   - Change the port in `main.py`: `app.run(debug=True, port=5001)`
   - Or kill the process using port 5000

## Keyboard Shortcuts

- **Ctrl+S**: Save current file
- **Ctrl+Enter**: Compile LaTeX document
- **Ctrl+Space**: Trigger autocomplete (in editor)
- **Esc**: Close settings menu

## Dependencies

- **Flask**: Web framework for the backend
- **CodeMirror**: Syntax-highlighted editor (loaded via CDN)
- **Bootstrap**: UI framework for responsive design
- **Font Awesome**: Icons for the interface
- **PIL (Pillow)**: Image processing for PDF preview
- **PyMuPDF (fitz)**: PDF handling and rendering
- **Requests**: HTTP client for AI assistant integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [x] ~~Syntax highlighting for LaTeX code~~ ✅ **Implemented**
- [x] ~~Dark mode theme~~ ✅ **Implemented**
- [x] ~~Modern orange color palette~~ ✅ **Implemented**
- [x] ~~AI assistant integration~~ ✅ **Implemented**
- [x] ~~Multi-project support~~ ✅ **Implemented**
- [ ] Multiple document tabs within projects
- [ ] LaTeX template library and starter templates
- [ ] Export to different formats (Word, HTML, etc.)
- [ ] Integrated spell checking and grammar checking
- [ ] LaTeX package manager integration
- [ ] Real-time collaborative editing
- [ ] Git integration for version control
- [ ] Advanced search and replace across projects
- [ ] Custom themes and color schemes
- [ ] Plugin system for extensions

## Screenshots

![Main Interface - Light Mode](screenshots/light-mode.png)
*Modern orange-themed interface with project management*

![Main Interface - Dark Mode](screenshots/dark-mode.png)
*Dark mode with orange accents for comfortable nighttime editing*

![AI Assistant](screenshots/ai-assistant.png)
*Built-in AI assistant for code generation and help*

## Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify that LaTeX is accessible from the command line
4. Check the browser console for JavaScript errors
5. Create a new issue on GitHub with detailed information about your problem

## Deployment

### 🚀 Vercel Deployment (Recommended)

Vercel provides excellent support for Flask applications. Here's how to deploy your LaTeX Editor:

#### Prerequisites for Vercel
- Vercel account (free tier available)
- Git repository (GitHub, GitLab, or Bitbucket)

#### Step 1: Prepare for Vercel

1. **Create a `vercel.json` file** in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

2. **Update your `main.py`** to work with Vercel:

```python
# Add this at the end of main.py
if __name__ == "__main__":
    app.run(debug=False)  # Set debug=False for production

# For Vercel, also add:
# This allows Vercel to import the app
app = app
```

3. **Create `requirements.txt`** (if not exists):

```txt
Flask==2.3.3
Pillow==10.0.1
PyMuPDF==1.23.8
Werkzeug==2.3.7
requests==2.31.0
```

#### Step 2: Deploy to Vercel

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

**Option B: GitHub Integration (Recommended)**
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will automatically detect the Python app
6. Click "Deploy"

#### Step 3: Configure Environment Variables

In your Vercel dashboard:
1. Go to Project Settings → Environment Variables
2. Add any required environment variables
3. Redeploy if needed

#### Limitations on Vercel
- **LaTeX Compilation**: Vercel's serverless environment doesn't include LaTeX by default
- **File Storage**: Serverless functions have limited file system access
- **AI Features**: Ollama won't work on Vercel (serverless limitation)

**Recommended Workarounds:**
- Use a LaTeX compilation service (like LaTeX.Online API)
- Store user files in external storage (AWS S3, etc.)
- Use cloud-based AI services (OpenAI API) instead of local Ollama

### 🐳 Docker Deployment

For full functionality including LaTeX compilation:

1. **Create `Dockerfile`**:

```dockerfile
FROM python:3.9-slim

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

2. **Deploy to various platforms**:

```bash
# Build and run locally
docker build -t latex-editor .
docker run -p 5000:5000 latex-editor

# Deploy to Railway
railway up

# Deploy to Render
# (Connect your GitHub repo to Render)

# Deploy to DigitalOcean App Platform
# (Use their web interface or doctl CLI)
```

### ☁️ Alternative Deployment Platforms

#### Railway
- **Pros**: Supports Docker, persistent storage, databases
- **Setup**: Connect GitHub repo, Railway auto-detects Dockerfile
- **Cost**: Free tier with limitations, paid plans available

#### Render
- **Pros**: Easy Docker deployment, free tier, automatic SSL
- **Setup**: Connect GitHub, configure build settings
- **Dockerfile**: Required for LaTeX support

#### Heroku
- **Pros**: Mature platform, add-ons ecosystem
- **Setup**: Use buildpacks for Python + LaTeX
- **Note**: No longer has a free tier

#### DigitalOcean App Platform
- **Pros**: Full control, scalable, competitive pricing
- **Setup**: Deploy via GitHub or Docker registry

#### AWS/Azure/GCP
- **Pros**: Full enterprise features, highly scalable
- **Setup**: Use container services (ECS, Container Apps, Cloud Run)

### 🔧 Production Configuration

#### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
LATEX_PATH=/usr/bin/pdflatex
AI_SERVICE_URL=your-ai-service-endpoint
```

#### Security Considerations
- Set `debug=False` in production
- Use environment variables for sensitive data
- Implement proper authentication if needed
- Configure CORS for API endpoints
- Use HTTPS (most platforms provide this automatically)

#### Performance Optimization
- Use a production WSGI server (Gunicorn):
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
  ```
- Configure caching for static assets
- Optimize Docker image size
- Consider using a CDN for assets

### 📋 Deployment Checklist

- [ ] Test application locally
- [ ] Create production configuration
- [ ] Set up environment variables
- [ ] Configure database (if using one)
- [ ] Test LaTeX compilation in target environment
- [ ] Set up monitoring and logging
- [ ] Configure domain and SSL
- [ ] Test all features in production
- [ ] Set up backup strategy for user projects

### 🆘 Deployment Troubleshooting

**Common Issues:**

1. **LaTeX not found**
   - Ensure LaTeX is installed in the deployment environment
   - Check PATH configuration
   - Consider using a pre-built Docker image with LaTeX

2. **File permissions**
   - Ensure write permissions for output directory
   - Check user permissions in container

3. **Port configuration**
   - Use environment variable for port: `port = int(os.environ.get('PORT', 5000))`
   - Update `app.run(host='0.0.0.0', port=port)`

4. **Memory/timeout limits**
   - LaTeX compilation can be resource-intensive
   - Configure appropriate timeout and memory limits
   - Consider async compilation for large documents

---

**Note**: This application supports Windows, macOS, and Linux. While the instructions focus on Windows with MiKTeX, the application works with any LaTeX distribution that provides `pdflatex`. For other operating systems, install TeX Live and ensure `pdflatex` is in your system PATH.