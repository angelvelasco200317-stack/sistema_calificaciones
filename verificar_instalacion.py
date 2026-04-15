#!/usr/bin/env python3
"""
Script para verificar la instalación completa del sistema.
"""

import os
import sys
import subprocess
import platform

def verificar_python():
    """Verificar versión de Python."""
    print("=" * 60)
    print("VERIFICANDO INSTALACIÓN DE PYTHON")
    print("=" * 60)
    
    version = sys.version
    print(f"Python {version}")
    
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print("✅ Versión de Python compatible")
    return True

def verificar_dependencias():
    """Verificar dependencias instaladas."""
    print("\n" + "=" * 60)
    print("VERIFICANDO DEPENDENCIAS")
    print("=" * 60)
    
    dependencias = [
        'Django',
        'djangorestframework',
        'django-cors-headers',
        'python-decouple',
        'xhtml2pdf',
        'reportlab',
        'Pillow'
    ]
    
    try:
        import pkg_resources
        for dep in dependencias:
            try:
                version = pkg_resources.get_distribution(dep).version
                print(f"✅ {dep:30} v{version}")
            except pkg_resources.DistributionNotFound:
                print(f"❌ {dep:30} NO INSTALADO")
                return False
    except ImportError:
        print("⚠️  No se puede verificar dependencias (pkg_resources no disponible)")
    
    return True

def verificar_estructura():
    """Verificar estructura de directorios."""
    print("\n" + "=" * 60)
    print("VERIFICANDO ESTRUCTURA DE DIRECTORIOS")
    print("=" * 60)
    
    estructura_esperada = [
        'SISTEMA_CALIFICACIONES/',
        'SISTEMA_CALIFICACIONES/backend/',
        'SISTEMA_CALIFICACIONES/gestion_calificaciones/',
        'SISTEMA_CALIFICACIONES/templates/',
        'SISTEMA_CALIFICACIONES/static/',
        'SISTEMA_CALIFICACIONES/venv/',
        'SISTEMA_CALIFICACIONES/.env',
        'SISTEMA_CALIFICACIONES/manage.py',
        'SISTEMA_CALIFICACIONES/requirements.txt'
    ]
    
    faltantes = []
    for dir_file in estructura_esperada:
        if not os.path.exists(dir_file.replace('/', os.sep)):
            faltantes.append(dir_file)
            print(f"❌ {dir_file}")
        else:
            print(f"✅ {dir_file}")
    
    if faltantes:
        print(f"\n⚠️  Faltan {len(faltantes)} elementos en la estructura")
        return False
    
    return True

def verificar_venv():
    """Verificar entorno virtual."""
    print("\n" + "=" * 60)
    print("VERIFICANDO ENTORNO VIRTUAL")
    print("=" * 60)
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Entorno virtual activado")
        
        # Verificar pip en venv
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Pip disponible: {result.stdout.split()[1]}")
            else:
                print("❌ Pip no disponible en el entorno virtual")
                return False
        except:
            print("❌ Error al verificar pip")
            return False
    else:
        print("⚠️  Entorno virtual NO activado")
        return False
    
    return True

def verificar_sistema_operativo():
    """Verificar sistema operativo."""
    print("\n" + "=" * 60)
    print("VERIFICANDO SISTEMA OPERATIVO")
    print("=" * 60)
    
    sistema = platform.system()
    version = platform.version()
    print(f"Sistema: {sistema}")
    print(f"Versión: {version}")
    
    if sistema == "Windows":
        print("✅ Sistema operativo compatible (Windows)")
    elif sistema == "Linux":
        print("✅ Sistema operativo compatible (Linux)")
    elif sistema == "Darwin":
        print("✅ Sistema operativo compatible (macOS)")
    else:
        print("⚠️  Sistema operativo no verificado completamente")
    
    return True

def verificar_puertos():
    """Verificar puertos disponibles."""
    print("\n" + "=" * 60)
    print("VERIFICANDO PUERTOS DISPONIBLES")
    print("=" * 60)
    
    puertos = [8000, 5432]  # Django y PostgreSQL
    
    import socket
    for puerto in puertos:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex(('localhost', puerto))
        sock.close()
        
        if resultado == 0:
            print(f"⚠️  Puerto {puerto} está en uso")
        else:
            print(f"✅ Puerto {puerto} disponible")
    
    return True

def main():
    """Función principal."""
    print("=" * 60)
    print("VERIFICACIÓN COMPLETA DEL SISTEMA INSTALADO")
    print("=" * 60)
    
    resultados = []
    
    resultados.append(("Python", verificar_python()))
    resultados.append(("Sistema Operativo", verificar_sistema_operativo()))
    resultados.append(("Entorno Virtual", verificar_venv()))
    resultados.append(("Dependencias", verificar_dependencias()))
    resultados.append(("Estructura", verificar_estructura()))
    resultados.append(("Puertos", verificar_puertos()))
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    exit_code = 0
    for nombre, resultado in resultados:
        status = "✅" if resultado else "❌"
        print(f"{status} {nombre}")
        if not resultado:
            exit_code = 1
    
    print(f"\n{'='*60}")
    if exit_code == 0:
        print("✅ VERIFICACIÓN COMPLETA EXITOSA")
    else:
        print("❌ VERIFICACIÓN CON ERRORES")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()