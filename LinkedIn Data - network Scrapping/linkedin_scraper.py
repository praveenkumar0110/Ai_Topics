# single profile scrap
# import requests
# import json
# import html

# VANITY_NAME = "p-suresh-webdev"

# COOKIES = {
#     "bcookie": "v=2&ce343504-00e8-475b-85f6-7eed21f3183c",
#     "li_at": "AQEDAV5pkaMB3qPmAAABnPT0Q2sAAAGdGQDHa1YAxEmgmX7NC15rsGRPF5s_etvCHaOAHQuz-pFrBoOk5agvs3waZpKz68MzyTw309mJ4ZCbfSvgDpicwvPYOkD7ZaxvO5McPA9pnZ6-HeHEprpN49q-",
#     "JSESSIONID": "ajax:0854231741340664444",
#     "lidc": "b=OB67:s=O:r=O:a=O:p=O:g=4040:u=72:x=1:i=1773645357:t=1773731757:v=2:sig=AQGoD5CfmGyyttCEfwLsER2e20IgboSl",
# }

# HEADERS = {
#     "accept": "application/vnd.linkedin.normalized+json+2.1",
#     "accept-language": "en-US,en;q=0.9",
#     "csrf-token": "ajax:0854231741340664444",
#     "referer": f"https://www.linkedin.com/in/{VANITY_NAME}/",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
#     "x-li-lang": "en_US",
#     "x-restli-protocol-version": "2.0.0",
# }

# def fetch_profile():
#     url = "https://www.linkedin.com/voyager/api/identity/dash/profiles"
#     params = {
#         "q": "memberIdentity",
#         "memberIdentity": VANITY_NAME,
#         "decorationId": "com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-93",
#     }
#     r = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES)
#     if r.status_code != 200:
#         print(f"Error: {r.status_code}")
#         return None
#     return r.json()

# def extract_all(data):
#     included = data.get("included", [])
#     profile_info = {}
#     skills = []
#     experience = []
#     education = []

#     for item in included:
#         t = item.get("$type", "")

#         if t == "com.linkedin.voyager.dash.identity.profile.Profile":
#             profile_info["name"]     = f"{item.get('firstName','')} {item.get('lastName','')}".strip()
#             profile_info["headline"] = item.get("headline", "")
#             profile_info["about"]    = html.unescape(item.get("summary", "") or "")

#         if t == "com.linkedin.voyager.dash.common.Geo":
#             if "defaultLocalizedNameWithoutCountryName" in item:
#                 profile_info["location"] = item.get("defaultLocalizedName", "")

#         if t == "com.linkedin.voyager.dash.identity.profile.Skill":
#             name = item.get("name", "").strip()
#             if name:
#                 skills.append(name)

#         if t == "com.linkedin.voyager.dash.identity.profile.Position":
#             start = item.get("dateRange", {}).get("start", {})
#             end   = item.get("dateRange", {}).get("end", {})
#             months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
#                       7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
#             def fmt(d):
#                 if not d: return "Present"
#                 return f"{months.get(d.get('month',''), '')} {d.get('year','')}".strip()
#             experience.append({
#                 "title":       item.get("title", ""),
#                 "company":     item.get("companyName", ""),
#                 "location":    item.get("locationName", ""),
#                 "start":       fmt(start),
#                 "end":         fmt(end),
#                 "description": item.get("description", "") or "",
#             })

#         if t == "com.linkedin.voyager.dash.identity.profile.Education":
#             start = item.get("dateRange", {}).get("start", {})
#             end   = item.get("dateRange", {}).get("end", {})
#             education.append({
#                 "school":     item.get("schoolName", ""),
#                 "degree":     item.get("degreeName", ""),
#                 "field":      item.get("fieldOfStudy", ""),
#                 "grade":      item.get("grade", ""),
#                 "start_year": start.get("year", ""),
#                 "end_year":   end.get("year", ""),
#             })

#     return profile_info, skills, experience, education

# def main():
#     print("Fetching LinkedIn profile...")
#     data = fetch_profile()
#     if not data:
#         return

#     with open("basic_profile.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

#     profile_info, skills, experience, education = extract_all(data)

#     print("\n" + "="*60)
#     print("SURESH P - LinkedIn Profile")
#     print("="*60)
#     print(f"\nName     : {profile_info.get('name')}")
#     print(f"Headline : {profile_info.get('headline')}")
#     print(f"Location : {profile_info.get('location','')}")
#     print(f"\nAbout:\n{profile_info.get('about','')}")

