import marisa_trie
import string

def build_trie(terms):
    return marisa_trie.Trie(terms)

def mfm_segment_trie(text, trie):
    segment_chars = string.punctuation + string.whitespace

    words = []
    i = 0
    n = len(text)
    while i < n:
        # 使用 trie.prefixes 方法找到所有可能的前缀
        prefixes = trie.prefixes(text[i:])
        if prefixes:
            # 如果找到前缀，选择最长的一个
            longest_prefix = max(prefixes, key=len)
            if len(longest_prefix) == 0:
                i+= 1
                continue
            else:
                # 检查这个最大匹配的前后字符是否为分隔符，比如空格或者标点符号
                left_idx = i - 1
                right_idx = i + len(longest_prefix)
                if (left_idx < 0 or text[left_idx] in segment_chars) and (right_idx >= n or text[right_idx] in segment_chars):
                    words.append(longest_prefix)
                    i += len(longest_prefix)
                else:
                    i += 1
                    continue
        else:
            # 如果没有找到前缀，跳过当前字符
            i += 1
    return words

en_terms_1 = ["Valkyrie’s Training Camp", "Memorial Arena", "Valkyrie Chronicles", 'V', 'M']
en_terms_2 = ["Schicksal Battle", "Final HOMU Fantasy", "Infinity Abyss", 'V', 'M']

trie1 = build_trie(en_terms_1)
trie2 = build_trie(en_terms_2)

text0 = "The new recruits were excited to start their first day at the Valkyrie’s Training Camp." 
text1 = "Thousands of fans gathered at the Memorial Arena to watch the championship match."
text2 = "I spent the whole weekend binge-watching the entire Valkyrie Chronicles anime series."
text3 = "The fate of the world hung in the balance as the heroes prepared for the final Schicksal Battle."
text4 = "Players were eagerly anticipating the release of Final HOMU Fantasy, the latest installment in the beloved game franchise."
text5 = "As they peered into the Infinity Abyss, the explorers felt a mix of awe and terror at its endless depths."

term_list1 = mfm_segment_trie(text0, trie1)
print(term_list1)
term_list2 = mfm_segment_trie(text1, trie1)
print(term_list2)
term_list3 = mfm_segment_trie(text2, trie1)
print(term_list3)
term_list4 = mfm_segment_trie(text3, trie1)
print(term_list4)
term_list5 = mfm_segment_trie(text4, trie1)
print(term_list5)
term_list6 = mfm_segment_trie(text5, trie1)
print(term_list6)

term_list11 = mfm_segment_trie(text0, trie2)
print(term_list11)
term_list22 = mfm_segment_trie(text1, trie2)
print(term_list22)
term_list33 = mfm_segment_trie(text2, trie2)
print(term_list33)
term_list44 = mfm_segment_trie(text3, trie2)
print(term_list44)
term_list55 = mfm_segment_trie(text4, trie2)
print(term_list55)
term_list66 = mfm_segment_trie(text5, trie2)
print(term_list66)

text6 = "V As they peered into the Infinity Abyss, the explorers felt a mix of awe and Very terror at its endless depths."
text7 = "As they peered into the Infinity Abyss, the explorers felt a mix of awe and terror at its endless depths. M"

term_list77 = mfm_segment_trie(text6, trie2)
print(term_list77)
term_list88 = mfm_segment_trie(text7, trie2)
print(term_list88)