import sys
import requests

def check_json(data) -> bool :
    flag_not_found = False
    flag_no_info = False
    flag_no_data = False
    flag_not_found = ('message' in data.keys() and data['message'] == 'Not Found')
    if (not flag_not_found):
        flag_no_info = not ('info' in data.keys() and 'requires_dist' in data['info'].keys())
    if not (flag_not_found and flag_no_info):
        flag_no_data = (data['info']['requires_dist'] == None)
    return flag_not_found or flag_no_info or flag_no_data

def check_liter(elem) -> bool :
    small = ('a' <= elem <= 'z')
    big = ('A' <= elem <= 'Z')
    is_num = elem.isnumeric()
    is_mark = (elem in ['-', '.'])
    return not (small or big or is_num or is_mark)

def get_info(package) -> list:
    url=f"https://pypi.org/pypi/{package}/json"
    response = requests.get(url)
    data = response.json()
    if (check_json(data)):
        return None
    dependence = data["info"]["requires_dist"]
    
    for i in range (len(dependence)):
        index = len(dependence[i])
        for j in range (len(dependence[i])):
            if (check_liter(dependence[i][j])):
                index = j
                break

        dependence[i] = dependence[i].replace('-', '_')
        dependence[i] = dependence[i].replace('.', '_')
        dependence[i] = dependence[i][:index]
    return dependence


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
