treba mat json,requirements, bs4(beautifull soup)

2 verzie async je pri 6 vstupoch 2.7x rychlejsia
dalo by sa to spravit aj cez class ale moc som tam nevidel vyuzitie
class by mohla byt aj na jednu ponuku aj na vsetky ponuky
teda v tej 2 by bolo pole s poziciami a nejake funkcie
class by bola napr

```
class Ponuka():
    def __init__(self,title,place,salary,contract_type,contact_email):
        self.ponuka={
        "title": title,
        "place": place,
        "salary": salary,
        "contract_type": contract_type,
        "contract_email": contact_email}

class Ponuky():
    def __init__(self):
        self.ponuky=[]
    def add(self,ponuka):
        self.ponuky.append(ponuka)
```
