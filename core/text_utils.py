# coding: utf-8
import string

DOMAINS = ['.ua', '.com', '.info', '.biz', '.net', '.in', '.co', '.all', '.name', '.su', '.ag', '.am',
           '.at', '.be', '.bz', '.de', '.uk', '.cc', '.fm', '.md', '.pl', '.se', '.jp', '.tk',
           '.tv', '.ms', '.tc', '.ws', '.kz', '.cz', '.ch', '.tj', '.cn', '.tw', '.es', '.eu', '.io',
           '.la', '.sc', '.sg', '.sh', '.vc', '.tm', '.nl', '.im', '.mobi', '.dk', '.pt', '.lv', '.it',
           '.fr', '.li', '.lt', '.sk', '.ro', '.asia', '.gr', '.hk', '.il', '.aero', '.me', '.travel', '.za',
           '.tel', '.kg', '.by', '.mx', '.nz', '.ae', '.si', '.cx', '.рф ', '.pro', '.kr', '.ru']


class Utils(object):

    @staticmethod
    def text_normalizer(text):
        text = text.lower().replace('\n', ' ').replace('\r', ' ')
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        text = text.translate(remove_punctuation_map).split()
        return ' '.join(text)

    @staticmethod
    def words_count(text, is_percent=False):
        words = text.split()
        if words:
            percent = 100.0 / len(words)
        else:
            percent = 0
        d = dict()
        for word in words:
            if word not in d:
                d[word] = 1
            else:
                d[word] += 1
        if is_percent:
            for word in d:
                d[word] = float(format((d[word] * percent), '.2f'))
        return d

    @staticmethod
    def top_in_dict(d, num):
        top = dict()
        values = sorted(d.values())[-num:]
        for key in d:
            if d[key] in values:
                top[key] = d[key]
        return top

    @staticmethod
    def distance(a, b):
        """Calculates the Levenshtein distance between a and b."""
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n+1)  # Keep current and previous row, not entire matrix
        for i in range(1, m+1):
            previous_row, current_row = current_row, [i]+[0]*n
            for j in range(1, n+1):
                add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
                if a[j-1] != b[i-1]:
                    change += 1
                current_row[j] = min(add, delete, change)
        return current_row[n]

    @staticmethod
    def top_in_text(text, num):
        text = Utils.text_normalizer(text)
        words = Utils.words_count(text, True)
        return Utils.top_in_dict(words, num)

    @staticmethod
    def get_max(l):
        max_l = 0
        item = ''
        for i in l:
            if not i:
                continue
            if len(i) > max_l:
                max_l = len(i)
                item = i
        return item

    @staticmethod
    def get_one(l):
        if type(l) is list:
            return Utils.get_max(l)
        if type(l) is str:
            return l
        if type(l) is None:
            return ''

    @staticmethod
    def delete_none(l):
        for num, item in enumerate(l):
            if not item:
                del l[num]
        return l

    @staticmethod
    def get_all(l, flag=False):
        if type(l) is list:
            new = u' '.join(Utils.delete_none(l))
            if flag:
                return Utils.text_normalizer(new)
            else:
                return u' '.join(new.lower().split())
        if type(l) is str:
            if flag:
                return Utils.text_normalizer(l)
            else:
                return u' '.join(l.lower().split())
        if type(l) is None:
            return ''

    @staticmethod
    def get_count(text, kw, root):
        # l = len(text)
        normal = Utils.text_normalizer(text)
        w = len(normal.split())
        uw = len(set(normal.split()))
        kw = normal.count(kw)
        kwr = {}
        for r in root:
            kwr[r] = normal.count(r)

        plt = {}
        for r in kwr:
            try:
                plt[r] = 100.0 * kwr[r] / w
            except:
                plt[r] = 0

        return w, kw, kwr, plt, uw


if __name__ == '__main__':
    text = '''Вам нужны клиенты? Чтобы добавить товары и услуги в каталог Prom.ua, зарегистрируйте свою компанию.
    Спасибо, но я покупатель. Товары и услуги — бизнес-каталог www.ua.all.biz компаний Украины,
    создание сайтов, товары и услуги,
    прайс-листы Вам нужны клиенты? Вам нужeн клиент?    чтооо  тоооо  Что вы будете делать с клиентами?'''
    k1 = Utils.text_normalizer(text)
    k2 = Utils.get_count(text, 'купить товар', ['куп', 'товар'])
    # k = Utils.top_in_text(text, 3)
    print(k1)
    print(k2)
