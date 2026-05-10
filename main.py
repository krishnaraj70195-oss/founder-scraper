import asyncio

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


async def process_website(
    website,
    extractor,
    analyzer,
    semaphore
):

    async with semaphore:

        print(f"[SCRAPING] {website}")

        try:

            extracted = await extractor.scrape_website(
                website
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

    websites = load_websites(
        "input/failed_websites.txt"
    )

    completed = load_completed_websites()

    websites = [
        w for w in websites
        if w not in completed
    ]

    print(f"Remaining websites: {len(websites)}")

    # Use VPS proxy for better success rate
    extractor = WebsiteExtractor(
        timeout=45000,
        proxy="http://107.173.47.31:8888"
    )

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
