import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt


def grabWebWords(url, localPaths):  # 抓取网页，将单词存入word.txt文件
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
    except:
        print("从 " + url + "获取数据失败")
        return 0

    soup = BeautifulSoup(html, "html.parser")
    with open(localPaths, 'w+', encoding='utf-8') as file:
        for link in soup.find_all('a'):
            if link.string is not None:
                file.write(link.string + '\n')


def wordCount(localPath, wordCountPath):  # 统计单词出现的次数
    wordCountDict = {}
    with open(localPath, 'r', encoding='utf-8') as file:
        fileString = file.read()
        partten = re.compile(r"\b[a-z][a-z0-9]+|U\.S\.\b")
        fileString = fileString.lower()
        wordList = partten.findall(fileString)

    for word in wordList:
        if word in wordCountDict.keys():
            wordCountDict[word] = wordCountDict[word] + 1
        else:
            wordCountDict[word] = 1
    with open(wordCountPath, 'w+', encoding='utf-8') as file:
        for key, value in wordCountDict.items():
            file.write(key + " " + str(value) + '\n')


def statisticsVisual(wordCountPaths):  # 将统计后的结果可视化
    wordCountDictSum = {}
    for i in range(len(wordCountPaths)):
        with open(wordCountPaths[i], 'r', encoding='utf-8') as file:
            for line in file:
                words = line.replace('\n', '').split(' ')
                if words[0] in wordCountDictSum:
                    wordCountDictSum[words[0]] = wordCountDictSum[words[0]] + int(words[1])
                else:
                    wordCountDictSum[words[0]] = int(words[1])

    wordCountListSum = []
    for key, value in wordCountDictSum.items():
        wordCountListSum.append((key, value))

    wordCountSortListSum = sorted(wordCountListSum, key=lambda x: x[1], reverse=True)

    wordName = []
    wordNum = []

    for word in wordCountSortListSum[0:50]:
        wordName.append(word[0])
        wordNum.append(word[1])
    plt.figure(figsize=(60, 20))
    plt.bar(wordName, wordNum, width=0.5, label='wordCount')
    plt.xlabel('words')
    plt.ylabel('times')
    plt.legend()
    plt.show()


def main():
    urls = ["http://en.people.cn", "http://www.chinadaily.com.cn"]
    localPaths = ["D:/wordCount/people.txt", "D:/wordCount/chinadaily.txt"]
    wordCountPaths = ["D:/wordCount/peopleCount.txt", "D:/wordCount/chinadailyCount.txt"]
    for url, localtxt in zip(urls, localPaths):
        grabWebWords(url, localtxt)

    for localPath, wordCountPath in zip(localPaths, wordCountPaths):
        wordCount(localPath, wordCountPath)

    statisticsVisual(wordCountPaths)


main()
