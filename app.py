from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import subprocess
import tempfile
import base64
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
import shutil
import json
import requests
from datetime import datetime
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

class LatexCompilerWeb:
    def __init__(self):
        self.base_dir = "projects"
        self.output_dir = "output"
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.current_project = "default"
        self.pdflatex_path = r'C:\Users\psmsw\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
        self.bibtex_path = r'C:\Users\psmsw\AppData\Local\Programs\MiKTeX\miktex\bin\x64\bibtex.exe'
        self.ollama_url = "http://localhost:11434"  # Default Ollama URL
        
    def get_project_path(self, project_name=None):
        """Get the path for a specific project"""
        if project_name is None:
            project_name = self.current_project
        return os.path.join(self.base_dir, project_name)
    
    def create_project(self, project_name):
        """Create a new project directory"""
        project_path = self.get_project_path(project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # Create basic project structure
        os.makedirs(os.path.join(project_path, "figures"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "chapters"), exist_ok=True)
        
        # Create main.tex file
        main_tex = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage{cite}

\\title{""" + project_name.replace("_", " ").title() + """}
\\author{Your Name}
\\date{\\today}

\\begin{document}
\\maketitle

\\section{Introduction}
Welcome to your new LaTeX project! This is a sample citation \\cite{example2023}.

\\section{Related Work}
For more information, see the comprehensive study by \\cite{sample2024}.

\\bibliographystyle{plain}
\\bibliography{references}

\\end{document}"""
        
        with open(os.path.join(project_path, "main.tex"), 'w', encoding='utf-8') as f:
            f.write(main_tex)
            
        # Create references.bib file
        references_bib = """@article{example2023,
    title={Example Article},
    author={Author, First and Second, Author},
    journal={Journal Name},
    volume={1},
    number={1},
    pages={1--10},
    year={2023},
    publisher={Publisher}
}

@article{sample2024,
    title={Comprehensive Study on LaTeX},
    author={Smith, John and Doe, Jane},
    journal={Documentation Quarterly},
    volume={15},
    number={3},
    pages={45--67},
    year={2024},
    publisher={Academic Press}
}"""
        
        with open(os.path.join(project_path, "references.bib"), 'w', encoding='utf-8') as f:
            f.write(references_bib)
            
        return project_path
    
    def get_projects(self):
        """Get list of all projects"""
        if not os.path.exists(self.base_dir):
            return []
        return [d for d in os.listdir(self.base_dir) 
                if os.path.isdir(os.path.join(self.base_dir, d))]
    
    def get_project_files(self, project_name):
        """Get all files in a project"""
        project_path = self.get_project_path(project_name)
        if not os.path.exists(project_path):
            return []
        
        files = []
        for root, dirs, filenames in os.walk(project_path):
            for filename in filenames:
                if filename.endswith(('.tex', '.bib', '.cls', '.sty', '.txt', '.md')):
                    rel_path = os.path.relpath(os.path.join(root, filename), project_path)
                    files.append({
                        'name': filename,
                        'path': rel_path,
                        'full_path': os.path.join(root, filename),
                        'type': filename.split('.')[-1]
                    })
        return files
    
    def read_file(self, project_name, file_path):
        """Read a file from a project"""
        full_path = os.path.join(self.get_project_path(project_name), file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def save_file(self, project_name, file_path, content):
        """Save a file to a project"""
        full_path = os.path.join(self.get_project_path(project_name), file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def delete_file(self, project_name, file_path):
        """Delete a file from a project"""
        full_path = os.path.join(self.get_project_path(project_name), file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    
    def delete_project(self, project_name):
        """Delete an entire project directory"""
        if project_name == "default":
            return False  # Don't allow deletion of default project
        
        project_path = self.get_project_path(project_name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            return True
        return False
    
    def call_ollama(self, prompt, model="codellama"):
        """Call Ollama API for code assistance"""
        try:
            # First try to check if Ollama is running
            health_response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if health_response.status_code != 200:
                return None
                
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60  # Increased timeout for AI responses
            )
            if response.status_code == 200:
                return response.json().get('response', '')
            return None
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        except Exception as e:
            return None
    
    def get_available_models(self):
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model['name'] for model in models]
            return []
        except:
            return []

    def compile_latex(self, project_name, main_file="main.tex"):
        """Compile LaTeX code and return success status and PDF path"""
        project_path = self.get_project_path(project_name)
        tex_file = os.path.join(project_path, main_file)
        pdf_file = os.path.join(project_path, main_file.replace('.tex', '.pdf'))

        if not os.path.exists(tex_file):
            return False, None, f"File {main_file} not found in project {project_name}"

        try:
            # Run pdflatex first time
            result = subprocess.run(
                [self.pdflatex_path, '-interaction=nonstopmode', main_file],
                cwd=project_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Check if we have citations by looking for \cite commands in the tex file
            with open(tex_file, 'r', encoding='utf-8') as f:
                tex_content = f.read()
                has_citations = '\\cite{' in tex_content or '\\citep{' in tex_content or '\\citet{' in tex_content
            
            # Check if bibtex is needed by looking at aux file
            aux_file = os.path.join(project_path, main_file.replace('.tex', '.aux'))
            needs_bibtex = False
            
            if os.path.exists(aux_file):
                with open(aux_file, 'r', encoding='utf-8', errors='ignore') as f:
                    aux_content = f.read()
                    needs_bibtex = ('\\bibdata{' in aux_content or 
                                  '\\citation{' in aux_content or 
                                  has_citations)
            
            if needs_bibtex:
                # Run bibtex
                bibtex_result = subprocess.run(
                    [self.bibtex_path, main_file.replace('.tex', '')],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                
                # Run pdflatex again (twice for references to resolve properly)
                subprocess.run(
                    [self.pdflatex_path, '-interaction=nonstopmode', main_file],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                subprocess.run(
                    [self.pdflatex_path, '-interaction=nonstopmode', main_file],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
            
            return True, pdf_file, None
        except subprocess.CalledProcessError as e:
            # Read the log file for error details
            log_file = os.path.join(project_path, main_file.replace('.tex', '.log'))
            error_msg = "Compilation failed."
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()
                    # Extract relevant error information
                    lines = log_content.split('\n')
                    error_lines = [line for line in lines if 'Error' in line or '!' in line or 'undefined' in line.lower()]
                    if error_lines:
                        error_msg = '\n'.join(error_lines[:5])  # Show first 5 error lines
            return False, None, error_msg

    def generate_preview(self, pdf_path):
        """Generate base64 encoded preview image from PDF"""
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)  # Load first page
            
            # Create pixmap with higher resolution for better quality
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Convert to base64 for web display
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            doc.close()
            return img_base64
        except Exception as e:
            return None

# Initialize the compiler
compiler = LatexCompilerWeb()

@app.route('/')
def index():
    """Main page with project manager and LaTeX editor"""
    projects = compiler.get_projects()
    if not projects:
        # Create default project
        compiler.create_project("default")
        projects = ["default"]
    
    current_project = request.args.get('project', 'default')
    if current_project not in projects:
        current_project = projects[0]
    
    compiler.current_project = current_project
    
    # Get project files
    project_files = compiler.get_project_files(current_project)
    
    # Get current file content
    current_file = request.args.get('file', 'main.tex')
    file_content = compiler.read_file(current_project, current_file)
    
    return render_template('index.html', 
                         projects=projects,
                         current_project=current_project,
                         project_files=project_files,
                         current_file=current_file,
                         file_content=file_content)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get list of all projects"""
    return jsonify({'projects': compiler.get_projects()})

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    project_name = data.get('name', '').strip()
    
    if not project_name:
        return jsonify({'success': False, 'error': 'Project name is required'})
    
    # Sanitize project name
    project_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
    project_name = project_name.replace(' ', '_')
    
    try:
        compiler.create_project(project_name)
        return jsonify({'success': True, 'project': project_name})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    """Delete a project"""
    try:
        if compiler.delete_project(project_name):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Project not found or cannot be deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<project_name>/files', methods=['GET'])
def get_project_files(project_name):
    """Get files in a project"""
    files = compiler.get_project_files(project_name)
    return jsonify({'files': files})

@app.route('/api/projects/<project_name>/files/<path:file_path>', methods=['GET'])
def get_file_content(project_name, file_path):
    """Get content of a specific file"""
    content = compiler.read_file(project_name, file_path)
    return jsonify({'content': content})

@app.route('/api/projects/<project_name>/files/<path:file_path>', methods=['POST'])
def save_file_content(project_name, file_path):
    """Save content to a specific file"""
    data = request.get_json()
    content = data.get('content', '')
    
    try:
        compiler.save_file(project_name, file_path, content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<project_name>/files/<path:file_path>', methods=['DELETE'])
def delete_file(project_name, file_path):
    """Delete a file from project"""
    try:
        if compiler.delete_file(project_name, file_path):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<project_name>/files/new', methods=['POST'])
def create_new_file(project_name):
    """Create a new file in project"""
    data = request.get_json()
    file_path = data.get('path', '').strip()
    file_type = data.get('type', 'tex')
    
    if not file_path:
        return jsonify({'success': False, 'error': 'File path is required'})
    
    # Add extension if not present
    if not file_path.endswith(f'.{file_type}'):
        file_path += f'.{file_type}'
    
    # Create template content based on file type
    if file_type == 'tex':
        content = """\\documentclass{article}
\\usepackage[utf8]{inputenc}

\\begin{document}

\\end{document}"""
    elif file_type == 'bib':
        content = """@article{example,
    title={Example Article},
    author={Author, First},
    journal={Journal Name},
    year={2023}
}"""
    else:
        content = ""
    
    try:
        compiler.save_file(project_name, file_path, content)
        return jsonify({'success': True, 'file_path': file_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ollama/status', methods=['GET'])
def ollama_status():
    """Check if Ollama is running and get available models"""
    try:
        models = compiler.get_available_models()
        if models:
            return jsonify({
                'status': 'available',
                'models': models,
                'url': compiler.ollama_url
            })
        else:
            return jsonify({
                'status': 'unavailable',
                'error': 'Ollama service is not running or no models are installed',
                'url': compiler.ollama_url
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'url': compiler.ollama_url
        })

@app.route('/api/ollama/assist', methods=['POST'])
def ollama_assist():
    """Get AI assistance for LaTeX code"""
    data = request.get_json()
    code = data.get('code', '')
    request_type = data.get('type', 'improve')
    model = data.get('model', 'codellama')
    
    if not code.strip():
        return jsonify({'success': False, 'error': 'No code provided'})
    
    # Check if Ollama is available
    available_models = compiler.get_available_models()
    if not available_models:
        return jsonify({
            'success': False, 
            'error': 'Ollama service is not available. Please install and start Ollama, then pull a model like: ollama pull codellama'
        })
    
    # Use the first available model if specified model is not available
    if model not in available_models:
        model = available_models[0]
    
    # Create prompt based on request type
    if request_type == 'improve':
        prompt = f"""You are a LaTeX expert. Improve this LaTeX code by making it more readable, adding proper structure, and fixing any issues. Only return the improved LaTeX code without explanations:

{code}"""
    elif request_type == 'fix':
        prompt = f"""You are a LaTeX expert. Fix any syntax errors or issues in this LaTeX code. Only return the corrected LaTeX code without explanations:

{code}"""
    elif request_type == 'explain':
        prompt = f"""You are a LaTeX expert. Explain what this LaTeX code does in simple terms:

{code}"""
    elif request_type == 'generate':
        prompt = f"""You are a LaTeX expert. Generate LaTeX code for: {code}

Only return the LaTeX code without explanations."""
    else:
        return jsonify({'success': False, 'error': 'Invalid request type'})
    
    try:
        response = compiler.call_ollama(prompt, model)
        if response:
            return jsonify({
                'success': True, 
                'response': response.strip(),
                'model_used': model
            })
        else:
            return jsonify({
                'success': False, 
                'error': f'Failed to get response from model {model}. The model might be busy or not responding.'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error calling Ollama: {str(e)}'})

@app.route('/compile', methods=['POST'])
def compile_latex():
    """Compile LaTeX code and return preview"""
    data = request.get_json()
    project_name = data.get('project', 'default')
    file_path = data.get('file', 'main.tex')
    content = data.get('content', '')
    
    if not content.strip():
        return jsonify({'success': False, 'error': 'No LaTeX code provided'})
    
    try:
        # Save the current file content
        compiler.save_file(project_name, file_path, content)
        
        # Compile the project
        success, pdf_path, error_msg = compiler.compile_latex(project_name, file_path)
        
        if success:
            # Generate preview image
            preview_image = compiler.generate_preview(pdf_path)
            return jsonify({
                'success': True,
                'preview': preview_image,
                'message': 'Compilation successful!'
            })
        else:
            return jsonify({
                'success': False,
                'error': error_msg or 'Compilation failed'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<project_name>/<file_name>')
def download_pdf(project_name, file_name):
    """Download the compiled PDF"""
    pdf_file = os.path.join(compiler.get_project_path(project_name), file_name)
    
    if os.path.exists(pdf_file):
        return send_file(pdf_file, as_attachment=True, download_name=file_name)
    else:
        return jsonify({'error': 'PDF not found'}), 404

@app.route('/download/project/<project_name>')
def download_project(project_name):
    """Download entire project as ZIP"""
    project_path = compiler.get_project_path(project_name)
    
    if not os.path.exists(project_path):
        return jsonify({'error': 'Project not found'}), 404
    
    # Create ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_path)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return send_file(
        io.BytesIO(zip_buffer.read()),
        as_attachment=True,
        download_name=f"{project_name}.zip",
        mimetype='application/zip'
    )

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
