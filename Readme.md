# Twitter video API for Hydrus Network
Based on https://github.com/erickythierry/BaixarVideoTwitterAPI

## Installation:
- `pip -r requirements.txt`
- Dump your twitter cookies in netscape format into `cookies.txt`
- Run the api using `python api.py`
- Open `hydrus_content_parser_video.json` and change `api_address` to address of the api
- Import `hydrus_content_parser_video.json` into your twitter parser via content parsers tab

## Standalone API usage
Api can also be used in other software by accessing it via the following url: `http://api_address:5000/get_tweet_video?url=https://twitter.com/user/status/1234567890`