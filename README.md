# Web Crawler
A crawler that can go through a complete website and find a specific element.

Entirely written in Python

### How often should you run this crawler
I would recommend running the crawler once a month to see if something changed.
To do so, clone this repository and use Crontab (for macOS). 
Here is a helpful tutorial on scheduling jobs - [Crontab Tutorial](https://betterprogramming.pub/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30i)


### Third Party Libraries
* [beautiful soup](https://pypi.org/project/beautifulsoup4/) - for HTML parsing
* [Tenacity](https://tenacity.readthedocs.io/en/latest/w) - for retry behavior
