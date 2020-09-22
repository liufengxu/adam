class Yggdrasil(object):
    def __init__(self):
        self.name = ''
        self.code = ''
        self.parent = None
        self.children = []

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def add_child(self, ygg):
        self.children.append(ygg)
        ygg.set_parent(self)

    def gen_code(self):
        if not self.parent:
            self.set_code('O')
        start = 1
        for i in self.get_children():
            print(i.get_name())
            i.set_code(self.get_code()+'_'+str(start))
            i.gen_code()
            start += 1


root = Yggdrasil()
root.set_name('ROOT')
a = Yggdrasil()
a.set_name('A')
root.add_child(a)
b = Yggdrasil()
b.set_name('B')
root.add_child(b)

c = Yggdrasil()
c.set_name('C')
a.add_child(c)
d = Yggdrasil()
d.set_name('D')
a.add_child(d)

root.gen_code()
print(root.get_code())
print(a.get_code())
print(b.get_code())
print(c.get_code())
print(d.get_code())

