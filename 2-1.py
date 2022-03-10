# -*- coding:utf-8 -*-
import os
import json
import random
import math

class FirstRec:
    '''
    filePath: origin fielpath
    seed: random
    k: neighbor num
    nitems: num of recon movie

    '''
    def __init__(self, file_path, seed, k, n_items):
        self.seed = seed
        self.file_path = file_path
        self.k = k
        self.n_items = n_items
        self.users_1000 = self.__select_1000_users()
        self.train, self.test = self._load_and_split_data()


    def __select_1000_users(self):
        # print("randomly select 1000 users")
        if os.path.exists('data/Netflix/train.json')and os.path.exists('data/Netflix/test.json'):
            return list()
        else:
            users = set() # 去重每个电影下的评价用户
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path,file)
                # print("{}".format(one_path))
                with open(one_path, 'r') as fp:
                    for line in fp.readlines():
                        if line.strip().endswith(':'):
                            continue
                        userID, _, _ = line.split(',')
                        users.add(userID)
            users_1000 = random.sample(list(users), 1000)
            # print(users_1000)
            return users_1000

    def _load_and_split_data(self):
        train = dict()
        test = dict()
        if os.path.exists('./data/Netflix/test.json') and os.path.exists('data/Netflix/train.json'):
            test = json.load(open('data/Netflix/test.json'))
            train = json.load(open('data/Netflix/train.json'))
            print("从文件中加载数据集")
        else:
            random.seed(self.seed)
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print(one_path)
                with open(one_path, 'r') as fp:
                    movieID = fp.readline().split(':')[0]
                    for line in fp.readlines():
                        if line.strip().endswith(':'):
                            continue
                        userID,rate,_ = line.split(',')
                        if userID in self.users_1000:
                            if random.randint(1, 50) == 1:
                                test.setdefault(userID, {})[movieID] = int(rate)
                            else:
                                train.setdefault(userID, {})[movieID] = int(rate)
            print('加载数据到data/train.json data/test/json')
            json.dump(test, open('data/Netflix/test.json', 'w'))
            json.dump(train, open('data/Netflix/train.json', 'w'))
            print('load ok')
        return train, test

    def pearson(self, rating1, rating2):
        # rating1: {'movieid1':rate1, 'movieid2':rate2}
        i1, i2, i3, i4, i5, num = 0,0,0,0,0,0
        for key in rating1.keys():
            if key in rating2.keys():
                num += 1
                x = rating1[key]
                y = rating2[key]
                i1 += x*y
                i2 += x
                i3 += y
                i4 += x**2
                i5 += y**2
        if num==0:
            return 0
        denominator = math.sqrt(i4-math.pow(i2,2)/num)*math.sqrt(i5-math.pow(i3,2)/num)
        if denominator == 0:
            return 0
        else:
            return (i1-i2*i3/num)/denominator

    def recommend(self, userID):
        neighborUser = dict()
        for user in self.train.keys():
            if user != userID:
                distance = self.pearson(self.train[userID], self.train[user])
                neighborUser[user] = distance
        newNU = sorted(neighborUser.items(), key=lambda x:x[1], reverse= True)
        movies = dict()
        for user, dis in newNU[:self.k]:
            for movieID in self.train[user].keys():
                movies.setdefault(movieID, 0)
                movies[movieID] += dis*self.train[user][movieID]
        newMovies = sorted(movies.items(), key=lambda x:x[1], reverse=True)
        return newMovies

    def evaluate(self, num=30):
        precision = list()
        random.seed(10)
        for user in random.sample(self.test.keys(), num):
            hit = 0
            movies = self.recommend(user)[:self.n_items]
            for movie, rate in movies: # movie is a dict,return key-val
                if movie in self.test[user]:
                    hit += 1
            precision.append(hit/self.n_items)
        return sum(precision)/precision.__len__()


if '__main__' == __name__:
    file_path = "./data/Netflix/training_set"
    seed = 30
    k = 15
    n_items = 20
    f_rec = FirstRec(file_path, seed, k, n_items)
    r = f_rec.pearson(f_rec.train['1457974'], f_rec.train['2384044'])
    # print(r)
    result = f_rec.recommend('1457974')
    # print(result)
    print(f_rec.evaluate())