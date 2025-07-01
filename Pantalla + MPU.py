import time
from machine import Pin, I2C, PWM  # <-- 1. IMPORTAMOS PWM
import sh1106
from mpu6050 import MPU6050

# --- CONFIGURACIÓN DE PINES ---
SCL_PIN = 22
SDA_PIN = 21
SERVO_PIN = 2

# --- CONFIGURACIÓN DE DISPOSITIVOS ---
I2C_ADDR_MPU = 0x68 # Dirección típica del MPU6050
SERVO_FREQ = 50
MIN_DUTY = 1638  # Valor para 0 grados (ajustar si es necesario)
MID_DUTY = 4915  # Masomenos la micha
MAX_DUTY = 8191  # Valor para 180 grados (ajustar si es necesario)

# --- INICIALIZACIÓN DE I2C ---
# 2. Inicializamos el bus I2C una sola vez
print("Inicializando bus I2C...")
try:
    i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
    devices = i2c.scan()
    print("Dispositivos I2C encontrados:", [hex(device) for device in devices])
    if not devices:
        raise Exception("No se encontraron dispositivos I2C.")
except Exception as e:
    print(f"Error fatal al inicializar I2C: {e}")
    import sys
    sys.exit()

# --- INICIALIZACIÓN DE DISPOSITIVOS ---
print("\nInicializando dispositivos...")
display = None
sensor = None

try:
    # Inicializar pantalla OLED
    print("- Inicializando pantalla OLED...")
    # 3. Quitamos 'rotate' del constructor
    display = sh1106.SH1106_I2C(128, 64, i2c, addr=0x3c)
    # 3. Rotamos la pantalla con un método separado
    display.rotate(True) # True para rotar 180 grados
    display.fill(0)
    display.text('Pantallazo', 10,20)
    display.text('Azul', 30, 40)
    display.show()
    print("  Pantalla OLED inicializada.")
    time.sleep(1)

    # Inicializar sensor MPU6050
    print("- Inicializando sensor MPU6050...")
    sensor = MPU6050(i2c, addr=I2C_ADDR_MPU)
    print("  MPU6050 encontrado y listo!")

    # Inicializar Servomotor
    print("- Inicializando servomotor...")
    servo = PWM(Pin(SERVO_PIN), freq=SERVO_FREQ)
    print("  Servo listo en el pin 2.")

except Exception as e:
    print(f"ERROR DURANTE LA INICIALIZACIÓN: {e}")
    print("Revisa las conexiones y la dirección I2C de tus dispositivos.")
    import sys
    sys.exit()

print("-" * 20)

# --- FUNCIONES AUXILIARES ---
def mover_servo(angulo):
    """Mueve el servo a un ángulo específico (0-180)."""
    if not 0 <= angulo <= 180:
        print("El ángulo debe estar entre 0 y 180")
        return
    duty = int(MIN_DUTY + (MAX_DUTY - MIN_DUTY) * (angulo / 180.0))
    servo.duty_u16(duty)

def actualizar_pantalla(accel, gyro,):
    """Limpia y muestra todos los datos en la pantalla."""
    display.fill(0)
    # 4. MOSTRAMOS TODOS LOS DATOS A LA VEZ
    gx = int(gyro['x'])
    gy = int(gyro['y'])
    gz = int(gyro['z'])
    
    display.text(f"G: {gx},{gy},{gz}", 10, 0)   #coords x,y
    display.text("Acc:",40,15)
    display.text(f" X:{accel['x']:.2f}", 0, 28)#? "f" de function
    display.text(f" Y:{accel['y']:.2f}", 0, 41)
    display.text(f" Z:{accel['z']:.2f}", 0, 54)
    display.show()

# --- BUCLE PRINCIPAL ---
print("Iniciando bucle principal... (Presiona Ctrl+C para detener)")
# Posición inicial del servo
mover_servo(90)

while True:
    try:
        
        
        # Leer datos del acelerómetro (en 'g')
        accel_data = sensor.read_accel(g=True)

        # Leer datos del giroscopio (en deg/s)
        gyro_data = sensor.read_gyro()

        # Imprimir valores en la consola
        print(f"Accel X: {accel_data['x']:.2f}, Y: {accel_data['y']:.2f}, Z: {accel_data['z']:.2f} | "
              f"Gyro X: {gyro_data['x']:.1f}, Y: {gyro_data['y']:.1f}, Z: {gyro_data['z']:.1f}", end='\r')
        print()
        time.sleep(0.5)
        # Actualizar la pantalla OLED con todos los datos
        actualizar_pantalla(accel_data, gyro_data,)

        # Ejemplo de cómo usar el servo: moverlo según la inclinación en X
        # Mapea la aceleración en Y (de -1g a +1g) a un ángulo (0 a 180)
        # Limita el valor de -1 a 1 para evitar errores
        accel_y_limitado = max(-1.0, min(1.0, accel_data['y']))
        angulo_servo = 90 + (accel_y_limitado * -90) # -90 para invertir la dirección si es necesario
        mover_servo(angulo_servo)

        time.sleep_ms(100) # Un retardo más corto para una respuesta más fluida

    except KeyboardInterrupt:
        
        print("\n Babye :)")
        print()
        print("\nPrograma detenido por el usuario.")
        break
    except Exception as e:
        print(f"\nOcurrió un error en el bucle: {e}")
        break

# Al salir del bucle, apagar la pantalla y el servo
display.text("Se va a apagar esto",0,0)
time.sleep(1.5)
display.fill(0)
display.show()
print("\nDispositivos apagados. Babye :)")
print()