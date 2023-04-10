#!/usr/bin/env python3.10

import os
import platform
import subprocess
from pathlib import Path
from fire import Fire

class NuitkaBuilder:
    def __init__(self, python: str = "python3.10"):
        self.python = python
        self.script_path = Path(__file__).resolve()
        self.app_dir = self.script_path.parent
        self.root_dir = self.app_dir.parent
        self.app_name = "MultInpainter"
        self.source_file = self.app_dir / "multinpainter.py"
        self.output_folder = self.app_dir / "dist_nuitka"
        self.output_folder.mkdir(exist_ok=True)
        self.venv_path = self.app_dir / "venv"
        self.venv_env = self.create_and_activate_virtualenv(self.venv_path)
        os.chdir(self.root_dir)
        self.install_dependencies()
        os.chdir(self.app_dir)
        self.build_application(self.source_file, self.output_folder)

    def create_and_activate_virtualenv(self, venv_path: Path):
        subprocess.run([self.python, "-m", "venv", venv_path], check=True)
        bin_folder = "Scripts" if platform.system() == "Windows" else "bin"
        return {
            "VIRTUAL_ENV": str(venv_path),
            "PATH": f"{venv_path / bin_folder}:{os.environ['PATH']}",
        }

    def install_dependencies(self):
        subprocess.run(
            [self.python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "setuptools_scm", "wheel", "urllib3"],
            check=True,
            env=self.venv_env,
        )
        subprocess.run([self.python, "-m", "pip", "install", "--upgrade", "nuitka"], check=True, env=self.venv_env)
        subprocess.run([self.python, "-m", "pip", "install", "--upgrade", "."], check=True, env=self.venv_env)

    def build_application(self, source_file: Path, output_folder: Path):
        nuitka_command = [
            self.python, "-m", "nuitka",
            "--assume-yes-for-downloads",
            "--standalone",
            "--onefile",
            "--enable-plugin=no-qt",
            "--follow-imports",
            "--lto=yes",
            f"--jobs={os.cpu_count()}",
            "--show-modules",
            "--nofollow-import-to=Crypto,dask,distributed,distutils,IPython,nuitka,numba,pytest,setuptools,setuptools_scm,snappy,test,tkinter,unittest",
            "--output-dir", str(output_folder),
            str(source_file),
        ]

        if platform.system() == "Darwin":
            nuitka_command.extend([
                "--clang",
                "--macos-disable-console",
                "--macos-create-app-bundle",
                "--macos-app-icon=../icons/multinpainter.icns",
            ])
        elif platform.system() == "Windows":
            nuitka_command.extend([
                "--windows-disable-console",
                "--windows-icon-from-ico=../icons/multinpainter.ico",
            ])

        subprocess.run(nuitka_command, check=True, env=self.venv_env)


if __name__ == "__main__":
    Fire(NuitkaBuilder)
