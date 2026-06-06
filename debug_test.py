import os
import traceback
import time
import mysql.connector

def debug_test():
    print("=== DEBUG TEST START ===")

    # Step 1: MySQL connection
    print("\n[1] Testing MySQL connection...")
    try:
        mydb = mysql.connector.connect(
            host="localhost", user="root", passwd="mysql", database="DBConnection")
        mycursor = mydb.cursor()
        mycursor.execute("SHOW TABLES")
        print("[1] Tables:", mycursor.fetchall())
        mycursor.execute("DELETE FROM users")
        mycursor.execute("DELETE FROM repos")
        mydb.commit()
        print("[1] Tables cleared OK")
    except Exception as e:
        print("[1] MySQL FAILED:", e)
        traceback.print_exc()
        return

    # Step 1.5: Direct HTTP POST - detects old vs new code
    print("\n[1.5] Direct HTTP POST to /CreateUser...")
    try:
        import urllib.request
        import urllib.parse
        import re
        data = urllib.parse.urlencode({'userName': 'httpcheck'}).encode()
        resp = urllib.request.urlopen('http://localhost:8000/CreateUser', data=data, timeout=5)
        final_url = resp.url
        body = resp.read().decode('utf-8', errors='replace')
        print("[1.5] Final URL:", final_url)
        if 'status=' in final_url:
            print("[1.5] OLD CODE RUNNING (redirect) - server NOT restarted after paste!")
        else:
            print("[1.5] NEW CODE RUNNING (forward)")
        m = re.search(r"alert\([\"']([^\"']+)[\"']", body)
        if m:
            print("[1.5] Alert content in HTML:", repr(m.group(1)))
        else:
            print("[1.5] No alert found. Body snippet:\n", body[:600])
    except Exception as e:
        print("[1.5] Direct POST check failed:", e)
        traceback.print_exc()

    # Step 2: Start Chrome
    print("\n[2] Starting Chrome...")
    browser = None
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        print("[2] Chrome started OK")
    except Exception as e:
        print("[2] Chrome FAILED:", e)
        traceback.print_exc()
        return

    try:
        # Step 3: Load page
        print("\n[3] Loading http://localhost:8000 ...")
        browser.get("http://localhost:8000")
        print("[3] Title:", browser.title)
        print("[3] URL:", browser.current_url)

        # Step 4: Find form elements
        print("\n[4] Finding form elements...")
        try:
            inp = browser.find_element_by_id("userName")
            print("[4] #userName found OK")
        except Exception as e:
            print("[4] #userName NOT found:", e)
            print("[4] Page source:\n", browser.page_source[:3000])
            return
        try:
            btn = browser.find_element_by_id("create")
            print("[4] #create button found OK")
        except Exception as e:
            print("[4] #create NOT found:", e)
            return

        # Step 5: Create first user
        print("\n[5] Creating user qwerty001...")
        inp.send_keys("qwerty001")
        btn.click()
        print("[5] Clicked submit")
        time.sleep(2)

        try:
            alert = browser.switch_to.alert
            print("[5] Alert text:", repr(alert.text))
            alert.accept()
            print("[5] Alert accepted OK")
        except Exception as e:
            print("[5] NO ALERT:", e)
            print("[5] URL after click:", browser.current_url)
            print("[5] Page source:\n", browser.page_source[:3000])

        time.sleep(2)

        # Step 6: Create second user
        print("\n[6] Creating user qwerty002...")
        try:
            inp2 = browser.find_element_by_id("userName")
            print("[6] #userName found OK")
        except Exception as e:
            print("[6] #userName NOT found after first submit:", e)
            print("[6] URL:", browser.current_url)
            print("[6] Page source:\n", browser.page_source[:3000])
            return

        inp2.send_keys("qwerty002")
        browser.find_element_by_id("create").click()
        print("[6] Clicked submit")
        time.sleep(1)

        try:
            alert2 = browser.switch_to.alert
            print("[6] Alert text:", repr(alert2.text))
            alert2.accept()
            print("[6] Alert accepted OK")
        except Exception as e:
            print("[6] NO ALERT:", e)
            print("[6] URL:", browser.current_url)

        # Step 7: Check users in DB
        print("\n[7] Checking users in DB...")
        mydb2 = mysql.connector.connect(
            host="localhost", user="root", passwd="mysql", database="DBConnection")
        mycursor2 = mydb2.cursor()
        mycursor2.execute("SELECT * FROM users")
        records = mycursor2.fetchall()
        print("[7] Users:", records)

        if len(records) < 2:
            print("[7] ERROR: need 2 users, got", len(records))
            return

        newlist = [row[0] for row in records]
        print("[7] userIds:", newlist)

        # Step 8: curl CreateRepo
        print("\n[8] Creating repo via curl...")
        params = "userId=" + newlist[0] + "&RepoName=testrepo&RepoDesc=testrepodesc&RepoDev=" + newlist[1]
        command = 'curl -v -X POST -d "' + params + '" http://localhost:8000/CreateRepo'
        print("[8] Command:", command)
        ret = os.system(command)
        print("[8] curl exit code:", ret)
        time.sleep(1)

        # Step 9: Check repos in DB
        print("\n[9] Checking repos in DB...")
        mydb3 = mysql.connector.connect(
            host="localhost", user="root", passwd="mysql", database="DBConnection")
        mycursor3 = mydb3.cursor()
        mycursor3.execute("SELECT * FROM repos")
        rows = mycursor3.fetchall()
        print("[9] Repos:", rows)

        if not rows:
            print("[9] ERROR: no repos in DB!")
            return

        myresult = rows[0]
        print("[9] myresult[1] (userId)  =", myresult[1])
        print("[9] newlist[0] (expected) =", newlist[0])
        print("[9] myresult[4] (RepoDev) =", myresult[4])
        print("[9] newlist[1] (expected) =", newlist[1])

        if myresult[1] == newlist[0] and myresult[4] == newlist[1]:
            print("\n=== FS_SCORE:100% ===")
        else:
            print("\n=== MISMATCH: check values above ===")

    except Exception as e:
        print("\nUNEXPECTED ERROR:", e)
        traceback.print_exc()
    finally:
        if browser:
            browser.quit()
            print("[DONE] Browser closed")

debug_test()
