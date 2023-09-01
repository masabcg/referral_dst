num_rooms = 'num_rooms'
num_people = 'num_people'
housearea = 'housearea'
is_ac = 'is_ac'
is_tv = 'is_tv'
is_flat = 'is_flat'
ave_monthly_income = 'ave_monthly_income'
num_children = 'num_children'
is_urban = 'is_urban'
amount_paid = 'amount_paid'

list_cols = [
    num_rooms, 
    num_people, 
    housearea, 
    is_ac, 
    is_tv, 
    is_flat, 
    ave_monthly_income, 
    num_children, 
    is_urban, 
    amount_paid
            ]

cols_dtypes = {
    num_rooms: int, 
    num_people: int, 
    housearea: int, 
    is_ac: str, 
    is_tv: str, 
    is_flat: str, 
    ave_monthly_income: int, 
    num_children: int, 
    is_urban: str, 
    amount_paid: int
}