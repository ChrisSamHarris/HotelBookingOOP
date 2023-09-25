import pandas as pd
import uuid

df = pd.read_csv("documents/hotels.csv", dtype={"id": str})
df_cc = pd.read_csv("documents/cards.csv", dtype=str).to_dict(orient="records")
df_cc_security = pd.read_csv("documents/card_security.csv", dtype=str)


class Hotel:
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
        
class SpaHotel(Hotel):
    def book_spa_package(self):
        pass
    

class ReservationTicket:
    def __init__(self, customer_name, hotel_object) -> None:
        self.customer_name = customer_name
        self.hotel = hotel_object
    
    def generate(self) -> str:
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
    
    
class SpaReservation(ReservationTicket):
    def generate(self) -> str:
        """Generate a unique code for both the guest and the hotel - send an email to the guest and hotel with the unique code - SPA reservation"""
        random_code = uuid.uuid4().hex.upper()[0:5]
        content = f"""
        Thank you for your SPA reservation!\n
        Here is your booking data: 
        {self.customer_name}
        {self.hotel.hotel_name} - {self.hotel.hotel_city}
        \n
        {random_code}
        """
        return content
    
    
class CreditCard:
    def __init__(self, cc_number) -> None:
        self.cc_number = cc_number
    
    def validate(self, cc_expiration, cc_holder, cc_cvc) -> bool:
        card_data = {'number': self.cc_number, 'expiration':cc_expiration,
                     'cvc':cc_cvc, 'holder':cc_holder.upper()}
        if card_data in df_cc:
            return True


class SecureCreditCard(CreditCard):
    """Inheritcs the parent Class and capabilities."""
    def authenticate(self, given_password) -> bool:
        password = df_cc_security.loc[df_cc_security["number"] == self.cc_number, "password"].squeeze()
        if password == given_password:
            return True

    
print(df)
hotel_ID = input("Enter the ID of the hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(cc_number="1234567890123456")
    if credit_card.validate(cc_expiration="12/26", cc_cvc="123", cc_holder="John Smith"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book_hotel()
            name = input("Enter your name: ")
            booking_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(booking_ticket.generate())
            spa_booking = input("Do you want to book a spa package?").lower()
            if spa_booking == "y" or spa_booking == "yes":
                booking_ticket = SpaReservation(customer_name=name, hotel_object=hotel)
                print(booking_ticket.generate())
        else: 
            print("\nCredit card authentication failed.")
    else:
        print("\nThere was a problem with your payment method..")
else:
    print("\nHotel has no availability!")