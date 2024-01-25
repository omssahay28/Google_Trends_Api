import pandas as pd
import sys
from helper import get_graph


def main():
    
    if len(sys.argv)!=2:
        print("Usage: python Script.py arg1")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    
    flag = False
    if (arg1=="True"):
        flag = True
    
    data = pd.read_csv("Sheet.csv")

    keyword = data['Keyword'].tolist()
    location = data['Location']

    # print(keyword)
    filename = 'output_data.csv'
    for q, l in zip(keyword, location):
        get_graph(q, l, filename, flag);
        
if __name__ == '__main__':
    main()