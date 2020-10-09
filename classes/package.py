import mysql.connector


class Package:

    def __init__(self, package_id, destination_from, destination_to, weight, price):
        self.package_id = package_id
        self.destination_from = destination_from
        self.destination_to = destination_to
        self.weight = weight
        self.price = price


mydb = mysql.connector.connect(user='root', password='root',
                              host='localhost', database='kts')

print(mydb)
