# import it all
from sklearn.neural_network import MLPClassifier  # import neural MLP classifier
import pandas as pd  # import pandas for CSV file
import serial  # to handel serial data to Arduino
from time import sleep  # for delay


portAddr = '/dev/ttyS0'  # Arduino communication port
#portAddr = 'COM5'
baudRate = 9600  # Arduino comm. baud
impedance = []   # empty list to store impedance data

df_train = pd.read_csv('sensor_data_cancer_train.csv') # open train CSV file
df_test = pd.read_csv('sensor_data_cancer_test.csv')   # open test CSV file

def serialRead(port, baud):
    ser = serial.Serial(port, baud, timeout = 3.0)
    sleep(2)
    ser.write('C')
    sleep(2)
    for itr in xrange(100):
        dataRead = ser.readline()
        impedance.append(float(dataRead.split('\n\r')))
    ser.close()

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
    elif fit_it == [0]:
        print 'Normal', fit_it


def main():
    serialRead(portAddr, baudRate)
    writetoCSV(impedance)
    sleep(3)
    learnIt(df_train, df_test)


if __name__ == '__main__':
    main()
