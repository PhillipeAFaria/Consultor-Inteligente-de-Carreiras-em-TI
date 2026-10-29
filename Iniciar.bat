@echo off
setlocal
title Consultor de Carreiras em TI - Etapa 2
pushd "%~dp0"
if errorlevel 1 exit /b 1

set "SOMENTE_VERIFICAR=0"
if /I "%~1"=="--verificar" set "SOMENTE_VERIFICAR=1"
set "PYTHON_LOCAL=%CD%\.venv\Scripts\python.exe"

echo ================================================
echo   Consultor Avancado de Carreiras em TI
echo ================================================
echo.
if not exist "app.py" goto arquivos_ausentes
if not exist "requirements.txt" goto arquivos_ausentes
if exist "%PYTHON_LOCAL%" goto validar_python
if "%SOMENTE_VERIFICAR%"=="1" goto ambiente_ausente

echo Preparando o ambiente virtual da primeira execucao...
py -3.12 -c "import sys; raise SystemExit(sys.version_info.__lt__((3,10)))" >nul 2>nul
if not errorlevel 1 goto criar_py312
py -3 -c "import sys; raise SystemExit(sys.version_info.__lt__((3,10)))" >nul 2>nul
if not errorlevel 1 goto criar_py3
python -c "import sys; raise SystemExit(sys.version_info.__lt__((3,10)))" >nul 2>nul
if not errorlevel 1 goto criar_python
goto python_ausente

:criar_py312
py -3.12 -m venv ".venv"
if errorlevel 1 goto falha_ambiente
goto validar_python

:criar_py3
py -3 -m venv ".venv"
if errorlevel 1 goto falha_ambiente
goto validar_python

:criar_python
python -m venv ".venv"
if errorlevel 1 goto falha_ambiente

:validar_python
"%PYTHON_LOCAL%" -c "import sys; raise SystemExit(sys.version_info.__lt__((3,10)))" >nul 2>nul
if errorlevel 1 goto falha_ambiente
"%PYTHON_LOCAL%" -c "from importlib.metadata import version; from packaging.requirements import Requirement; from pathlib import Path; linhas=[l.strip() for l in Path('requirements.txt').read_text().splitlines() if l.strip() and not l.lstrip().startswith('#')]; raise SystemExit(not all(Requirement(l).specifier.contains(version(Requirement(l).name)) for l in linhas))" >nul 2>nul
if not errorlevel 1 goto pronto
if "%SOMENTE_VERIFICAR%"=="1" goto dependencias_ausentes

echo Instalando as dependencias no ambiente local...
echo A primeira instalacao precisa de acesso a internet.
"%PYTHON_LOCAL%" -m pip install -r "requirements.txt"
if errorlevel 1 goto falha_dependencias

:pronto
if "%SOMENTE_VERIFICAR%"=="1" goto verificado
echo Abrindo a aplicacao no navegador...
echo Mantenha esta janela aberta enquanto utilizar o sistema.
echo Para encerrar, pressione Ctrl+C e confirme, se solicitado.
echo.
"%PYTHON_LOCAL%" -m streamlit run "app.py" --server.address 127.0.0.1 --server.headless false
if errorlevel 1 goto falha_execucao
popd
exit /b 0

:verificado
echo VERIFICACAO OK: arquivos, Python e dependencias disponiveis.
popd
exit /b 0

:arquivos_ausentes
echo ERRO: mantenha Iniciar.bat na mesma pasta de app.py e requirements.txt.
goto erro
:ambiente_ausente
echo ERRO: ambiente .venv ainda nao foi criado. Execute Iniciar.bat sem argumentos.
goto erro
:python_ausente
echo ERRO: instale Python 3.10 ou superior. Recomendado: Python 3.12.
echo Instalador oficial: https://www.python.org/downloads/
echo Na instalacao, habilite a opcao de adicionar Python ao PATH.
goto erro
:falha_ambiente
echo ERRO: nao foi possivel criar ou utilizar o ambiente .venv.
echo Confira a instalacao do Python. Nenhum ambiente existente foi apagado.
goto erro
:dependencias_ausentes
echo ERRO: dependencias ausentes ou incompativeis. Execute sem --verificar para instalar.
goto erro
:falha_dependencias
echo ERRO: a instalacao das dependencias falhou. Confira a conexao e as mensagens acima.
goto erro
:falha_execucao
echo ERRO: o servidor nao iniciou ou foi interrompido. Confira as mensagens acima.
:erro
if "%SOMENTE_VERIFICAR%"=="0" pause
popd
exit /b 1
