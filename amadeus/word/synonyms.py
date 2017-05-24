def is_synonyms(s1,s2):
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                return True
    return False
