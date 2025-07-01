import time
from machine import Pin, I2C
# Importa la CLASE MPU6050 desde el ARCHIVO mpu6050.py
from mpu6050 import MPU6050 

# --- CONFIGURACIÓN DE I2C PARA ESP32 ---
# Asegúrate de que los pines son los correctos para tu conexión.
# Por defecto en muchos ESP32 son: SCL=22, SDA=21
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# --- INICIALIZACIÓN DEL SENSOR ---
# La dirección del MPU6050 suele ser 0x68
try:
    # Creamos una instancia de la clase MPU6050
    sensor = MPU6050(i2c)
    print("MPU6050 encontrado y listo!")
    
    # Opcional: Puedes configurar el rango del acelerómetro y giroscopio
    # Valores posibles para acelerómetro: 2, 4, 8, 16 (en g)
    # Valores posibles para giroscopio: 250, 500, 1000, 2000 (en grados/s)
    # sensor.set_accel_range(2) # Ejemplo: configurar a ±2g
    # sensor.set_gyro_range(250) # Ejemplo: configurar a ±250 deg/s

except Exception as e:
    print(f"MPU6050 no encontrado en el bus I2C. Revisa las conexiones. Error: {e}")
    # Detiene la ejecución si no se encuentra el sensor
    import sys
    sys.exit()


# --- BUCLE PRINCIPAL ---
while True:
    try:
        # 1. Leer la temperatura
        temperatura = sensor.read_temperature()

        # 2. Leer los datos del acelerómetro
        # g=True devuelve los valores en 'g' (fuerza de gravedad)
        # Es más intuitivo que los valores en m/s^2
        accel_data = sensor.read_accel(g=True)

        # 3. Leer los datos del giroscopio
        # Devuelve los valores en grados por segundo (deg/s)
        gyro_data = sensor.read_gyro()

        # Imprimimos los valores de forma ordenada
        print("========================================")
        print(f"Temperatura:    {temperatura:.2f} C")
        
        # El .3f formatea el número para mostrar 3 decimales
        print("--- Acelerómetro (g) ---")
        print(f"  X: {accel_data['x']:.3f} g")
        print(f"  Y: {accel_data['y']:.3f} g")
        print(f"  Z: {accel_data['z']:.3f} g")
        
        print("--- Giroscopio (deg/s) ---")
        print(f"  X: {gyro_data['x']:.3f} deg/s")
        print(f"  Y: {gyro_data['y']:.3f} deg/s")
        print(f"  Z: {gyro_data['z']:.3f} deg/s")
        
        # Esperamos un poco antes de la siguiente lectura
        time.sleep_ms(500) # 500 milisegundos = 0.5 segundos

    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        break
    except Exception as e:
        print(f"Ocurrió un error en el bucle: {e}")
        break