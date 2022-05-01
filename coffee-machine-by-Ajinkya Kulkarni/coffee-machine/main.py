from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


is_on=True
coffee_maker=CoffeeMaker()
money_machine=MoneyMachine()
my_menu=Menu()

while(is_on==True):
    menu_items = my_menu.get_items()
    user_choice = input(f"What would you like?{menu_items}: ")

    if user_choice=="off" :
        is_on=False

    elif user_choice == "report":
        coffee_maker.report()
        money_machine.report()

    else:
        drink = my_menu.find_drink(user_choice)
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)

