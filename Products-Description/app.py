

import pandas as pd
from playwright.sync_api import sync_playwright
import time

def get_amazon_description(page, product_name):
    try:
       
        search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        
   
        if "captcha" in page.url or page.locator("text=Type the characters you see below").is_visible():
            print(f"⚠️ CAPTCHA detected! Solve it manually in the browser...")
            page.wait_for_selector("#twotabsearchtextbox", timeout=120000)

      
        page.wait_for_selector('[data-component-type="s-search-result"]', timeout=15000) 
        
   
        all_results = page.locator('[data-component-type="s-search-result"]') 
        
      
        product_found = False
        product_link = None
        
        for i in range(min(10, all_results.count())): 
            result = all_results.nth(i)
            
           
            is_sponsored = False
            
            
            try:
                if result.locator('text=Sponsored').first.is_visible(timeout=1000): 
                    is_sponsored = True
                elif result.locator('[data-component-type="sp-sponsored-result-info"]').first.is_visible(timeout=1000):
                    is_sponsored = True
                elif result.locator('.s-sponsored-label-info-icon').first.is_visible(timeout=1000):
                    is_sponsored = True
            except:
                pass
            
            if not is_sponsored:
                
                try:
                    product_link = result.locator('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').first
                    if product_link.is_visible(timeout=1000):
                        print(f"   Found non-sponsored product at position {i+1}")
                        product_found = True
                        break
                except:
                    continue
       
        if not product_found or product_link is None:
            print(f"   ⚠️ No non-sponsored products found, using first available")
            
            product_link = page.locator('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').first
        
      
        with page.context.expect_page() as new_page_info: 
            product_link.click()
        
        product_page = new_page_info.value
        product_page.wait_for_load_state("domcontentloaded")

  
        try:
            
            show_more_selectors = [
                "#feature-bullets .a-expander-prompt",
                "#feature-bullets button.a-expander-prompt",
                "span.a-expander-prompt",
                "button:has-text('Show More')",
                "button:has-text('See More')",
                "span:has-text('Show More')",
                "span:has-text('See More')",
                ".a-expander-header .a-expander-prompt"
            ]
            
            clicked = False
            for selector in show_more_selectors:
                try:
                    show_more_btn = product_page.locator(selector).first
                    if show_more_btn.is_visible(timeout=2000):
                        print("   Expanding 'Show More'/'See More' for full description...")
                        show_more_btn.scroll_into_view_if_needed()
                        show_more_btn.click()
                        product_page.wait_for_timeout(1500)
                        clicked = True
                        break
                except:
                    continue
            
   
            if not clicked:
     
                try:
                    expanders = product_page.locator("#feature-bullets [class*='expander'], #feature-bullets [class*='Expander']") 
                    for i in range(expanders.count()):
                        element = expanders.nth(i)
                        if element.is_visible(timeout=1000):
                            element_text = element.inner_text().lower()
                            if 'show' in element_text or 'more' in element_text or 'see' in element_text:
                                element.click()
                                product_page.wait_for_timeout(1500)
                                break
                except:
                    pass
        except Exception as e:
            print(f"   Note: Could not find/show more button: {str(e)[:50]}")


        try:
            product_page.wait_for_selector("#feature-bullets", timeout=10000)
            description_element = product_page.locator("#feature-bullets").first
            raw_text = description_element.inner_text()
            
           
            clean_text = raw_text.replace("About this item", "").replace("Show More", "").replace("Show less", "").replace("See More", "").replace("See less", "").strip()
            clean_text = " ".join(clean_text.split())
        except:
            print("  Could not find description, trying alternative selectors...")
        
            alt_selectors = [
                "#productDescription",
                "#aplus",
                ".product-description",
                ".aplus-v2",
                "[data-feature-name='productDescription']"
            ]
            
            clean_text = "Not found"
            for selector in alt_selectors:
                try:
                    desc_element = product_page.locator(selector).first
                    if desc_element.is_visible(timeout=2000):
                        clean_text = desc_element.inner_text()
                        clean_text = " ".join(clean_text.split())
                        break
                except:
                    continue
        
        product_page.close()
        return clean_text

    except Exception as e:
        print(f" Error for {product_name}: {str(e)[:50]}")
        return "Not found"

def main():
    try:
        df = pd.read_excel('products.xlsx') 
    except:
        print("Error: products.xlsx file not found")
        return

    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(   
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page() 

        for i, row in df.iterrows(): 
            product = str(row['Product Name']) 
            print(f"Processing ({i+1}/{len(df)}): {product}") 
            
            desc = get_amazon_description(page, product)
            df.at[i, 'Description'] = desc
            
           
            time.sleep(2)
        
      
        print("\nAll products processed")
        browser.close()

    df.to_excel('products_filled.xlsx', index=False)
    print("\nSUCCESS! All descriptions (full)")

if __name__ == "__main__":
    main()