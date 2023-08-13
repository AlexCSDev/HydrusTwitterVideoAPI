# Video Proxy API for Hydrus Network
Based on https://github.com/erickythierry/BaixarVideoTwitterAPI

## Supported sites:
* Twitter
* Pixiv (ugoira)

## Installation:
- Make sure ffmpeg is installed
- `pip -r requirements.txt`
- Dump your twitter cookies in netscape format into `cookies.txt`
- Configure your pixiv refresh token in `gallery-dl.conf` if you are going to be downloading pixiv ugoira
- Run the api using `python api.py`
- Open `hydrus_twitter_content_parser_video.json`, `hydrus_pixiv_content_parser_ugoira.json` and change `api_address` to address of the api
- Import `hydrus_content_parser_video.json`, `hydrus_pixiv_content_parser_ugoira.json` into your twitter and pixiv parsers via content parsers tab
- Delete `ugoira veto` from pixiv content parsers
- Depending on the machine api is running on and its internet connection speed you might want to increase `network timeout (seconds)` under `file -> options -> connection` to 30 seconds or more. Especially if you are downloading ugoira.

## Standalone API usage
Api can also be used in other software by accessing it via the following url: `http://api_address:5000/get_video?url=https://twitter.com/user/status/1234567890`
