# TON NFT Resales Notificator
:gem: Bot notifying about resales of any TON NFT collection

## How to run bot

### .env variables

You need to specify these env variables to run this bot. If you run it locally, you can also write them in `.env` text file.

``` bash
CHATS=              # Chats to send resell notifications to (separated by semicolons) // Example: "-1001536482073;-1001627286419"
BOT_TOKEN=          # Telegram bot API token from @BotFather // Example: "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROYALTY_ADDRESS=    # TON address to which royalties from resales are accrued // Example: "EQABh4JBalyRKN42tZB1jevT3BheWqHYjkhSv3zoHldqqRJs"
COLLECTION_ADDRESS= # TON address of NFT collection // Example: "EQAo92DYMokxghKcq-CkCGSk_MgXY5Fo1SPW20gkvZl75iCN"
TONCENTER_API_KEY=  # toncenter.com API key from @tonapibot

```

### Run bot locally

First, you need to install all dependencies:

```bash
pip install -r requirements.txt
```

Then you can run the bot. Don't forget to fill in the `.env` file in the root folder with all required params (read above).

``` bash
python main.py
```
