

class User:
    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear
        
    def get_name(self) -> str:
        up_name = self.name.upper()
        return up_name
    
    def age(self, current_year) -> int:
        years_old = current_year - self.birthyear
        return years_old
    
user = User(name="John", birthyear=1999)
print(user.age(2023))
print(user.get_name())


    
    