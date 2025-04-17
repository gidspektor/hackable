def findSubstring(s, words):
    """
    :type s: str
    :type words: List[str]
    :rtype: List[int]
    """
    current = 0
    res = []

    while current < len(words) - 1:
        current_word = words.pop(current) if current != 0 else words[0]
        words[0] = current_word

        for index in range(0, len(words)):
            if index > len(words):
                break

            if index != 0:
                current_word = words.pop(index - 1)
                words[index:index] = [current_word]

            position = s.find(''.join(words))

            if (position or position == 0) and position != -1:
                res.append(position)
        print(words)
        current += 1

    return res

print(findSubstring("barfoofoobarthefoobarman", ["bar","foo","the"]))