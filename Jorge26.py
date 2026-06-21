import random
import os
import time

# --- CONFIGURACIÓN DE COLORES ANSI ---
C_CYAN = '\033[96m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_MAGENTA = '\033[95m'
C_BLUE = '\033[94m'
C_BLANCO = '\033[97m'
C_RESET = '\033[0m'

# Lista base de nombres (puedes añadir los que quieras)
NOMBRES_BASE = [
    "Jorge", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofia", 
    "Miguel", "Lucia", "Diego", "Carmen", "Andres", "Elena", "Raul",
    "Alejandro", "Maria", "Jose", "Santiago", "Daniela", "Fernando"
]
def generar_nombre_silabas():
    """Genera un nombre pronunciable uniendo consonantes y vocales al azar"""
    consonantes = "bcdfghjklmnprstvwxyz" # Sin la 'q' para evitar sonidos extraños
    vocales = "aeiou"
    
    # Decide al azar si el nombre tendrá 2, 3 o 4 sílabas (4 a 8 letras en total)
    cantidad_silabas = random.randint(2, 4) 
    
    nombre = ""
    for _ in range(cantidad_silabas):
        nombre += random.choice(consonantes)
        nombre += random.choice(vocales)
        
    return nombre

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def asegurar_txt(nombre):
    """Garantiza que el archivo termine siempre en .txt"""
    if not nombre.lower().endswith('.txt'):
        return f"{nombre}.txt"
    return nombre

def leer_archivo(ruta):
    """Lee un archivo y devuelve sus líneas limpias"""
    if not os.path.exists(ruta):
        print(f"{C_RED}[-] Error: El archivo '{ruta}' no existe.{C_RESET}")
        return None
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
        if not lineas:
            print(f"{C_RED}[-] Error: El archivo está vacío.{C_RESET}")
            return None
        return lineas
    except Exception as e:
        print(f"{C_RED}[-] Error al leer el archivo: {e}{C_RESET}")
        return None

def mostrar_progreso(iteracion, total, texto_item, color_barra, color_texto):
    """Muestra la barra de 0 a 100% con colores dinámicos"""
    porcentaje = (iteracion / total) * 100
    longitud_barra = 20
    bloques_llenos = int(longitud_barra * iteracion // total)
    barra = '█' * bloques_llenos + '-' * (longitud_barra - bloques_llenos)
    
    # \r hace que la línea se sobreescriba en terminales soportadas, pero como queremos ver la lista, usamos print normal
    print(f"{color_barra}[{barra}] {porcentaje:5.1f}%{C_RESET} | {color_texto}{texto_item}{C_RESET}")

def obtener_ruta_final(nombre_archivo):
    return os.path.abspath(nombre_archivo)

def mezclar_mayusculas_minusculas(palabra):
    """Toma una palabra y altera aleatoriamente sus letras a mayúscula o minúscula"""
    resultado = ""
    for letra in palabra:
        if random.choice([True, False]):
            resultado += letra.upper()
        else:
            resultado += letra.lower()
    return resultado

# --- OPCIONES DEL MENÚ ---

def opcion_1():
    print(f"\n{C_MAGENTA}--- 1. Generar Nombres Infinitos desde Cero ---{C_RESET}")
    nombre_input = input(f"{C_YELLOW}[?] Nombre del archivo a guardar (ej. lista): {C_RESET}").strip()
    archivo_salida = asegurar_txt(nombre_input)
    
    try:
        cantidad = int(input(f"{C_YELLOW}[?] ¿Cuántos nombres deseas generar?: {C_RESET}"))
    except ValueError:
        print(f"{C_RED}[-] Por favor, ingresa un número válido.{C_RESET}")
        return

    print(f"\n{C_CYAN}[+] Generando nombres infinitos (Generación Procedural)...{C_RESET}\n")
    time.sleep(0.5)
    
    generados = set()
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            while len(generados) < cantidad:
                # AQUÍ ESTÁ LA MAGIA: Fabricamos el nombre en lugar de leerlo de una lista
                base_inventada = generar_nombre_silabas()
                nombre_mezclado = mezclar_mayusculas_minusculas(base_inventada)
                
                # Verificamos que sea 100% único
                if nombre_mezclado not in generados:
                    generados.add(nombre_mezclado)
                    actual = len(generados)
                    
                    mostrar_progreso(actual, cantidad, nombre_mezclado, C_GREEN, C_CYAN)
                    f.write(nombre_mezclado + "\n")
                    
                    # Pequeña pausa visual solo si son pocos nombres
                    if cantidad <= 100: time.sleep(0.01)
                    
        ruta_absoluta = obtener_ruta_final(archivo_salida)
        print(f"\n{C_GREEN}[+] Proceso 100% finalizado.{C_RESET}")
        print(f"{C_BLUE}[*] Archivo guardado en:{C_RESET}\n    -> {C_BLANCO}{ruta_absoluta}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[-] Error al escribir el archivo: {e}{C_RESET}")
        
        
def opcion_2():
    print(f"\n{C_MAGENTA}--- 2. Enlazar Nombres (nombre:nombre) ---{C_RESET}")
    nombre_input = input(f"{C_YELLOW}[?] Nombre del archivo a guardar: {C_RESET}").strip()
    archivo_salida = asegurar_txt(nombre_input)
    
    ruta_origen = input(f"{C_YELLOW}[?] Ingresa la ruta/nombre del archivo .txt de origen: {C_RESET}").strip()
    nombres_txt = leer_archivo(ruta_origen)
    if not nombres_txt: return
    
    try:
        cantidad = int(input(f"{C_YELLOW}[?] ¿Cuántos combos deseas generar?: {C_RESET}"))
    except ValueError:
        print(f"{C_RED}[-] Por favor, ingresa un número válido.{C_RESET}")
        return

    print(f"\n{C_CYAN}[+] Enlazando combos...{C_RESET}\n")
    time.sleep(0.5)
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for i in range(cantidad):
                n1 = random.choice(nombres_txt).replace(" ", "")
                n2 = random.choice(nombres_txt).replace(" ", "")
                combo = f"{n1}:{n2}"
                
                mostrar_progreso(i + 1, cantidad, combo, C_YELLOW, C_MAGENTA)
                f.write(combo + "\n")
                if cantidad <= 100: time.sleep(0.01)
                
        ruta_absoluta = obtener_ruta_final(archivo_salida)
        print(f"\n{C_GREEN}[+] Proceso 100% finalizado.{C_RESET}")
        print(f"{C_BLUE}[*] Archivo guardado en:{C_RESET}\n    -> {C_BLANCO}{ruta_absoluta}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[-] Error al escribir el archivo: {e}{C_RESET}")

def opcion_3():
    print(f"\n{C_MAGENTA}--- 3. Enlazar Nombres Alfanuméricos ---{C_RESET}")
    nombre_input = input(f"{C_YELLOW}[?] Nombre del archivo a guardar: {C_RESET}").strip()
    archivo_salida = asegurar_txt(nombre_input)
    
    ruta_origen = input(f"{C_YELLOW}[?] Ingresa la ruta/nombre del archivo .txt de origen: {C_RESET}").strip()
    nombres_txt = leer_archivo(ruta_origen)
    if not nombres_txt: return
    
    try:
        cantidad = int(input(f"{C_YELLOW}[?] ¿Cuántos enlaces deseas generar?: {C_RESET}"))
    except ValueError:
        print(f"{C_RED}[-] Por favor, ingresa un número válido.{C_RESET}")
        return

    print(f"\n{C_CYAN}[+] Generando enlaces complejos...{C_RESET}\n")
    time.sleep(0.5)
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for i in range(cantidad):
                n1 = random.choice(nombres_txt).replace(" ", "")
                n2 = random.choice(nombres_txt).replace(" ", "")
                num1 = random.randint(10, 999)
                num2 = random.randint(10, 999)
                combo = f"{n1}{num1}:{n2.lower()}{num2}"
                
                mostrar_progreso(i + 1, cantidad, combo, C_CYAN, C_YELLOW)
                f.write(combo + "\n")
                if cantidad <= 100: time.sleep(0.01)
                
        ruta_absoluta = obtener_ruta_final(archivo_salida)
        print(f"\n{C_GREEN}[+] Proceso 100% finalizado.{C_RESET}")
        print(f"{C_BLUE}[*] Archivo guardado en:{C_RESET}\n    -> {C_BLANCO}{ruta_absoluta}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[-] Error al escribir el archivo: {e}{C_RESET}")

def opcion_4():
    print(f"\n{C_MAGENTA}--- 4. Eliminar Duplicados ---{C_RESET}")
    nombre_base = input(f"{C_YELLOW}[?] Nombre para el archivo: {C_RESET}").strip()
    
    if nombre_base.lower().endswith('.txt'):
        nombre_base = nombre_base[:-4]
    
    archivo_salida = f"{nombre_base}sinduplicas.txt"
    ruta_origen = input(f"{C_YELLOW}[?] Ingresa la ruta/nombre del archivo .txt de origen: {C_RESET}").strip()
    
    nombres_txt = leer_archivo(ruta_origen)
    if not nombres_txt: return
    
    total_original = len(nombres_txt)
    print(f"\n{C_CYAN}[+] Analizando y purgando duplicados...{C_RESET}")
    
    unicos = list(set(nombres_txt))
    unicos.sort() 
    total_final = len(unicos)
    eliminados = total_original - total_final
    
    print(f"{C_CYAN}[+] Guardando archivo limpio...{C_RESET}\n")
    time.sleep(0.5)
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for i, u in enumerate(unicos):
                mostrar_progreso(i + 1, total_final, f"Guardando: {u}", C_BLUE, C_BLANCO)
                f.write(u + "\n")
                
        ruta_absoluta = obtener_ruta_final(archivo_salida)
        print(f"\n{C_GREEN}========================================{C_RESET}")
        print(f"{C_GREEN}[+] Limpieza 100% finalizada.{C_RESET}")
        print(f"{C_YELLOW}[*] Nombres originales: {total_original}{C_RESET}")
        print(f"{C_RED}[*] Duplicados eliminados: {eliminados}{C_RESET}")
        print(f"{C_CYAN}[*] Nombres únicos guardados: {total_final}{C_RESET}")
        print(f"{C_BLUE}[*] Archivo guardado en:{C_RESET}\n    -> {C_BLANCO}{ruta_absoluta}{C_RESET}")
        print(f"{C_GREEN}========================================{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[-] Error al escribir el archivo: {e}{C_RESET}")

def main():
    while True:
        print(f"\n{C_CYAN}========================================{C_RESET}")
        print(f"{C_YELLOW}         GESTOR DE DATOS V4.0           {C_RESET}")
        print(f"{C_CYAN}========================================{C_RESET}")
        print(f"{C_GREEN} [1] Crear nombres únicos (Mayús/Minús){C_RESET}")
        print(f"{C_GREEN} [2] Crear combos (nombre:nombre){C_RESET}")
        print(f"{C_GREEN} [3] Crear combos alfanuméricos{C_RESET}")
        print(f"{C_GREEN} [4] Eliminar duplicados de un archivo{C_RESET}")
        print(f"{C_RED} [5] Salir del programa{C_RESET}")
        print(f"{C_CYAN}========================================{C_RESET}")
        
        opcion = input(f"{C_BLANCO} Selecciona una opción: {C_RESET}").strip()
        
        if opcion == '1': opcion_1()
        elif opcion == '2': opcion_2()
        elif opcion == '3': opcion_3()
        elif opcion == '4': opcion_4()
        elif opcion == '5':
            print(f"\n{C_GREEN}[+] Saliendo del programa. ¡Cualquier otra cosa, por aquí ando!{C_RESET}")
            break
        else:
            print(f"\n{C_RED}[-] Opción no válida. Intenta de nuevo.{C_RESET}")

if __name__ == "__main__":
    limpiar_pantalla()
    main()
