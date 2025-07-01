
from machine import Pin, I2C, PWM
import sh1106
import time

# --- Configuración de Pines y Constantes ---

# Configuración para la pantalla OLED (I2C)
SCL = 22
SDA = 21
I2C_ADDR = 0x3c   #? Dirección típica para pantallas OLED SH1106

# Configuración para el Servomotor (PWM)
SERVO = 2
FREC = 50


MIN_DUTY = 1638  #* Valor 0
MAX_DUTY = 8191  #* Valor 180


# --- Inicialización de Dispositivos ---
print()
print("Inicializando dispositivos...")

# 1. Inicializar I2C y la pantalla OLED
try:
    i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA))
    display = sh1106.SH1106_I2C(128, 64, i2c, addr=I2C_ADDR, rotate=180)
    display.fill(0)
    display.text('Pantalla OK!', 10, 30)
    display.show()
    print("- Pantalla OLED inicializada correctamente.")
    time.sleep(1)
except Exception as e:
    print(f"Error al inicializar la pantalla OLED: {e}")
    # Si la pantalla no funciona, el programa no continúa.
    # Podrías optar por continuar sin pantalla si lo prefieres.
    raise SystemExit("No se pudo conectar con la pantalla. Abortando.")


# 2. Inicializar el servomotor
servo = PWM(Pin(SERVO), freq=FREC)
print("- Servo en el 2.")
print("-" * 20)


# --- Funciones Auxiliares ---

def mover_servo(angulo):
    """
    Mueve el servo a un ángulo específico entre 0 y 180 grados.
    """
    if angulo < 0 or angulo > 180:
        print("El ángulo debe estar entre 0 y 180")
        return
    
    # Mapea el ángulo (0-180) al rango de duty (MIN_DUTY - MAX_DUTY)
    duty = int(MIN_DUTY + (MAX_DUTY - MIN_DUTY) * (angulo / 180.0))
    servo.duty_u16(duty)

def actualizar_pantalla(linea1, linea2):
    """
    Limpia la pantalla y muestra dos líneas de texto.
    """
    display.fill(0)
    display.text(linea1, 0, 15)  # Escribe en la parte superior
    display.text(linea2, 0, 35)  # Escribe en la parte inferior
    display.show()

# --- Bucle Principal ---

try:
    actualizar_pantalla("Iniciando...", "Ciclo de prueba")
    # Mover el servo a la posición inicial (90 grados) antes de empezar el bucle
    mover_servo(90)
    time.sleep(2)

    while True:
        # Mover a 0 grados
        angulo_actual = 0
        print(f"Moviendo a {angulo_actual} grados...")
        actualizar_pantalla("Servo  :) ", f"Pos: {angulo_actual} grados")
        mover_servo(angulo_actual)
        time.sleep(2)

        # Mover a 90 grados (posición central)
        angulo_actual = 90
        print(f"Moviendo a {angulo_actual} grados...")
        actualizar_pantalla("Servo  :) ", f"Pos: {angulo_actual} grados")
        mover_servo(angulo_actual)
        time.sleep(2)
        
        # Mover a 180 grados
        angulo_actual = 180
        print(f"Moviendo a {angulo_actual} grados...")
        actualizar_pantalla("Servo  :)", f"Pos: {angulo_actual} grados")
        mover_servo(angulo_actual)
        time.sleep(2)
        
        
        # Mover a 90 grados (posición central)
        angulo_actual = 90
        print(f"Moviendo a {angulo_actual} grados...")
        actualizar_pantalla("Servo  :) ", f"Pos: {angulo_actual} grados")
        mover_servo(angulo_actual)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
    
    
    # Mensaje de apagado en la pantalla
    actualizar_pantalla("Deteniendo...", " Vuelve pronto tonot@")
    time.sleep(1)
    actualizar_pantalla("Vuelve pronto tonot@", "eeee ")
    time.sleep(1)

    # Colocamos el servo en el centro antes de apagarlo
    mover_servo(90)
    time.sleep(1)
    
    # Detenemos la señal PWM para que el servo no haga ruido o consuma energía
    servo.deinit()
    
    # Limpiamos la pantalla y la apagamos (opcional pero buena práctica)
    display.fill(0)
    display.show()
    # display.poweroff() # Algunas librerías tienen esta función para apagarla por completo

    print("Recursos liberados. Programa finalizado.\n")
    print()
   