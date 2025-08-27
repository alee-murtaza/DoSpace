from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import os

def download_floor_image():
    """
    Clean flow: Go to URL → Wait 15s → Click Floor tab → Wait 10s → Click floor 126 → Download → 
    Navigate back → Click Floor tab → Wait 10s → Click floor 126 → Wait 15s → Canvas snapshot
    """
    driver = None
    try:
        print("🚀 Starting Floor Image Download")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize driver
        print("📱 Setting up Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Step 1: Go to URL
        print("🌐 Navigating to DoSpace...")
        driver.get("https://app.dospace.com/spaces/demo")
        
        # Step 2: Wait 15 seconds
        print("⏳ Waiting 15 seconds...")
        time.sleep(15)
        
        # Step 3: Click on Floor tab
        print("🏠 Looking for Floor tab...")
        
        # Wait for navigation to be present
        print("⏳ Waiting for navigation elements to load...")
        wait = WebDriverWait(driver, 30)
        
        try:
            # Wait for nav element to be present
            nav = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
            print("✅ Navigation element found")
            
            # Wait a bit more for all tabs to be visible
            time.sleep(3)
            
            # Try multiple methods to find Floor tab
            floor_tab = None
            
            # Method 1: Try to find Floor tab using the exact structure
            try:
                floor_tab = driver.find_element(By.XPATH, "//div[contains(@class, 'flex') and contains(@class, 'z-20') and contains(@class, 'bg-white') and contains(@class, 'rounded-t-[20px]')]//span[text()='Floor']/..")
                print("✅ Floor tab found using exact structure")
            except:
                print("⚠️  Exact structure method failed...")
            
            # Method 2: Try finding by text content
            if not floor_tab:
                try:
                    # Look for any element containing "Floor" text
                    floor_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Floor')]")
                    if floor_elements:
                        for element in floor_elements:
                            if element.text.strip() == "Floor":
                                # Get the clickable parent div
                                floor_tab = element.find_element(By.XPATH, "./..")
                                print("✅ Floor tab found using text search")
                                break
                    if not floor_tab:
                        print("⚠️  No element with 'Floor' text found...")
                except:
                    print("⚠️  Text search method failed...")
            
            # Method 3: Try finding by navigation order (Floor should be second tab)
            if not floor_tab:
                try:
                    nav_divs = nav.find_elements(By.CSS_SELECTOR, "div.flex.w-auto.shrink-0.grow.items-center.justify-center")
                    print(f"🔍 Found {len(nav_divs)} navigation tabs")
                    
                    for i, tab in enumerate(nav_divs):
                        try:
                            tab_text = tab.text.strip()
                            print(f"  Tab {i+1}: '{tab_text}'")
                            if tab_text == "Floor":
                                floor_tab = tab
                                print(f"✅ Floor tab found at position {i+1}")
                                break
                        except:
                            print(f"  Tab {i+1}: Could not get text")
                    
                    if not floor_tab:
                        print("⚠️  Floor tab not found in navigation order...")
                        
                except Exception as e:
                    print(f"⚠️  Navigation order method failed: {str(e)}")
            
            # Method 4: Try finding any clickable div with Floor text
            if not floor_tab:
                try:
                    all_divs = driver.find_elements(By.CSS_SELECTOR, "div[class*='cursor-pointer']")
                    for div in all_divs:
                        if "Floor" in div.text:
                            floor_tab = div
                            print("✅ Floor tab found using cursor-pointer search")
                            break
                    if not floor_tab:
                        print("⚠️  No clickable div with Floor text found...")
                except:
                    print("⚠️  Cursor-pointer search failed...")
            
            if not floor_tab:
                print("❌ Could not find Floor tab with any method")
                # Take a screenshot and show page source for debugging
                driver.save_screenshot("debug_no_floor_tab.png")
                print("📸 Debug screenshot saved: debug_no_floor_tab.png")
                
                # Show what's actually in the navigation
                print("🔍 Current navigation content:")
                try:
                    nav_html = nav.get_attribute("outerHTML")
                    print(f"Navigation HTML: {nav_html[:500]}...")
                except:
                    print("Could not get navigation HTML")
                
                return False
            
            # Verify we found the right element
            if "Floor" not in floor_tab.text:
                print(f"❌ Wrong element found! Text is '{floor_tab.text}', expected 'Floor'")
                return False
            
            print(f"🎯 Floor tab element found: {floor_tab.tag_name} with text: '{floor_tab.text}'")
            print(f"📍 Floor tab location: {floor_tab.location}")
            print(f"📏 Floor tab size: {floor_tab.size}")
            
        except Exception as e:
            print(f"❌ Error finding Floor tab: {str(e)}")
            driver.save_screenshot("error_floor_tab.png")
            print("📸 Error screenshot saved: error_floor_tab.png")
            return False
        
        print("🖱️  Clicking on Floor tab...")
        driver.execute_script("arguments[0].click();", floor_tab)
        
        # Step 4: Wait 10 seconds for floors to load
        print("⏳ Waiting 10 seconds for floors to load...")
        time.sleep(10)
        
        # Step 5: Find and click on floor thumbnail with ID 126
        print("🔍 Looking for floor thumbnail with ID 126...")
        try:
            # Look for floor thumbnail with ID 126
            floor_126 = driver.find_element(By.CSS_SELECTOR, "div[style*='floor-thumbnail-126.jpg']")
            print("✅ Found floor thumbnail with ID 126")
            
            # Click on the floor thumbnail
            print("🖱️  Clicking on floor thumbnail 126...")
            driver.execute_script("arguments[0].click();", floor_126)
            
            # Get the background image URL for download
            background_style = floor_126.get_attribute("style")
            background_url = ""
            if "background-image" in background_style:
                background_url = background_style.split("url(")[1].split(")")[0].strip('"')
            
            print(f"🎨 Floor thumbnail URL: {background_url}")
            
        except Exception as e:
            print(f"❌ Could not find floor thumbnail with ID 126: {str(e)}")
            return False
        
        # Step 6: Download the floor image
        print("⬇️  Downloading floor image...")
        try:
            # Navigate to the image URL in the same browser session
            driver.get(background_url)
            time.sleep(2)
            
            # Take screenshot of the image
            image_filename = "floor_126_thumbnail.png"
            driver.save_screenshot(image_filename)
            print(f"✅ Floor thumbnail downloaded: {image_filename}")
            
        except Exception as e:
            print(f"⚠️  Could not download thumbnail: {str(e)}")
        
        # Step 7: Navigate back to DoSpace
        print("🔄 Navigating back to DoSpace...")
        driver.get("https://app.dospace.com/spaces/demo")
        
        # Step 8: Click on Floor tab again
        print("🖱️  Clicking on Floor tab again...")
        try:
            floor_tab = driver.find_element(By.XPATH, "//div[contains(@class, 'flex') and contains(@class, 'z-20') and contains(@class, 'bg-white') and contains(@class, 'rounded-t-[20px]')]//span[text()='Floor']/..")
            driver.execute_script("arguments[0].click();", floor_tab)
            print("✅ Floor tab clicked again")
        except:
            # Fallback
            floor_span = driver.find_element(By.XPATH, "//span[text()='Floor']")
            floor_tab = floor_span.find_element(By.XPATH, "./..")
            driver.execute_script("arguments[0].click();", floor_tab)
            print("✅ Floor tab clicked again (fallback)")
        
        # Step 9: Wait 10 seconds for floors to load
        print("⏳ Waiting 10 seconds for floors to load again...")
        time.sleep(10)
        
        # Step 10: Click on the same floor thumbnail (ID 126) to view in canvas
        print("🖱️  Clicking on floor thumbnail 126 to view in canvas...")
        try:
            floor_126_again = driver.find_element(By.CSS_SELECTOR, "div[style*='floor-thumbnail-126.jpg']")
            driver.execute_script("arguments[0].click();", floor_126_again)
            print("✅ Floor thumbnail 126 clicked for canvas view")
            
        except Exception as e:
            print(f"❌ Could not click floor thumbnail 126 again: {str(e)}")
            return False
        
        # Step 11: Wait 15 seconds for floor to be implemented in canvas
        print("⏳ Waiting 15 seconds for floor to be implemented in canvas...")
        time.sleep(15)
        
        # Step 12: Take snapshot of canvas
        print("📸 Taking snapshot of canvas...")
        try:
            canvas = driver.find_element(By.CSS_SELECTOR, "canvas[data-engine='three.js r161']")
            if canvas.is_displayed():
                # Get canvas location and size
                canvas_location = canvas.location
                canvas_size = canvas.size
                
                # Take full page screenshot first
                full_screenshot = driver.get_screenshot_as_png()
                
                # Import PIL for image cropping
                from PIL import Image
                import io
                
                # Open the screenshot and crop to canvas area
                full_image = Image.open(io.BytesIO(full_screenshot))
                
                # Calculate crop coordinates
                left = canvas_location['x']
                top = canvas_location['y']
                right = left + canvas_size['width']
                bottom = top + canvas_size['height']
                
                # Crop the image to canvas area
                canvas_image = full_image.crop((left, top, right, bottom))
                
                # Save the cropped canvas image
                canvas_filename = "floor_126_canvas_implemented.png"
                canvas_image.save(canvas_filename)
                print(f"✅ Canvas-only snapshot saved: {canvas_filename}")
                
                # Also save canvas location info
                location_filename = "floor_126_canvas_location.txt"
                with open(location_filename, 'w') as f:
                    f.write(f"Floor ID: 126\n")
                    f.write(f"Canvas Location: x={canvas_location['x']}, y={canvas_location['y']}\n")
                    f.write(f"Canvas Size: width={canvas_size['width']}, height={canvas_size['height']}\n")
                    f.write(f"Crop Coordinates: left={left}, top={top}, right={right}, bottom={bottom}\n")
                    f.write(f"Applied at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"✅ Canvas location info saved: {location_filename}")
                
            else:
                print("⚠️  3D canvas is not visible")
                
        except Exception as e:
            print(f"⚠️  Could not capture canvas: {str(e)}")
        
        print(f"📁 All files saved to: {os.getcwd()}")
        return True
            
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return False
        
    finally:
        if driver:
            print("🧹 Cleaning up...")
            driver.quit()
            print("✅ WebDriver closed")

def main():
    """Main function"""
    print("=" * 50)
    print("⬇️  Floor Image Download Script (Clean Flow)")
    print("📋 Steps: URL → 15s → Floor tab → 10s → Floor 126 → Download → Back → Floor tab → 10s → Floor 126 → 15s → Canvas")
    print("=" * 50)
    
    success = download_floor_image()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS: Floor 126 downloaded and implemented in canvas!")
    else:
        print("❌ FAILED: Could not complete the process")
    print("=" * 50)

if __name__ == "__main__":
    main() 