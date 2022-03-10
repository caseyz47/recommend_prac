import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ['SimHei']
plt.rcParams["axes.unicode_minus"] = False

def getRating(file_path):
    # rates = pd.read_table(
    #     file_path,
    #     # header=None,
    #     # sep="::",
    #     # names=["userID", "movieID", "rate", "timestamp"]
    #     index_col='userId'
    # )
    rates = pd.read_csv(
        file_path,
        # index_col= 'userId'
    )
    # print(rates)
    # print("range of user", min(rates['userId']),max(rates['userId']))
    # print("range of rate", min(rates['rating']), max(rates['rating']))
    # print("num of rate", rates.count())
    # print("top 5 items", rates.head(5))
    # print("user's min num of rate", rates['userId'].groupby(rates['userId']).count().min())
    # print("range of movie", min(rates['movieId'], max(rates['movieId'])))
    scores = rates['rating'].groupby(rates['rating']).count()
    # print(scores)

    for x,y in scores.items():
        plt.text(x,y+2,"%.0f"%y, ha='center', va='bottom', fontsize=12)

    plt.bar(scores.keys(), scores.values, fc='r', tick_label=scores.keys())
    plt.xlabel('grade')
    plt.ylabel('num of people')
    plt.title('statistic for rank')
    plt.show()


def getMovies(file_path):
    movies = pd.read_csv(
        file_path
    )
    print("movieId范围<{},{}>".format(min(movies['movieId']), max(movies['movieId'])))
    print("数据范围:{}".format(movies['movieId'].count()))
    moviesDict = dict()
    for line in movies['genres'].values:
        for one in line.split('|'):
            moviesDict.setdefault(one, 0)
            moviesDict[one] += 1
    print("电影类型总数{}".format(len(moviesDict)))
    print("电影类型：{}".format(moviesDict.keys()))
    print(moviesDict)

    # paint
    newMD = sorted(moviesDict.items(), key=lambda x:x[1], reverse=True)
    labels = [newMD[i][0] for i in range(len(newMD))]
    values = [newMD[i][1] for i in range(len(newMD))]
    explode = [x*0.01 for x in range(len(newMD))]
    plt.axes(aspect = 1)
    plt.pie(
        x=values,
        labels=labels,
        explode=explode,
        autopct="%3.1f %%",
        shadow=False,
        labeldistance=1.1,
        startangle=0,
        pctdistance=0.8,
        center=(-1,0),
    )
    plt.legend(loc=7,bbox_to_anchor=(1.3,1.0), ncol=3, fancybox=True,shadow=True, fontsize=6)
    plt.show()


def getUsers(file_path):
    users = pd.read_csv(file_path)
    # print(users)
    print("userId范围<{},{}>".format(min(users['userId'], max(users['userId']))))
    usersGender = users['gender'].groupby(users['gender']).count()
    plt.axes(aspect=1)
    plt.pie(x=usersGender.values,labels=usersGender.keys(), autopct="%3.1f%%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.show()

    # age info
    usersAge = users['age'].groupby(users['age']).count()
    plt.plot(usersAge.keys(), usersAge.values, label="user's age info",
             linewidth=3, color='r',marker='o',markerfacecolor='blue',
             markersize=12)
    for x,y in usersAge.items():
        plt.text(x,y+10,"%.0f"%y,ha='centet',va='bottom',fnotsize=12)
    plt.xlabel('user age')
    plt.ylabel('num for age rannge')
    plt.title('sum num')
    plt.show()




if __name__ == '__main__':
    getRating("./data/movielens/ratings.csv")
    # getMovies("./data/movielens/movies.csv")
    # getUsers('./data/movielens/')
