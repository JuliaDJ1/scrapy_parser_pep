BOT_NAME = "pep_parse"

SPIDER_MODULES = ["pep_parse.spiders"]
NEWSPIDER_MODULE = "pep_parse.spiders"

ADDONS = {}

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    "pep_parse.pipelines.PepParsePipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    "results/pep_%(time)s.csv": {
        "format": "csv",
        "encoding": "utf-8",
        "fields": ["number", "name", "status"],
        "item_export_kwargs": {
            "include_headers_line": True,
        },
    },
}

PEP_URL = 'https://peps.python.org/'
