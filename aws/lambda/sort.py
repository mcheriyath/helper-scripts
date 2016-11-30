def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
            print(item)
    return result

a = ["asd","def","ase","dfg","asd","def","dfg"]
print getUniqueItems(a)
