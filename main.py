import pandas as pd
import uuid


df = pd.read_csv("documents/hotels.csv", dtype={"id": str})


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.hotel_city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()
    
    def book_hotel(self):
        """Book a hotel by changing its availability to a no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("documents/hotels.csv", index=False)
        
    
    def available(self):
        """Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
    

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object
    
    def generate(self):
        """Generate a unique code for both the guest and the hotel - send an email to the guest and hotel with the unique code"""
        random_code = uuid.uuid4().hex.upper()[0:5]
        content = f"""
        Thank you for your reservation!\n
        Here is your booking data: 
        {self.customer_name}
        {self.hotel.hotel_name} - {self.hotel.hotel_city}
        \n
        {random_code}
        """
        return content
    
    
print(df)

hotel_ID = input("Enter the ID of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    hotel.book_hotel()
    name = input("Enter your name: ")
    booking_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
    print(booking_ticket.generate())
else:
    print("Hotel is not available to book")