#     print(f"\nSkills ({len(skills)}):")
#     for s in skills:
#         print(f"  - {s}")

#     print(f"\nExperience ({len(experience)}):")
#     for e in experience:
#         print(f"\n  {e['title']} @ {e['company']}")
#         print(f"  {e['start']} -> {e['end']} | {e['location']}")
#         if e['description']:
#             for line in e['description'].strip().split('\n'):
#                 print(f"    {line}")

#     print(f"\nEducation ({len(education)}):")
#     for ed in education:
#         print(f"\n  {ed['school']}")
#         print(f"  {ed['degree']} - {ed['field']}")
#         print(f"  {ed['start_year']} -> {ed['end_year']} | Grade: {ed['grade']}")

#     result = {"profile": profile_info, "skills": skills,
#               "experience": experience, "education": education}
#     with open("profile_extracted.json", "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2, ensure_ascii=False)
#     print("\nprofile_extracted.json saved!")

# if __name__ == "__main__":
#     main()  


# import requests
# import json
# import html
# import sys


# COOKIES = {
#     "bcookie": "v=2&ce343504-00e8-475b-85f6-7eed21f3183c",
#     "li_at": "AQEDAV5pkaMD_nikAAABnPZDFaIAAAGdGk-ZolYAxTleiWQFkY_u2Ad5235nO-gBnOvduq-SpiHF57zvCvWys1pO-MX9o4bmJNla0x2sKWCKHn1w9s0wwmWiZdjDWexsE0a1UQQubBQ4L8WEw_-zqiKZ",
#     "JSESSIONID": "ajax:0854231741340664444",
#     "lidc": "b=OB67:s=O:r=O:a=O:p=O:g=4040:u=72:x=1:i=1773645357:t=1773731757:v=2:sig=AQGoD5CfmGyyttCEfwLsER2e20IgboSl",
# }

# HEADERS = {
#     "accept": "application/vnd.linkedin.normalized+json+2.1",
#     "accept-language": "en-US,en;q=0.9",
#     "csrf-token": "ajax:0854231741340664444",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
#     "x-li-lang": "en_US",
#     "x-restli-protocol-version": "2.0.0",
# }

# MONTHS = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
#           7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

# def fmt_date(d):
#     if not d:
#         return "Present"
#     m = d.get("month", "")
#     y = d.get("year", "")
#     return f"{MONTHS.get(m,'')} {y}".strip()

# def fetch_profile(vanity_name):
#     HEADERS["referer"] = f"https://www.linkedin.com/in/{vanity_name}/"
#     url = "https://www.linkedin.com/voyager/api/identity/dash/profiles"
#     #to get full details   
#     params = {
#         "q": "memberIdentity",
#         "memberIdentity": vanity_name,
#         "decorationId": "com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-93",
#     }
#     r = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES)
#     print(f"Status: {r.status_code}")
#     if r.status_code != 200:
#         print(f"Error body: {r.text[:300]}")
#         return None
#     return r.json()

# def extract_all(data):
#     #   "included" key irundha → antha array edukurom
#     included = data.get("included", [])
#     profile_info = {}
#     skills = []
#     experience = []
#     education = []

#     for item in included:
#         t = item.get("$type", "")

#         # Profile
#         if t == "com.linkedin.voyager.dash.identity.profile.Profile":
#             profile_info["name"]     = f"{item.get('firstName','')} {item.get('lastName','')}".strip()
#             profile_info["headline"] = item.get("headline", "")
#             profile_info["about"]    = html.unescape(item.get("summary", "") or "")
#             profile_info["public_id"] = item.get("publicIdentifier", "")

#         # Location
#         if t == "com.linkedin.voyager.dash.common.Geo":
#             if "defaultLocalizedNameWithoutCountryName" in item:
#                 profile_info["location"] = item.get("defaultLocalizedName", "")

#         # Skills
#         if t == "com.linkedin.voyager.dash.identity.profile.Skill":
#             name = item.get("name", "").strip()
#             if name:
#                 skills.append(name)

#         # Experience
#         if t == "com.linkedin.voyager.dash.identity.profile.Position":
#             dr = item.get("dateRange", {}) or {}
#             experience.append({
#                 "title":       item.get("title", ""),
#                 "company":     item.get("companyName", ""),
#                 "location":    item.get("locationName", ""),
#                 "start":       fmt_date(dr.get("start")),
#                 "end":         fmt_date(dr.get("end")),
#                 "description": (item.get("description", "") or "").strip(),
#             })

