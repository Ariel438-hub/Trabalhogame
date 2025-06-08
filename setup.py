import cx_Freeze
import os

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="assets/NinjaX.ico"
    )
]

include_arquivos = [("assets", "assets")]

cx_Freeze.setup(
    name="NinjaX",
    version="1.0",
    description="Um jogo de plataforma",
    options={
        "build_exe": {
            "packages": ["pygame", "os"],
            "includes": ["audioop", "aifc", "chunk", "speech_recognition","pyttsx3.drivers.sapi5"],
            "include_files": include_arquivos,
            "zip_include_packages": [],
            "zip_exclude_packages": ["pygame"]  # evita colocar seu jogo no .zip
        }
    },
    executables=executaveis
)