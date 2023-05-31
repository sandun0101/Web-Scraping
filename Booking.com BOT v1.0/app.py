from booking.booking import Booking


try:
    with Booking() as bot:
        bot.land_first_page()
        bot.dismiss_signin_info()
        bot.change_currency()
        bot.select_currency()
        bot.select_place_to_go('New York')

        # check_in_date = input("Enter the check-in date (YYYY-MM-DD): ")
        # check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")

        bot.select_dates(check_in_date='2023-06-10', check_out_date='2023-06-15')
        bot.select_adult_count(1)
        bot.select_room_count(1)
        bot.search_data()
        bot.apply_filtrations()
        bot.scraper()

except Exception as e:
    print("something wrong with web driver")