#         # Education
#         if t == "com.linkedin.voyager.dash.identity.profile.Education":
#             dr = item.get("dateRange", {}) or {}
#             education.append({
#                 "school":     item.get("schoolName", ""),
#                 "degree":     item.get("degreeName", ""),
#                 "field":      item.get("fieldOfStudy", ""),
#                 "grade":      item.get("grade", ""),
#                 "start_year": (dr.get("start") or {}).get("year", ""),
#                 "end_year":   (dr.get("end")   or {}).get("year", ""),
#                 "description": (item.get("description", "") or "").strip(),
#             })

#     # Sort experience by start date (newest first)
#     experience.sort(key=lambda x: x["start"], reverse=True)

#     return profile_info, skills, experience, education

# def print_and_save(vanity_name, profile_info, skills, experience, education):
#     sep = "="*60

#     print(f"\n{sep}")
#     print(f"  LinkedIn Profile: {profile_info.get('name','')}")
#     print(sep)
#     print(f"\n  URL      : https://www.linkedin.com/in/{vanity_name}/")
#     print(f"  Headline : {profile_info.get('headline','')}")
#     print(f"  Location : {profile_info.get('location','')}")

#     about = profile_info.get("about","")
#     if about:
#         print(f"\n--- ABOUT ---")
#         print(about)

#     print(f"\n--- SKILLS ({len(skills)}) ---")
#     for s in skills:
#         print(f"  • {s}")

#     print(f"\n--- EXPERIENCE ({len(experience)}) ---")
#     for e in experience:
#         print(f"\n  {e['title']}  @  {e['company']}")
#         print(f"  {e['start']} → {e['end']}  |  {e['location']}")
#         if e["description"]:
#             for line in e["description"].split("\n"):
#                 if line.strip():
#                     print(f"    {line.strip()}")

#     print(f"\n--- EDUCATION ({len(education)}) ---")
#     for ed in education:
#         print(f"\n  {ed['school']}")
#         print(f"  {ed['degree']} — {ed['field']}")
#         yr = f"{ed['start_year']} → {ed['end_year']}"
#         if ed["grade"]:
#             yr += f"  |  Grade: {ed['grade']}"
#         print(f"  {yr}")
#         if ed["description"]:
#             print(f"  {ed['description']}")

#     print(f"\n{sep}\n")

#     # Save JSON
#     filename = f"{vanity_name}_profile.json"
#     result = {
#         "url": f"https://www.linkedin.com/in/{vanity_name}/",
#         "profile": profile_info,
#         "skills": skills,
#         "experience": experience,
#         "education": education,
#     }
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2, ensure_ascii=False)
#     print(f"Saved: {filename}")

# def main():
#     if len(sys.argv) > 1:
#         vanity_name = sys.argv[1].strip().strip("/")
#     else:
#         vanity_name = input("LinkedIn vanity name enter பண்ணு (e.g. p-suresh-webdev): ").strip().strip("/")
#         if not vanity_name:
#             vanity_name = "p-suresh-webdev"

#     print(f"\nFetching: {vanity_name} ...")
#     data = fetch_profile(vanity_name)
#     if not data:
#         return

#     profile_info, skills, experience, education = extract_all(data)
#     print_and_save(vanity_name, profile_info, skills, experience, education)

# if __name__ == "__main__":
#     main()


#multi profile scrap 


import requests
import json
import html
import sys
import time


COOKIES = {
    "bcookie": "v=2&ce343504-00e8-475b-85f6-7eed21f3183c",
    "li_at": "AQEDAV5pkaMD_nikAAABnPZDFaIAAAGdGk-ZolYAxTleiWQFkY_u2Ad5235nO-gBnOvduq-SpiHF57zvCvWys1pO-MX9o4bmJNla0x2sKWCKHn1w9s0wwmWiZdjDWexsE0a1UQQubBQ4L8WEw_-zqiKZ",
    "JSESSIONID": "ajax:0854231741340664444",
    "lidc": "b=OB67:s=O:r=O:a=O:p=O:g=4040:u=72:x=1:i=1773645357:t=1773731757:v=2:sig=AQGoD5CfmGyyttCEfwLsER2e20IgboSl",
}

HEADERS = {
    "accept": "application/vnd.linkedin.normalized+json+2.1",
    "accept-language": "en-US,en;q=0.9",
    "csrf-token": "ajax:0854231741340664444",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-li-lang": "en_US",
    "x-restli-protocol-version": "2.0.0",
}

