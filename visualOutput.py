import serial
import numpy as np
import adi
import pyqtgraph as pg

#параметры
CENTER_FREQ = 145_500_000
SAMPLE_RATE = 10_000_000
BUF_SIZE = 65536

F_MIN = 140.5
F_MAX = 150.5

COM_PORT = "COM6"
COM_BAUD = 9600

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
win = pg.GraphicsLayoutWidget(show=True)

plot = win.addPlot()
plot.setXRange(F_MIN, F_MAX, padding=0)
curve = plot.plot()

label = pg.LabelItem("")
win.addItem(label, row=0, col=1)

while True:
    spec = np.fft.fftshift(np.fft.fft(sdr.rx()))
    curve.setData(20 * np.log10(np.abs(spec) + 1e-12))

    while ser.in_waiting:
        parse(ser.readline().decode("ascii", errors="ignore").strip())

    label.setText(f"x: {x} <br> y: {y} <br> z: {z} <br> широта: {sh} <br> долгота: {d}")

    pg.QtWidgets.QApplication.processEvents()
