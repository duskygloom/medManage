import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fmng

fpath = os.path.join("resources", "Josefin Sans", "static", "JosefinSans-Regular.ttf")
font = fmng.FontProperties(fname=fpath, size=15)

profit      = [10, 50, 0, 60, 30]
loss        = [5, 10, 20, 0, 40]
expenditure = [200, 300, 600, 1000, 100]
monthdat    = [1, 2, 3, 4, 5]
months = ["Jan", "Feb", "Mar", "Apr", "May"]

ydatasets   = [expenditure, profit, loss]

def createlinegraph():

    plt.plot(monthdat, profit, marker='o', color="skyblue", alpha=0.7, linewidth=3, markersize=5)
    # xaxis, yaxis, alpha = transparency
    plt.plot(monthdat, expenditure, marker='o', color="lime", alpha=0.7, linewidth=3, markersize=5)
    plt.plot(monthdat, loss, marker='o', color="red", alpha=0.7, linewidth=3, markersize=5)
    for data in ydatasets:
        for index in range(len(expenditure)):
            plt.annotate(f"{data[index]}", (index+1, data[index]))

    plt.xlabel("month", fontproperties=font)
    plt.ylabel("value", fontproperties=font)
    plt.title("FINANCE", fontproperties=font)
    plt.savefig("graph.svg")


def createbargraph():
    
    plt.bar(monthdat, expenditure, tick_label=months, color="red", width=0.8, align="edge")
    plt.bar(monthdat, profit, color="blue", width=0.6, align="edge")
    # xaxis, yaxis, alpha = transparency
    plt.bar(monthdat, loss, color="green", width=0.4, align="edge")

    x = 0.5
    for i in ydatasets:
        for j in range(len(i)):
            plt.annotate(str(i[j]), (j+1+x, i[j]))
        x -= 0.2

    plt.legend(["expenditure", "profit", "loss"])
    plt.xlabel("month", fontproperties=font)
    plt.ylabel("value", fontproperties=font)
    plt.title("FINANCE", fontproperties=font)
    plt.savefig("graph.svg")



def editimage(dark: bool):
    '''theme: dark / light'''
    if dark:
        bgcol = "#212121"
        fgcol = "#e9e9e9"
        cored = "#ff647d"
        coblu = "#00b0c7"
        cogrn = "#00c73f"
    else:
        bgcol = "#e9e9e9"
        fgcol = "#212121"
        cored = "#ff007b"
        coblu = "#00e1ff"
        cogrn = "#00ff50"
    with open("graph.svg", 'r') as rfile:
        content = rfile.read()
    content = content.replace("#000000", fgcol)
    content = content.replace("#ffffff", bgcol)
    content = content.replace("#ff0000", cored)
    content = content.replace("#00ff00", cogrn)
    content = content.replace("#0000ff", coblu)
    string = "*{stroke-linecap:butt;stroke-linejoin:round;"
    content = content.replace(string, string + f"fill:{fgcol}")
    with open("graph.svg", "w") as wfile:
        wfile.write(content)
    print("edited")

createbargraph()
editimage(False)


plt.show()