MONTHS = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
          7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


def fmt_date(d):
    if not d:
        return "Present"
    m = d.get("month", "")
    y = d.get("year", "")
    return f"{MONTHS.get(m,'')} {y}".strip()

def fetch_profile(vanity_name):
    HEADERS["referer"] = f"https://www.linkedin.com/in/{vanity_name}/"
    url = "https://www.linkedin.com/voyager/api/identity/dash/profiles"
    params = {
        "q": "memberIdentity",
        "memberIdentity": vanity_name,
        "decorationId": "com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-93",
    }
    r = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES)
    if r.status_code != 200:
        return None, r.status_code
    return r.json(), 200

def extract_all(data):
    included = data.get("included", [])
    profile_info = {}
    skills = []
    experience = []
    education = []

    for item in included:
        t = item.get("$type", "")

        if t == "com.linkedin.voyager.dash.identity.profile.Profile":
            profile_info["name"]      = f"{item.get('firstName','')} {item.get('lastName','')}".strip()
            profile_info["headline"]  = item.get("headline", "")
            profile_info["about"]     = html.unescape(item.get("summary", "") or "")
            profile_info["public_id"] = item.get("publicIdentifier", "")

        if t == "com.linkedin.voyager.dash.common.Geo":
            if "defaultLocalizedNameWithoutCountryName" in item:
                profile_info["location"] = item.get("defaultLocalizedName", "")

        if t == "com.linkedin.voyager.dash.identity.profile.Skill":
            name = item.get("name", "").strip()
            if name:
                skills.append(name)

        if t == "com.linkedin.voyager.dash.identity.profile.Position":
            dr = item.get("dateRange", {}) or {}
            experience.append({
                "title":       item.get("title", ""),
                "company":     item.get("companyName", ""),
                "location":    item.get("locationName", ""),
                "start":       fmt_date(dr.get("start")),
                "end":         fmt_date(dr.get("end")),
                "description": (item.get("description", "") or "").strip(),
            })

        if t == "com.linkedin.voyager.dash.identity.profile.Education":
            dr = item.get("dateRange", {}) or {}
            education.append({
                "school":      item.get("schoolName", ""),
                "degree":      item.get("degreeName", ""),
                "field":       item.get("fieldOfStudy", ""),
                "grade":       item.get("grade", ""),
                "start_year":  (dr.get("start") or {}).get("year", ""),
                "end_year":    (dr.get("end")   or {}).get("year", ""),
                "description": (item.get("description", "") or "").strip(),
            })

    experience.sort(key=lambda x: x["start"], reverse=True)
    return profile_info, skills, experience, education


def bulk_scrape(txt_file, output_file, delay=3):
    # Step 1: txt file lendhu usernames read pannrom
    with open(txt_file, "r", encoding="utf-8") as f:
        usernames = [line.strip() for line in f if line.strip()]

    total = len(usernames)
    print(f"\nTotal profiles to scrape: {total}")
    print("="*60)

    all_profiles = []  
    failed = []         

    
    for i, vanity_name in enumerate(usernames, 1):
        print(f"\n[{i}/{total}] Fetching: {vanity_name} ...")

        
        data, status = fetch_profile(vanity_name)

        if data is None:
            print(f"   Failed — Status: {status}")
            failed.append({"username": vanity_name, "status": status})
        else:
          
            profile_info, skills, experience, education = extract_all(data)

            
            profile_data = {
                "url": f"https://www.linkedin.com/in/{vanity_name}/",
                "profile": profile_info,
                "skills": skills,
                "experience": experience,
                "education": education,
            }

            all_profiles.append(profile_data)
            print(f"   Success — {profile_info.get('name', 'Unknown')}")

      
        if i < total:
            print(f"  ⏳ Waiting {delay} seconds...")
            time.sleep(delay)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, indent=2, ensure_ascii=False)

    
    print("\n" + "="*60)
    print(f" Success : {len(all_profiles)}/{total}")
    print(f" Failed  : {len(failed)}/{total}")
    if failed:
        print("\nFailed profiles:")
        for f_item in failed:
            print(f"  • {f_item['username']} — Status: {f_item['status']}")
    print(f"\n📁 Saved: {output_file}")
    print("="*60)


if __name__ == "__main__":

    bulk_scrape(
        txt_file="profile.txt",
        output_file="all_profiles.json",
        delay=3          
    )