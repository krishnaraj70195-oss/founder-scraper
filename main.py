import asyncio
import itertools
import os

from extractor import WebsiteExtractor
from analyzer import LeadershipAnalyzer

from utils import (
    load_websites,
    create_output_files,
    append_result,
    append_failed,
    load_completed_websites,
)

CONCURRENCY = 20

# Proxy rotation - cycle through all available proxies
PROXIES = [
    "http://107.173.47.31:8888",  # VPS tinyproxy
    f"http://itskrisz_245:Krisz@$$78130@us-ca.proxymesh.com:31280",  # ProxyMesh
    None,  # No proxy (datacenter IP)
]

proxy_cycle = itertools.cycle(PROXIES)


def get_next_proxy():
    return next(proxy_cycle)


async def process_website(
    website,
    extractor,
    analyzer,
    semaphore
):

    async with semaphore:

        proxy = get_next_proxy()
        print(f"[SCRAPING] {website} (proxy: {proxy if proxy else 'direct'})")

        try:

            extracted = await extractor.scrape_website(
                website,
                proxy=proxy
            )

            text = extracted["text"]

            if not text:

                print(f"[NO TEXT] {website}")

                append_failed(website)

                return

            people = await analyzer.analyze(text)

            if not people:

                print(f"[NO PEOPLE] {website}")

                append_failed(website)

                return

            for person in people:

                append_result(
                    website,
                    person["role"],
                    person["full_name"]
                )

            print(
                f"[SUCCESS] {website} "
                f"({len(people)} people)"
            )

        except Exception as e:

            print(f"[ERROR] {website} -> {e}")

            append_failed(website)


async def main():

    create_output_files()

    # Use test_websites.txt by default, switch to failed_websites.txt to retry
    input_file = os.getenv("INPUT_FILE", "input/test_websites.txt")

    websites = load_websites(input_file)

    completed = load_completed_websites()

    websites = [
        w for w in websites
        if w not in completed
    ]

    print(f"Remaining websites: {len(websites)}")
    print(f"Using proxies: VPS + ProxyMesh + Direct")

    extractor = WebsiteExtractor(timeout=45000)

    analyzer = LeadershipAnalyzer()

    await extractor.start()

    semaphore = asyncio.Semaphore(CONCURRENCY)

    tasks = []

    for website in websites:

        task = process_website(
            website,
            extractor,
            analyzer,
            semaphore
        )

        tasks.append(task)

    await asyncio.gather(*tasks)

    await extractor.close()

    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
