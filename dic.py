class M:
    def name(self):
        return "MClass()"
    
class E:
    def name(self):
        return "EClass()"
    
dic =  {M: M().name(), 
        E: E().name()}

for cls in dic:
    print(dic[cls])