def CleanSoup(content):
    for tags in content.find_all():
        for val in list(tags.attrs):
            del tags.attrs[val]
    return content
