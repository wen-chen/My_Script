import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def Features_Cumulative_Frequency(X, y):
    X = pd.DataFrame(X)
    y = pd.DataFrame(y)
    df = pd.concat((y,X), axis=1)
    columns = ['y'] 
    for i in range(1,df.shape[1]):
        columns.append('x' + str(i))
    df.columns = columns

    for i in range(1,df.shape[1]):
        x = 'x' + str(i)
        sns.kdeplot(df[df.y==0][x], cumulative=True, label="y=0")
        sns.kdeplot(df[df.y==1][x], cumulative=True, label="y=1")
        plt.xlabel(x + ' features')
        plt.ylabel('Cumulative frequency')
        plt.show()