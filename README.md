# Telegram UrlProBot

Bot available at [telegram.me/UrlProBot](http://telegram.me/UrlProBot)

## Usage

Be sure to create the file `urlprobot.conf` and set it as follows:

```
[DEFAULTS]
bot_token = 1234567890EXAMPLE0987654321
google_client = 1234567890EXAMPLE0987654321
min_url_size = 5
bitly = 1234567890EXAMPLE0987654321
```

Then run:

```
$ pip install -r requirements.txt
$ python3 urlprobot.py
```

## Need help

I tried to add inline queries to this bot. It worked, but the VM's load would eventually get really high. So I removed the functionality.

My last attempt is commented on the code. Pull requests are welcome!
