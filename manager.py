import sys
import requests

def check(data) -> bool :
    flag_not_found = False
    flag_no_info = False
    flag_no_data = False
    flag_not_found = ('message' in data.keys() and data['message'] == 'Not Found')
    if (not flag_not_found):
        flag_no_info = not ('info' in data.keys() and 'requires_dist' in data['info'].keys())
    if not (flag_not_found and flag_no_info):
        flag_no_data = (data['info']['requires_dist'] == None)
    return flag_not_found or flag_no_info or flag_no_data

def get_info(package) -> list:
    url=f"https://pypi.org/pypi/{package}/json"
    response = requests.get(url)
    data = response.json()
    if (check(data)):
        return None
    first = data["info"]["requires_dist"]
    
    for i in range (len(first)):
        index = len(first[i])
        for j in range (len(first[i])):
            if (not (('a' <= first[i][j] <= 'z') or ('A' <= first[i][j] <= 'Z' ) \
              or (first[i][j] in ['-', '.']) or (first[i][j].isnumeric()))):
                index = j
                break

        first[i] = first[i].replace('-', '_')
        first[i] = first[i].replace('.', '_')
        first[i] = first[i][:index]
    return first


def make_graph(list_dependecy) -> str:
    result = f"digraph {sys.argv[1]}" + '{\n'
    if (list_dependecy == None):
        return result + f'{sys.argv[1]}\n' + '}'

    for i in list_dependecy:
        result += f'{sys.argv[1]} -> {i}\n'
        second_level = get_info(i)
        if not(second_level is None):
            for j in range(len(second_level)):
                result += f'{i} -> {second_level[j]}\n'
   
    result += '}'
    return result

def main():
    print(make_graph(get_info(sys.argv[1])))
     

if __name__ == "__main__":
    main()
