import csv
import datetime as dt
from pathlib import Path

from itemadapter import ItemAdapter

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results"
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_count = {}
        RESULTS_DIR.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        status = adapter.get("status", "")
        self.status_count[status] = (
            self.status_count.get(status, 0) + 1
        )
        return item

    def close_spider(self, spider):
        now = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f"status_summary_{now}.csv"
        file_path = RESULTS_DIR / file_name
        total = sum(self.status_count.values())
        rows = [["Статус", "Количество"]]
        rows.extend(
            [status, count]
            for status, count in self.status_count.items()
        )
        rows.append(["Total", total])
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
