import serial #для работы с COM-портом
import numpy as np #для математики
import adi #для работы с Pluto SDR
import pyqtgraph as pg #построение графика

#параметры
CENTER_FREQ = 145_500_000 # центральная частота SDR, Гц
SAMPLE_RATE = 10_000_000 # частота дискретизации, Гц
BUF_SIZE = 65536 # размер буфера

F_MIN = 140.5 # нижняя граница графика, МГц
F_MAX = 150.5 # верхняя граница графика, МГц

COM_PORT = "COM6" # номер COM-порта Arduino
COM_BAUD = 9600 # скорость порта

sdr = adi.Pluto("usb:")
sdr.sample_rate = SAMPLE_RATE
sdr.rx_lo = CENTER_FREQ
sdr.rx_buffer_size = BUF_SIZE

ser = serial.Serial(COM_PORT, COM_BAUD, timeout=0)

x = 0
y = 0
z = 0
sh = 0
d = 0

def parse(line):
    global x, y, z, sh, d
    parts = line.split(",")
    if len(parts) >= 5:
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        sh = float(parts[3])
        d = float(parts[4])

app = pg.mkQApp()
win = pg.GraphicsLayoutWidget(show=True) # окно с графиком

plot = win.addPlot() # область графика
plot.setXRange(F_MIN, F_MAX, padding=0) # границы по X в МГц
curve = plot.plot() # кривая спектра

label = pg.LabelItem("") # текстовая панель
win.addItem(label, row=0, col=1) # размещаем справа от графика

while True:
    spec = np.fft.fftshift(np.fft.fft(sdr.rx()))
    curve.setData(20 * np.log10(np.abs(spec) + 1e-12)) # перевод сигнала в логарифмическую шкалу (дБ)

    while ser.in_waiting: # пока есть данные в COM-порту
        parse(ser.readline().decode("ascii", errors="ignore").strip())

    label.setText(f"x: {x} <br> y: {y} <br> z: {z} <br> широта: {sh} <br> долгота: {d}")

    pg.QtWidgets.QApplication.processEvents()