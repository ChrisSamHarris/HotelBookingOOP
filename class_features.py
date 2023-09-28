import pandas as pd
import uuid
from abc import ABC, abstractmethod

df = pd.read_csv("documents/hotels.csv", dtype={"id": str})


class Hotel:
    # Value of a class variable : can be shared across all class instances
    watermark = "The real estate company"
    
    def __init__(self, hotel_id) -> None:
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.hotel_city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()
    
    def book_hotel(self) -> None:
        """Book a hotel by changing its availability to a no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("documents/hotels.csv", index=False)
        
    
    def available(self) -> bool:
        """Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
    
    @classmethod
    def get_hotel_count(cls, data):
        """Class method = related to a class but not specifically tied to an instance. Note best practice: cls argument"""
        return len(data)
    
    def __eq__(self, other) -> bool:
        if self.hotel_id == other.hotel_id:
            return True
        
    def __add__(self, other) -> float:
        total = self.price + other.price
        return total
    

class Ticket(ABC):
    """ABC = Abstract Based Class"""
    
    @abstractmethod
    def generate(self):
        pass

class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_object) -> None:
        self.customer_name = customer_name
        self.hotel = hotel_object
        
    def generate(self) -> str:
        """Generate a unique code for both the guest and the hotel - send an email to the guest and hotel with the unique code"""
        random_code = uuid.uuid4().hex.upper()[0:5]
        content = f"""
        Thank you for your reservation!\n
        Here is your booking data: 
        {self.the_customer_name}
        {self.hotel.hotel_name} - {self.hotel.hotel_city}
        \n
        {random_code}
        """
        return content
    
    @property
    def the_customer_name(self):
        """Class properties to be used for some processing - can be accessed as a normal instance variable"""
        name = self.customer_name.strip()
        name = name.title()
        return name
    
    @staticmethod
    def convert(amount):
        """Typically used for utilities, often less associated than classmethods"""
        return amount * 1.2
    

class DigitalTicket(ReservationTicket):
    def generate(self) -> str:
        return "<Digital Ticket>"
    
        
    
hotel1 = Hotel(hotel_id="188")
hotel2 = Hotel(hotel_id="134")

print(hotel1.available())

print(hotel1.hotel_name)
print(hotel2.hotel_name)

print(hotel1.watermark)
print(hotel2.watermark)

print(Hotel.watermark)

print(Hotel.get_hotel_count(data=df))
print(hotel1.get_hotel_count(data=df))

ticket = ReservationTicket(customer_name="chris harris   ", hotel_object=hotel1)
print(ticket.the_customer_name)
print(ticket.generate())

converted = ReservationTicket.convert(10)
print(converted)