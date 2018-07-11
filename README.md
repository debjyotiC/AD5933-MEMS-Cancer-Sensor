# Classification of data read form MEMS cancer (Impedance) sensor by a Multi-Layer-Perceprton (MLP) Classifier 

This work studies the impedance verses frequency characteristics of a blood cell to detect the level of malignancy in it. The developed MEMS sensor is connected to Analog Device's AD5933 impedance analyzer, the AD5933 after performing a frequency sweep from 1kHz to 100kHz reports the impedance data (100 samples) back to an Arduino over the i2c bus. The impedance data so collected is then passed on to a MLP classifier to print out the degree of malignancy in a given sample of human blood. The MPL classifier used here is two layes deep and uses 100 input neurons. The MLP classifier is implemented on Python 2.7 using sklearn on a Raspberry Pi zero W running Raspbian Lite.   

## Getting Started

To get started copy the `ann_ad5933_serial_support.py`, `sensor_data_cancer_test.csv` and `sensor_data_cancer_train.csv` files to a desired folder. The Arduino must be kept conneted to the h/w UART of the Raspberry Pi zero W via a TTL level shifter (as the Pi and Arduino uses different TTl levels).

### Prerequisites

The support modules required to run the code are :
     
      1. NumPy --> For numerial calculations
      2. SciPy --> For scientific calculations  
      3. Pandas --> To prase the CSV files
      4. Sklearn --> To implement the neural network

### Installing

To install all the above dependencies have the latest version of "pip => 1.5.4" installed. (check: $pip -V):

      1. To install NumPy --> sudo pip install numpy
      2. To install SciPy --> sudo pip install scipy
      3. To install Pandas --> sudo pip install pandas
      4. To install Sklearn --> sudo pip install sklearn

## Running the tests

After uploading the `ad5833_arduino_code` to the Arduino, run the code `$python ann_ad5933_serial_support.py` with the Arduino connectedto the UART of the Raspberry Pi zero W. To check the serial communication port allocated to the Arduino type 
`$sudo dmesg | grep tty`, replace what ever tty value is printed out with the one in the code. After running the code, the program will read and store the impedance data obtained in `sensor_data_cancer_test.csv`.   

After training on the data from `sensor_data_cancer_train.csv` the prediction is done, the code returns the malignancy state (i.e. Cancerous or Normal) along with the predicted label (i.e. [1] or [0]). To furthur tune the network change the number of neurons in the hidden layers at `clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(50, 2), random_state=1)`


## Built With

* [Scikitlearn](http://scikit-learn.org/) - The Neural Network by sklearn 
* [Pandas](https://pandas.pydata.org/) - Python data management lib

## Authors

* **Debjyoti Chowdhury** - *Initial work* - [MyGithub](https://github.com/debjyotiC)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Dr. Madhurima Chattopadhyay** -*For the MEMS sensor and idea for the project* [LinkedIn](https://www.linkedin.com/in/dr-madhurima-chattopadhyay-1a62294a/)
