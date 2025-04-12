import json
class Database:
    def register(self,name,email,password):
        with open('Data.json','r') as r:
            data=json.load(r)
            if email in data:
                return 0
            else:
                data[email]=[name,password]
        with open('Data.json','w') as w:
            json.dump(data,w)
            return 1
        
    def find(self,email,password):
        with open('Data.json','r') as rf:
            check=json.load(rf)
            if email in check:
                if check[email][1]==password:
                    return 1
                else:
                    return 0
            else:
                return 0
            
db=Database()
db.register('Shahir','Shahirmansuri3100@gmail.com','12345')