def findSubstring(s, words):
    """
    :type s: str
    :type words: List[str]
    :rtype: List[int]
    """
    end = len(words) - 1
    current = 0
    res = []

    found = s.find(''.join(words))

    if found:
        res.append(found)

    while current < end:
        current_word = words.pop(current)
        original_index = current
        words[0] = current_word

        for index in range(0, len(words) - 1):
            if index > len(words):
                break

            if index != 0:
                current_word = words.pop(index)

            words[index+1:index+1] = current_word

            position = s.find(''.join(words))

            if (position or position == 0) and position != -1:
                res.append(position)

        words[original_index:original_index] = current_word
        current += 1

    return res

findSubstring("barfoothefoobarman", ["foo", "bar"])