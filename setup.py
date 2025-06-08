import cx_Freeze
import os

# Define o nome do seu script principal
executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="/assets/NinjaX.ico"
    )
]

cx_Freeze.setup(
    name="NinjaX",
    version="1.0",
    description="Um jogo de plataforma",
    options={
        "build_exe": {
            "packages": ["pygame", "os"],
            "include_files": [
                "base trabalho game/assets/",        
                "recursos/"       
            ]
        }
    },
    executables=executaveis
)
