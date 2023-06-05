from utils.data import Reviews

if __name__ == "__main__":
    try:
        with Reviews() as bot:
            bot.scrape_data()
    except Exception as e:
        if "in PATH" in str(e):
            print(
                "You are trying to run the bot from the command line\n"
                "Please add your Selenium Drivers to the PATH environment variable\n"
                "Windows:\n"
                "    set PATH=%PATH%;C:path-to-your-driver-folder\n\n"
                "Linux:\n"
                "    export PATH=$PATH:/path/toyour/driver/folder/\n"
            )
        else:
            print("An error occurred:", str(e))
