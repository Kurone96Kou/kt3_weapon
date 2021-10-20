
from dataclasses import dataclass
from random import randint, uniform
from requests import get


class ErrorNotWeapon(Exception): #исключение
    def __init__(self, roles, message="Мир еще не придумал такое оружие"):
        self.roles = roles
        self.message = message

    def __str__(self): #преобразование объекта к строковому представлению, вызывается, когда объект передается функциям print() и str()
        return f'{self.roles} -> {self.message}'

@dataclass
class Weapons():#оружие
    rarity: int #редкость
    dropchance: float #шанс выпадения

    @property #свойства
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if len(name) > 0:
            self.__name = name
        else:
            raise ValueError("Назови свое оружие!")

    def __str__(self): #преобразование объекта к строковому представлению, вызывается, когда объект передается функциям print() и str()
        return f'○Получено:Оружие "{self.name}" редкость {self.rarity}★, шанс выпадения: {self.dropchance}%'


    def __add__(self, other): #метод перегрузки оператора сложения, вызывается, когда объект участвует в операции сложения будучи операндом с левой стороны
        if issubclass(type(other), Weapons):
            t = Weapons((self.rarity + other.rarity) / 2, round(self.dropchance + other.dropchance)/10) #немного корретируем рарность и дроп
            t.name = f"{self.name} {other.name}"
            return t
        elif isinstance(other, int) or isinstance(other, float):
            self.dropchance += other
            return self
        else:
            raise TypeError(f"Тебе запрещается складывать {self.__class__} с {type(other)}. За такую черную магию могут изгнать")

    def __sub__(self, other): #метод перегрузки вычитания
        if isinstance(other, int) or isinstance(other, float):
            self.dropchance -= other
            return self
        else:
            raise TypeError(f"Тебе запрещается вычитать {self.__class__} из {type(other)}. За такую черную магию могут изгнать")

    def __mul__(self, other): #метод перегрузки умножения
        if isinstance(other, int) or isinstance(other, float):
            self.dropchance *= other
            return self
        else:
            raise TypeError(f"Тебе запрещается умножать {self.__class__} с {type(other)}. За такую черную магию могут изгнать")

    def __truediv__(self, other): #метод перегрузки деления
        if isinstance(other, int) or isinstance(other, float):
            return self.dropchance * other
        else:
            raise TypeError(f"Тебе запрещается делить {self.__class__} на {type(other)}. За такую черную магию могут изгнать")

@dataclass
class Element(Weapons):
    fire: bool
    ice: bool
    description: str

    def Weapon_Element(self):
        if self.fire and self.ice:
            str = 'Паровой'
        elif self.fire:
            str = 'Огненный'
        elif self.ice:
            str = 'Ледяной'
        else:
            str = 'Другой тип магии'

        return str

    def __str__(self):
        return f'○Получено:{self.Weapon_Element()} оружие "{self.name}" - редкость {self.rarity}★, шанс выпадения: "{self.dropchance}"%'


class TypeWeapon(Element):
    TYPES = ['Катализатор', 'Дрековое', 'Клеймор', 'Одноручное', 'Лук']
    RANGS = ['Королевский', 'Бандитский', 'Демонический', 'Ангельский']
    MATERIALS = ['Березовый', 'Сосновый', 'Серебряный', 'Золотой', 'Платиновый', 'Божественный']

    @staticmethod
    def getRangs():
        return TypeWeapon.RANGS


    def _find(f, a): #исключение дублирования кода для поиска type и rang при создании объекта класса TypeWeapon, что позволяет исключить возможность создания неизвестного объекта
        f = str(f).lower()
        for x in a:
            if str(x).lower() == f:
                return x

        return False

    #Метод __init__ выполняется после того как Python создал новый экземпляр и, при этом, методу __init__ передаются аргументы с которыми был создан экземпляр
    def __init__(self, name, t, dropchance, fire, ice, description, material='Сучковый', type='Палка', rang='Простой'):
        #обращение к род.классу без создания нового экземпляра
        super().__init__(t, dropchance, fire, ice, description)
        self.name = name
        self.material = material

        self.type = TypeWeapon._find(type, TypeWeapon.TYPES)
        if self.type is False:
            raise ErrorNotWeapon(type) #вызов созданного исключения

        self.rang = TypeWeapon._find(rang, TypeWeapon.getRangs())
        if self.rang is False:
            raise Exception("В этом мире не существует такой группировки, что тебе об этом известно?")

    def __str__(self):
        return f'○Получено:  {self.rang} {self.material} {self.type} "{self.name}" - {self.Weapon_Element().lower()} элемент. Редкость: {self.rarity}★, шанс выпадения:  {self.dropchance}%. Описание: "{self.description}"'

    def __eq__(self, other): #метод ерегрущки сравнения
        #сравниваем матерал и ранг, чтобы оружку можно было влить
        return  self.material == other.material and self.rang == other.rang and issubclass(type(other), Weapons)

