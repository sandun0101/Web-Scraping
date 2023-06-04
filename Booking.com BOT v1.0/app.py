from booking.booking import Booking


try:
    with Booking() as bot:
        bot.land_first_page()
        bot.dismiss_signin_info()
        bot.currency_list()
        bot.select_currency()
        bot.select_place_to_go()
        bot.select_dates()
        bot.select_people_count()
        bot.select_room_count()
        bot.search_data()
        bot.apply_filtrations()
        bot.scraper()

except Exception as e:

    if "in PATH" in str(e):
        print(
            "You are trying to run the bot from command line\n"
            "Please add to PATH your Selenium Drivers \n"
            "Windows: \n"
            "       set PATH=%PATH%;C:path-to-your-driver-folder \n \n"
            "Linux: \n"
            "       PATH=$PATH:/path/toyour/driver/folder/ \n"
        )
    else:
        raise

