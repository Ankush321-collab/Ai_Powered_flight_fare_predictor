"""Small CLI runner to test the EasyMyTrip scraper adapter.

Usage:
  python test_easymytrip.py --from "Delhi" --to "Mumbai" --date 2025-11-09
"""
import argparse
import pprint
import json
import sys

from providers.easymytrip import search_flights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='frm', required=True)
    parser.add_argument('--to', dest='to', required=True)
    parser.add_argument('--date', dest='date', required=True)
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    args = parser.parse_args()

    if not args.json:
        print('Running EasyMyTrip search:', args.frm, '->', args.to, args.date, file=sys.stderr)
    
    try:
        results = search_flights(args.frm, args.to, args.date, headless=args.headless)
        
        if args.json:
            # Output as JSON for backend integration
            print(json.dumps(results))
        else:
            print('Found', len(results), 'results')
            pprint.pprint(results[:5])
            
    except Exception as e:
        if args.json:
            print(json.dumps({'error': str(e)}))
        else:
            print('Error running scraper:', e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