def weaponGENERTION() -> TypeWeapon: #генерируем случайное оржие
    weapon_names = ("Ancor",)
    try:
        weapon_names = get(r"https://raw.githubusercontent.com/solvenium/"
                         r"names-dataset/master/dataset/Female_given_names.txt").text.split()
        if len(weapon_names) + len(weapon_names) < 2:
            raise Exception("Твое оружие не может быть безымянным")
    except Exception as e:
        print(f"Ошибка внешнего мира. Боги передают следующее послание:\n{e}")

    description = ['можно найти на улице', 'нужно победить босса', 'находится в сундуке', 'можешь его скрафтить сам']

    while True:
        names = weapon_names
        rang = TypeWeapon.RANGS[randint(0, len(TypeWeapon.RANGS) - 1)]
        type = TypeWeapon.TYPES[randint(0, len(TypeWeapon.TYPES) - 1)]
        material = TypeWeapon.MATERIALS[randint(0, len(TypeWeapon.MATERIALS) - 1)]
        name = names[randint(0, len(names) - 1)]


        r = round(uniform(1,5))
        dc = round(uniform(0.1,99),2)
        fire_true= round(uniform(0,1))
        ice_true = round(uniform(0, 1))
        des_index=round(uniform(0,3))


        yield TypeWeapon(name, r, round(dc,2), fire_true, ice_true, description[des_index], material, type, rang)

def main():
    print("Привет, путник. У тебя нет оружия? Зачем, ты спрашиваешь? Какое приключение без него? В любом случае, в углу стоит подарок для тебя.")
    sword = Weapons(2, 34.56)
    sword.name = "Меч"
    print(sword)
    print("Так держать. Дальше тебе нужно изучить элементы. Каждое оружие имеет каплю огня или льда. Или все вместе. А может и не иметь. Что делать? Выйди на улицу, там начался дождь")
    el = Element(4, 14.74, True, False, "только во время дождя")
    el.name = "Электрический"
    el *= 1.3
    print(f"Если во время дождя началась гроза, то шанс статуса 'Электрический' становится {round(el.dropchance),2} %")

    #пробуем сложить созданные объекты
    print(f"Если вознести {sword.name} к небу во время дождя, то получится: {el + sword}")

    print("Отлично. Вот твое первое поручение: отправляйся в клетку Феникса. Да, это смертельное задание, но меня это не волнует")

    weap = TypeWeapon("Fenix", 5, 0.3, True, False, "Победить Феникса", "Золотой", "Катализатор", "Демонический")
    print(weap)
    print("Что? Ты вернулся... еще и оружие нашел? Ладно... можешь отправиться к нашим Богам, может, там тебе повезет больше")
    try: #пробуем вызвать созданное исключение
        t = TypeWeapon("Jesus", 6, 0.1, True, True, "убить бога", "Божественный", "Убийца богов", "Ангельский")
        print(t)
    except ErrorNotWeapon as e:
        print(f"Речь ангела: Я не могу сказать, где найти {e}")

    print("Я не говорил тебе убить Бога, я сказал проверить. Ладно, ступай уже куда-нибудь")
    weaponss = [] #генерируем случайные оружия
    weapGEN = weaponGENERTION()
    for i in range(5):
        weaponss.append(next(weapGEN))

    print("\nИ отправился ты в путь. Во время путешествия ты нашел: ")
    for t in weaponss:
        print(t)

    a = weaponss[0]#пробуем провеить перегрузку равенств
    b = weaponss[1]
    print("Большой улов, давай же посмотрим, что можно с ним сделать!")
    print(f"Оружие {a.name} схоже с {b.name} и его ранг можно повысить? Мой ответ: {a == b}")


if __name__ == '__main__':
    main()
    input("Введите ENTER, чтобы завершить работу")