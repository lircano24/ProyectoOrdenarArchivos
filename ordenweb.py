import os 
import shutil
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "file_organizer_secret_key"

# Definición de tipos de archivos y sus carpetas correspondientes
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".html", ".css", ".js", ".php", ".json"],
    "Others": []  # Archivos que no coinciden con ningún tipo
}

def organize_files(folder_path):
    """
    Organiza los archivos en subcarpetas según su tipo.
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # Detecta el tipo de archivo
            file_extension = os.path.splitext(file_name)[1].lower()
            folder_name = "Others"
            for key, extensions in FILE_TYPES.items():
                if file_extension in extensions:
                    folder_name = key
                    break
            
            # Crea la carpeta si no existe
            target_folder = os.path.join(folder_path, folder_name)
            os.makedirs(target_folder, exist_ok=True)
            
            # Mueve el archivo
            shutil.move(file_path, os.path.join(target_folder, file_name))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/organize", methods=["POST"])
def organize():
    folder_path = request.form.get("folder_path")
    if folder_path and os.path.exists(folder_path):
        organize_files(folder_path)
        flash(f"Archivos organizados en {folder_path}")
    else:
        flash("La carpeta seleccionada no es válida o no existe.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
