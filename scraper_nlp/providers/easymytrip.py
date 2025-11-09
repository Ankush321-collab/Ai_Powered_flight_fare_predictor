# Easy MyTrip scraper with Selenium - Direct URL approach
import time, logging
from datetime import datetime
from bs4 import BeautifulSoup
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except:
    webdriver = None
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def search_flights(from_text, to_text, date_str, headless=False, wait_sec=20):
    """
    Search for flights on EasyMyTrip by constructing the search URL directly.
    
    Args:
        from_text: Origin city/airport (e.g., "Delhi", "Kathmandu", "DEL", "KTM")
        to_text: Destination city/airport (e.g., "Mumbai", "Delhi", "BOM", "DEL")
        date_str: Date in DD/MM/YYYY format (e.g., "15/11/2025")
        headless: Run browser in headless mode
        wait_sec: Seconds to wait for results to load
    """
    # Map city names to airport codes and full city names
    city_to_airport = {
        'delhi': ('DEL', 'NewDelhi', 'India'),
        'mumbai': ('BOM', 'Mumbai', 'India'),
        'bangalore': ('BLR', 'Bangalore', 'India'),
        'kolkata': ('CCU', 'Kolkata', 'India'),
        'chennai': ('MAA', 'Chennai', 'India'),
        'hyderabad': ('HYD', 'Hyderabad', 'India'),
        'pune': ('PNQ', 'Pune', 'India'),
        'ahmedabad': ('AMD', 'Ahmedabad', 'India'),
        'goa': ('GOI', 'Goa', 'India'),
        'jaipur': ('JAI', 'Jaipur', 'India'),
        'kathmandu': ('KTM', 'Kathmandu', 'Nepal'),
        # Also support airport codes directly
        'ktm': ('KTM', 'Kathmandu', 'Nepal'),
        'del': ('DEL', 'NewDelhi', 'India'),
        'bom': ('BOM', 'Mumbai', 'India'),
        'blr': ('BLR', 'Bangalore', 'India'),
        'maa': ('MAA', 'Chennai', 'India'),
        'ccu': ('CCU', 'Kolkata', 'India'),
        'hyd': ('HYD', 'Hyderabad', 'India'),
    }
    
    # Get airport codes
    from_lower = from_text.lower().strip()
    to_lower = to_text.lower().strip()
    
    if from_lower in city_to_airport:
        from_code, from_city, from_country = city_to_airport[from_lower]
    else:
        # Assume it's already an airport code
        from_code = from_text.upper()
        from_city = from_text
        from_country = 'India'
    
    if to_lower in city_to_airport:
        to_code, to_city, to_country = city_to_airport[to_lower]
    else:
        to_code = to_text.upper()
        to_city = to_text
        to_country = 'India'
    
    # Construct the search URL directly
    # Format: srch=FROM_CODE-FromCity-Country|TO_CODE-ToCity-Country|DD/MM/YYYY
    search_query = f"{from_code}-{from_city}-{from_country}|{to_code}-{to_city}-{to_country}|{date_str}"
    search_url = f"https://flight.easemytrip.com/FlightList/Index?srch={search_query}&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=&&IsDoubleSeat=false&CCODE=IN&curr=INR&apptype=B2C"
    
    logger.info(f"Searching: {from_code} ({from_city}) → {to_code} ({to_city}) on {date_str}")
    logger.info(f"Direct URL: {search_url}")
    
    opts = Options()
    if headless: opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    opts.add_experimental_option('useAutomationExtension', False)
    
    # Try newer Selenium 4 syntax first, fall back to older versions
    try:
        from selenium.webdriver.chrome.service import Service
        svc = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=svc, options=opts)
    except:
        # Older Selenium versions
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Navigate directly to the search results URL
        driver.get(search_url)
        logger.info(f"Navigated to: {driver.current_url}")
        
        # Wait for Angular to render flight results
        logger.info("Waiting for flight cards to appear...")
        try:
            # Wait for price elements to appear (these indicate flights have loaded)
            WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[ng-bind*="TIDIS"], .cus-price, span[class*="price"]'))
            )
            logger.info("Flight price elements detected in DOM")
        except Exception as e:
            logger.warning(f"Timeout waiting for price elements: {e}")
        
        # Additional wait for all content to load
        logger.info("Waiting additional time for all flights to render...")
        time.sleep(10)
        
        # Try to extract Angular scope data directly using JavaScript
        logger.info("Attempting to extract flight data from Angular scope...")
        try:
            # Try to find the results data in multiple locations
            angular_data = driver.execute_script("""
                try {
                    // Method 1: Find flight list elements and get their scope
                    var flightDivs = document.querySelectorAll('div.list.intow, div.list[id^="divInt"]');
                    if (flightDivs.length > 0) {
                        var scope = angular.element(flightDivs[0]).scope();
                        if (scope && scope.dataToBindOutbound && Array.isArray(scope.dataToBindOutbound)) {
                            console.log('Found dataToBindOutbound from flight div:', scope.dataToBindOutbound.length);
                            return scope.dataToBindOutbound;
                        }
                    }
                    
                    // Method 2: Search all elements with ng-repeat
                    var repeatElems = document.querySelectorAll('[data-ng-repeat*="dataToBindOutbound"]');
                    if (repeatElems.length > 0) {
                        var scope = angular.element(repeatElems[0]).scope();
                        if (scope && scope.$parent && scope.$parent.dataToBindOutbound) {
                            console.log('Found dataToBindOutbound from parent scope:', scope.$parent.dataToBindOutbound.length);
                            return scope.$parent.dataToBindOutbound;
                        }
                    }
                    
                    // Method 3: Try window scope
                    var bodyScope = angular.element(document.body).scope();
                    if (bodyScope && bodyScope.$$childHead) {
                        var child = bodyScope.$$childHead;
                        while (child) {
                            if (child.dataToBindOutbound && Array.isArray(child.dataToBindOutbound) && child.dataToBindOutbound.length > 0) {
                                console.log('Found dataToBindOutbound in child scope:', child.dataToBindOutbound.length);
                                return child.dataToBindOutbound;
                            }
                            child = child.$$nextSibling;
                        }
                    }
                } catch(e) {
                    console.log('Angular extraction error:', e);
                }
                return null;
            """)
            
            if angular_data and len(angular_data) > 0:
                logger.info(f"Successfully extracted {len(angular_data)} flights from Angular scope!")
                
                # Debug: Log first flight structure to understand the data format
                if angular_data:
                    import json
                    first_flight = angular_data[0]
                    
                    # Save first flight to file for inspection
                    with open('sample_flight_raw.json', 'w', encoding='utf-8') as f:
                        json.dump(first_flight, f, indent=2, default=str)
                    logger.info(f"Saved raw flight data to sample_flight_raw.json")
                    
                    all_keys = list(first_flight.keys())
                    logger.info(f"Total keys in flight object: {len(all_keys)}")
                
                results = []
                for i, flight in enumerate(angular_data[:30]):  # Limit to first 30 flights
                    try:
                        # Flight segment data is in 'l_OB' (list of outbound segments)
                        segments = flight.get('l_OB', [])
                        if not segments or not isinstance(segments, list):
                            continue
                        
                        # Get first segment for main flight info
                        first_seg = segments[0] if segments else {}
                        
                        # Extract airline and flight number from segment
                        airline_names = first_seg.get('AN', [])
                        if isinstance(airline_names, list) and airline_names:
                            airline = airline_names[0]
                        else:
                            airline = str(airline_names) if airline_names else 'Unknown'
                        
                        # Flight codes
                        flight_codes = first_seg.get('AC', [])
                        if isinstance(flight_codes, list) and flight_codes:
                            flight_number = flight_codes[0]
                        else:
                            flight_number = str(flight_codes) if flight_codes else 'N/A'
                        
                        # Times from segment
                        dept_time = first_seg.get('DT', 'N/A')
                        arr_time = segments[-1].get('AT', 'N/A') if segments else 'N/A'  # Use last segment arrival
                        
                        # Duration from flight object
                        total_journey_time = flight.get('TJT', flight.get('TT', {}))
                        if isinstance(total_journey_time, dict):
                            hours = total_journey_time.get('h', 0)
                            mins = total_journey_time.get('m', 0)
                            duration = f"{hours}h {mins}m"
                        else:
                            duration = str(total_journey_time) if total_journey_time else 'N/A'
                        
                        # Stops
                        stops = flight.get('ST', len(segments) - 1 if segments else 0)
                        
                        # Price
                        price = flight.get('TF', flight.get('TIDIS', 0))
                        if isinstance(price, str):
                            price = float(price.replace(',', ''))
                        else:
                            price = float(price) if price else 0
                        
                        flight_info = {
                            'airline': airline,
                            'flight_number': flight_number,
                            'from': from_text,
                            'to': to_text,
                            'date': date_str,
                            'departure_time': dept_time,
                            'arrival_time': arr_time,
                            'duration': duration,
                            'stops': int(stops) if isinstance(stops, (int, float)) else 0,
                            'price': price,
                            'currency': 'INR',
                            'source': 'easymytrip',
                            'scraped_at': datetime.utcnow().isoformat()
                        }
                        if flight_info['price'] > 100:
                            results.append(flight_info)
                            if i < 5:  # Log first 5 in detail
                                logger.info(f"Extracted: {airline} {flight_number} | {dept_time}-{arr_time} | {duration} | ₹{price:.0f}")
                    except Exception as e:
                        logger.warning(f"Error parsing flight #{i} from Angular data: {e}")
                        continue
                
                if results:
                    logger.info(f"Successfully extracted {len(results)} flights from Angular! Cheapest: ₹{min(f['price'] for f in results):.0f}")
                    return results
                else:
                    logger.warning("No valid flights found in Angular data, falling back to HTML parsing")
        except Exception as e:
            logger.warning(f"Could not extract from Angular scope: {e}, falling back to HTML parsing")
        
        html = driver.page_source
        with open('last_page.html','w',encoding='utf-8') as f: f.write(html)
        logger.info("Page source saved to last_page.html")
        
        # Take a screenshot of results
        driver.save_screenshot('after_search_results.png')
        logger.info("Results screenshot saved to after_search_results.png")
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Find all flight result divs - flights have data embedded as HTML attributes!
        flight_divs = soup.select('div.fltResult[price]')
        logger.info(f"Found {len(flight_divs)} flight divs with price attributes")
        
        if not flight_divs:
            # Fallback: try alternative selectors
            flight_divs = soup.select('div[data-ng-repeat*="dataToBindOutbound"]')
            logger.info(f"Using fallback ng-repeat selector, found {len(flight_divs)} divs")
        
        import re
        airline_codes = {
            'IX': 'Air India Express',
            '6E': 'IndiGo',
            'AI': 'Air India',
            'SG': 'SpiceJet',
            'UK': 'Vistara',
            'G8': 'Go Air',
            'QP': 'Akasa Air'
        }
        
        for div in flight_divs:
            try:
                flight_info = {}
                
                # Extract from HTML attributes
                aircode = div.get('aircode', '')
                flight_info['airline'] = airline_codes.get(aircode, aircode if aircode else 'Unknown')
                flight_info['airline_code'] = aircode
                flight_info['flight_number'] = f"{aircode}-{div.get('fn', 'N/A')}"
                flight_info['aircraft_type'] = div.get('act', 'N/A')
                
                # Times
                flight_info['departure_time'] = div.get('deptm', 'N/A')
                flight_info['arrival_time'] = div.get('arrtm', 'N/A')
                
                # Calculate duration if both times available
                if flight_info['departure_time'] != 'N/A' and flight_info['arrival_time'] != 'N/A':
                    try:
                        from datetime import datetime as dt
                        dept = dt.strptime(flight_info['departure_time'], '%H:%M')
                        arrv = dt.strptime(flight_info['arrival_time'], '%H:%M')
                        diff = arrv - dept
                        hours = diff.seconds // 3600
                        mins = (diff.seconds % 3600) // 60
                        flight_info['duration'] = f"{hours}h {mins}m"
                    except:
                        flight_info['duration'] = 'N/A'
                else:
                    flight_info['duration'] = 'N/A'
                
                # Stops
                stops = div.get('stop', '0')
                flight_info['stops'] = int(stops) if stops.isdigit() else 0
                flight_info['stops_text'] = 'Non-stop' if flight_info['stops'] == 0 else f"{flight_info['stops']} stop{'s' if flight_info['stops'] > 1 else ''}"
                
                # Price
                price_str = div.get('price', '0')
                try:
                    flight_info['price'] = float(price_str)
                except:
                    flight_info['price'] = 0
                
                # Origin and destination
                flight_info['origin'] = div.get('og', from_text)
                flight_info['destination'] = div.get('ds', to_text)
                
                # Add metadata
                flight_info['from'] = from_text
                flight_info['to'] = to_text
                flight_info['date'] = date_str
                flight_info['currency'] = 'INR'
                flight_info['source'] = 'easemytrip'
                flight_info['scraped_at'] = datetime.utcnow().isoformat()
                
                # Only add if price is valid
                if flight_info['price'] > 100:
                    results.append(flight_info)
                    logger.info(f"Extracted: {flight_info['airline']} {flight_info['flight_number']} {flight_info['departure_time']}-{flight_info['arrival_time']} - ₹{flight_info['price']}")
                    
            except Exception as e:
                logger.warning(f"Error parsing flight div: {e}")
                continue
        
        # Remove duplicates based on flight_number and price
        seen = set()
        unique_results = []
        for flight in results:
            key = (flight['flight_number'], flight['price'], flight['departure_time'])
            if key not in seen:
                seen.add(key)
                unique_results.append(flight)
        
        logger.info(f"Found {len(unique_results)} unique flight results (removed {len(results) - len(unique_results)} duplicates)")
        return unique_results
    finally: driver.quit()
