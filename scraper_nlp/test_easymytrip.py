"""Small CLI runner to test the EasyMyTrip scraper adapter.

Usage:
  .venv\Scripts\python.exe test_easymytrip.py --from "Delhi" --to "Mumbai" --date 2025-11-09
"""
import argparse
import pprint

from providers.easymytrip import search_flights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='frm', required=True)
    parser.add_argument('--to', dest='to', required=True)
    parser.add_argument('--date', dest='date', required=True)
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()

    print('Running EasyMyTrip search:', args.frm, '->', args.to, args.date)
    try:
        results = search_flights(args.frm, args.to, args.date, headless=args.headless)
        print('Found', len(results), 'results')
        pprint.pprint(results[:5])
    except Exception as e:
        print('Error running scraper:', e)


if __name__ == '__main__':
    main()
