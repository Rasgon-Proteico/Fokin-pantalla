# test_minimo.py
from machine import Pin, I2C
import sh1106
import time

# Configuración básica
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

LED = Pin(2, Pin.OUT)  # Pin para el LED de estado
display = sh1106.SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)

for i in range(3):  # Parpadea el LED de estado 3 veces al inicio
    print()
    print("A ver si ya jalas")
    print()
    # Intenta inicializar la pantalla
    print()
    print("Pantalla inicializada.")

    # Limpia, escribe y muestra
    display.fill(0)
    display.text('Hola Mundo!', 10, 30, 1)
    display.show()
    print("'Hola Mundo!' enviado a la pantalla.")
    print()
    time.sleep(2)  # Espera 2 segundos
    display.fill(0)  # Limpia la pantalla
    display.show()
    time.sleep(1)  # Espera 1 segundo antes de reiniciar el bucle

