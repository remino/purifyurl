# purifyurl

Short Python 3 script to remove tracking parameters from URLs.

## Installation

```sh
git clone https://github.com/remino/purifyurl
cd purifyurl
pip install -r requirements.txt
```

## Usage

```sh
./purifyurl 'https://youtu.be/abc&feature=def'
# https://www.youtube.com/watch?v=abc

echo 'Go to https://youtu.be/abc&feature=def to watch the video.' | ./purifyurl
# Go to https://www.youtube.com/watch?v=abc to watch the video.
```

See `./purifyurl --help` for more options.

## Libraries

This script uses the following libraries or sources:

- [URL Cleaner](https://github.com/fireindark707/url_cleaner)
- [AdGuardFilters](https://github.com/AdguardTeam/AdguardFilters)

