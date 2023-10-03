import sys
import requests
# Запросить json
# Отрисовать граф
# Grapgviz Online
# Глубина зависимостей более 2
def get_info(package):
    url=f"https://pypi.org/pypi/{package}/json"
    response = requests.get(url)
    data = response.json()
    first = data["info"]["requires_dist"]
    print(first)
    for i in range (len(first)):
        index = len(first[i]) - 1
        for j in range (len(first[i])):
            if (not (('a' <= first[i][j] <= 'z') or ('A' <= first[i][j] <= 'Z' )or (first[i][j] in ['-', '.']))):

                index = j
                break
        first[i] = first[i][:index]
    print(first)
    # data["info"]["requires_dist"]

def make_graph():
    pass

def main():
    print(sys.argv[1])
    get_info(sys.argv[1])
 

if __name__ == "__main__":
    main()
