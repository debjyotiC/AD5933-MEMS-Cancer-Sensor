# import it all
from sklearn.neural_network import MLPClassifier  # import neural MLP classifier
import pandas as pd  # import pandas for CSV file
import serial  # to handle serial data to Arduino
import RPi.GPIO as GPIO
import os
from time import sleep  # for delay

portAddr = '/dev/ttyS0'  # Arduino communication port
baudRate = 9600  # Arduino comm. baud
impedance = []   # empty list to store impedance data

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)  #Red LED
GPIO.setup(13,GPIO.OUT)  #Green LED
GPIO.setup(15,GPIO.OUT)  #Blue LED

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.output(11,False)
GPIO.output(13,False)
GPIO.output(15,False)

df_train = pd.read_csv('sensor_data_cancer_train.csv') # open train CSV file
df_test = pd.read_csv('sensor_data_cancer_test.csv')   # open test CSV file

def serialRead(port, baud):
    ser = serial.Serial(port, baud)
    sleep(2)
    ser.write('C')
    sleep(2)
    for itr in xrange(100):
        dataRead = ser.readline()
        impedance.append(float(dataRead))
        GPIO.output(15,True)
    GPIO.output(15,False)

def writetoCSV(val):
    df_w = pd.DataFrame(val, columns=["datagot"])
    df_w.to_csv("sensor_data_cancer_test.csv", index=False)

def learnIt(df_train_samples, df_test_samples):
    # read the CSV file
    # import the column of data from the CSV file
    full_THP = df_train_samples['100%_THP'].tolist()
    full_PHA = df_train_samples['PHA(-)'].tolist()
    _50_THP = df_train_samples['50%_THP'].tolist()
    _60_THP = df_train_samples['60%_THP'].tolist()
    air = df_train_samples['Air'].tolist()
    water_data = df_train_samples['H2O'].tolist()

    # prepare the data and labels
    training_data = [full_THP, _50_THP, _60_THP, air, full_PHA, water_data]
    labels = [1, 1, 1, 0, 0, 0]
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(50, 2), random_state=1)
    clf.fit(training_data, labels)

    # prepare test data
    test_data = df_test_samples['datagot'].tolist()

    # predict test data label
    fit_it = clf.predict([test_data])

    # print 'Accuracy score:', clf.score(data, label, sample_weight=None) * 100, '%'

    # give nature based on predicted label
    print 'Nature:',
    if fit_it == [1]:
        print 'Cancerous', fit_it
        GPIO.output(11,True)       #glow Red LED if Cancerous
    elif fit_it == [0]:
        print 'Normal', fit_it
        GPIO.output(13,True)       #glow Green LED if not Cancerous
    sleep(10)
    GPIO.output(11,False)
    GPIO.output(13,False)

def action():
  flagit = False
  itr = 0
  while True:
    if GPIO.input(18) == GPIO.HIGH:
      sleep(0.2)
      serialRead(portAddr, baudRate)
      writetoCSV(impedance)
      sleep(1)
      learnIt(df_train, df_test)
    if GPIO.input(16) == GPIO.HIGH:
        flagit = True
        if flagit and itr == 5:
          print 'Shutting down'
          sleep(0.1)
          os.system('sudo shutdown now -h')
        itr = itr+1
        print 'count down', itr
        sleep(1)
    else:
      itr = 0
      flagit = False

def main():
  print '#####Ready####'
  action()

if __name__ == '__main__':
  main()
