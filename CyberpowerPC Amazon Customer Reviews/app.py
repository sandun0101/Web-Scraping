from scraper.reviews_scraper import ReviewsScraper

try:
    with ReviewsScraper() as bot:
        bot.land_first_page()
        bot.login()
        bot.review_scraper()

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
