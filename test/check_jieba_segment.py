import jieba
from jieba.posseg import POSTokenizer

class MultiJieba:
    def __init__(self):
        self.jiebaInstances = {}
    def add_instance(self, name, term_list):
        tokenizer = jieba.Tokenizer()
        pos_tokenizer = POSTokenizer(tokenizer)

        for term in term_list:
            pos_tokenizer.add_word(term.replace(' ', '_'), 1, "term")

        self.jiebaInstances[name] = pos_tokenizer

    def cut(self, text, instance_name):
        if instance_name in self.jiebaInstances:
            words = self.jiebaInstances[instance_name].cut(text)
            return list(set([ item.word.replace('_', ' ') for item in words if item.flag == 'term' ]))
        else:
            raise ValueError(f"No jieba instance named {instance_name}")
# 使用示例
multi_jieba = MultiJieba()
multi_jieba.add_instance("dict1", ["Valkyrie’s Training Camp", "Memorial Arena", "Valkyrie Chronicles"])
multi_jieba.add_instance("dict2",  ["Schicksal Battle", "Final HOMU Fantasy", "Infinity Abyss"])
# 
text0 = "The new recruits were excited to start their first day at the Valkyrie’s Training Camp." 
text1 = "Thousands of fans gathered at the Memorial Arena to watch the championship match."
text2 = "I spent the whole weekend binge-watching the entire Valkyrie Chronicles anime series."
text3 = "The fate of the world hung in the balance as the heroes prepared for the final Schicksal Battle."
text4 = "Players were eagerly anticipating the release of Final HOMU Fantasy, the latest installment in the beloved game franchise."
text5 = "As they peered into the Infinity Abyss, the explorers felt a mix of awe and terror at its endless depths."


print(list(multi_jieba.cut(text0.replace(' ', '_'), "dict1"))) # 不通过， jieba无法支持复合词之间的一些符号
print(list(multi_jieba.cut(text1.replace(' ', '_'), "dict1"))) # 通过
print(list(multi_jieba.cut(text2.replace(' ', '_'), "dict1"))) # 通过

print(list(multi_jieba.cut(text3.replace(' ', '_'), "dict1"))) # 通过
print(list(multi_jieba.cut(text4.replace(' ', '_'), "dict1"))) # 通过
print(list(multi_jieba.cut(text5.replace(' ', '_'), "dict1"))) # 通过

print(list(multi_jieba.cut(text0.replace(' ', '_'), "dict2"))) # 通过 
print(list(multi_jieba.cut(text1.replace(' ', '_'), "dict2"))) # 通过
print(list(multi_jieba.cut(text2.replace(' ', '_'), "dict2"))) # 通过

print(list(multi_jieba.cut(text3.replace(' ', '_'), "dict2"))) # 通过
print(list(multi_jieba.cut(text4.replace(' ', '_'), "dict2"))) # 通过
print(list(multi_jieba.cut(text5.replace(' ', '_'), "dict2"))) # 通过