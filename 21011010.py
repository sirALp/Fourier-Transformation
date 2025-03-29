import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QRadioButton, QPushButton, 
                             QButtonGroup, QGridLayout, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt

class SignalPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Signal Plotter')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        
        self.signal_inputs = []  # List to store inputs for each signal
        colors = ['blue', 'green', 'red']  # Colors for different signals
        
        for i in range(3):
            grid = QGridLayout()
            
            # Amplitude slider and label
            amp_label = QLabel(f'Amplitude {i+1}: 5')
            amp_label.setStyleSheet("font-size: 18px;")
            grid.addWidget(amp_label, 0, 0)
            amp_slider = QSlider(Qt.Horizontal, self)
            amp_slider.setRange(0, 100)
            amp_slider.setValue(50)
            amp_slider.valueChanged.connect(lambda value, lbl=amp_label, slider=amp_slider: self.update_label_and_slider(lbl, slider, value, 10.0))
            amp_slider.setStyleSheet(self.slider_style(amp_slider))
            grid.addWidget(amp_slider, 0, 1)
            
            # Frequency slider and label
            freq_label = QLabel(f'Frequency {i+1}: 5')
            freq_label.setStyleSheet("font-size: 18px;")
            grid.addWidget(freq_label, 1, 0)
            freq_slider = QSlider(Qt.Horizontal, self)
            freq_slider.setRange(0, 100)
            freq_slider.setValue(50)
            freq_slider.valueChanged.connect(lambda value, lbl=freq_label, slider=freq_slider: self.update_label_and_slider(lbl, slider, value, 10.0))
            freq_slider.setStyleSheet(self.slider_style(freq_slider))
            grid.addWidget(freq_slider, 1, 1)
            
            # Phase slider and label
            phase_label = QLabel(f'Phase {i+1}: 0')
            phase_label.setStyleSheet("font-size: 18px;")
            grid.addWidget(phase_label, 2, 0)
            phase_slider = QSlider(Qt.Horizontal, self)
            phase_slider.setRange(0, 360)
            phase_slider.setValue(0)
            phase_slider.valueChanged.connect(lambda value, lbl=phase_label, slider=phase_slider: self.update_label_and_slider(lbl, slider, value, 1.0))
            phase_slider.setStyleSheet(self.slider_style(phase_slider))
            grid.addWidget(phase_slider, 2, 1)
            
            # Sinus or Cosinus radio buttons
            signal_type_label = QLabel(f'Signal Type {i+1}:')
            signal_type_label.setStyleSheet("font-size: 18px;")
            grid.addWidget(signal_type_label, 3, 0)
            radio_sin = QRadioButton("Sinus")
            radio_cos = QRadioButton("Cosinus")
            radio_cos.setChecked(True)  # Default selection is Cosinus
            signal_type_group = QButtonGroup(self)
            signal_type_group.addButton(radio_sin)
            signal_type_group.addButton(radio_cos)
            
            hbox = QHBoxLayout()
            hbox.addWidget(radio_sin)
            hbox.addWidget(radio_cos)
            grid.addLayout(hbox, 3, 1)
            
            # Append the sliders and radio buttons for this signal to the list
            self.signal_inputs.append((amp_slider, freq_slider, phase_slider, signal_type_group, colors[i]))
            layout.addLayout(grid)
        
        # Fourier Series input fields
        fourier_grid = QGridLayout()
        
        a0_label = QLabel('a0:')
        a0_label.setStyleSheet("font-size: 18px;")
        fourier_grid.addWidget(a0_label, 0, 0)
        self.a0_input = QLineEdit(self)
        fourier_grid.addWidget(self.a0_input, 0, 1)
        
        ak_label = QLabel('a1, a2, a3 : ')
        ak_label.setStyleSheet("font-size: 18px;")
        fourier_grid.addWidget(ak_label, 1, 0)
        self.ak_input = QLineEdit(self)
        fourier_grid.addWidget(self.ak_input, 1, 1)
        
        bk_label = QLabel('b1, b2, b3 : ')
        bk_label.setStyleSheet("font-size: 18px;")
        fourier_grid.addWidget(bk_label, 2, 0)
        self.bk_input = QLineEdit(self)
        fourier_grid.addWidget(self.bk_input, 2, 1)
        
        # Option to choose between w0 and T
        self.param_select = QComboBox(self)
        self.param_select.addItem("w0")
        self.param_select.addItem("T")
        self.param_select.currentIndexChanged.connect(self.param_selection_changed)
        fourier_grid.addWidget(self.param_select, 3, 0)
        
        self.param_input = QLineEdit(self)
        fourier_grid.addWidget(self.param_input, 3, 1)
        
        layout.addLayout(fourier_grid)
        
        # Plot buttons
        self.plotButton1 = QPushButton('Plot Signals', self)
        self.plotButton1.clicked.connect(self.plot_signals)
        self.plotButton1.setStyleSheet("background-color: orange; font-size: 16px; padding: 10px;")
        layout.addWidget(self.plotButton1)

        self.plotButton2 = QPushButton('Plot Fourier Series', self)
        self.plotButton2.clicked.connect(self.plot_fourier_series)
        self.plotButton2.setStyleSheet("background-color: orange; font-size: 16px; padding: 10px;")
        layout.addWidget(self.plotButton2)

        self.setLayout(layout)
        self.setStyleSheet("background-color: white;")  # Set background color to white
    
    def update_label_and_slider(self, label, slider, value, scale):
        """Update the label text to show the current slider value, scaled as needed."""
        label.setText(f'{label.text().split(":")[0]}: {value / scale}')
        slider.setStyleSheet(self.slider_style(slider))  # Update slider style to reflect changes
    
    def slider_style(self, slider):
        """Return a stylesheet string for the slider, coloring the left part orange and the right part white."""
        value = slider.value()
        max_value = slider.maximum()
        percentage = value / max_value * 100
        return f"""
        QSlider::groove:horizontal {{
            height: 10px;
        }}
        QSlider::handle:horizontal {{
            background: white;
            border: 1px solid #5c5c5c;
            width: 20px;
            margin: -5px 0;
            border-radius: 10px;
        }}
        QSlider::sub-page:horizontal {{
            background: orange;
            border: 1px solid #777;
            height: 10px;
            border-radius: 2px;
            width: {percentage}%;
        }}
        QSlider::add-page:horizontal {{
            background: white;
            border: 1px solid #777;
            height: 10px;
            border-radius: 2px;
            width: {100 - percentage}%;
        }}
        """

    def param_selection_changed(self):
        """Handle changes in the parameter selection (w0 or T)."""
        selected_param = self.param_select.currentText()
        self.param_input.setPlaceholderText(f"Enter value for {selected_param}")
    
    def plot_signals(self):
        """Generate and plot the signals based on the user inputs."""
        try:
            t = np.linspace(0, 1, 500)
            fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
            
            synthesized_signal = np.zeros_like(t)  # Initialize synthesized signal
            
            for i, (amp_slider, freq_slider, phase_slider, signal_type_group, color) in enumerate(self.signal_inputs):
                amplitude = amp_slider.value() / 10.0
                frequency = freq_slider.value() / 10.0
                phase = phase_slider.value()
                signal_type = "cosine" if signal_type_group.buttons()[1].isChecked() else "sine"
                
                if signal_type == "cosine":
                    signal = amplitude * np.cos(2 * np.pi * frequency * t + np.radians(phase))
                else:
                    signal = amplitude * np.sin(2 * np.pi * frequency * t + np.radians(phase))
                
                axs[i].plot(t, signal, label=f'Signal {i+1}', color=color)
                axs[i].legend(loc='upper right')
                axs[i].grid(True)
                
                synthesized_signal += signal  # Sum the signals
            
            axs[3].plot(t, synthesized_signal, label='Synthesized Signal', color='black')
            axs[3].legend(loc='upper right')
            axs[3].grid(True)
            
            plt.xlabel('Time [s]')
            plt.show()
        except Exception as e:
            print(f"An error occurred: {e}")

    def plot_fourier_series(self):
        """Generate and plot the Fourier series based on the user inputs."""
        try:
            a0 = float(self.a0_input.text())
            ak = [float(k) for k in self.ak_input.text().split(',')]
            bk = [float(k) for k in self.bk_input.text().split(',')]
            selected_param = self.param_select.currentText()
            param_value = float(self.param_input.text())
            
            t = np.linspace(0, 20, 2000)
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if selected_param == 'w0':
                w0 = param_value
                T = 2 * np.pi / w0
            else:
                T = param_value
                w0 = 2 * np.pi / T
            
            fourier_series = a0 / 2 * np.ones_like(t)
            
            for k in range(1, 4):
                fourier_series += ak[k-1] * np.cos(k * w0 * t) + bk[k-1] * np.sin(k * w0 * t)
            
            ax.plot(t, fourier_series, label='Fourier Series', color='purple')
            ax.legend(loc='upper right')
            ax.grid(True)
            
            plt.xlabel('Time [s]')
            plt.show()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignalPlotter()
    ex.show()
    sys.exit(app.exec_())
