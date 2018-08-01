import requests
import re

def testInsert():
    requests.post("http://localhost:7990/insert",
                
                    json={
                        "verified":"TERMXX",
                        "verified_plaintext":"Tester2 inserted by new API.",
                        "alpha_order":"Tester1 inderted aplha_order.",
                        "category":"PEopLE",
                        "verified_alternates":None,
                        "verification_source":None,
                        "description":"<b>The testing item 2 inserted by REQUEST and POST method",
                        "description_plaintext":"The testing item inserted by REQUEST and POST method",
                        "comments":None,
                        "relationship":"JACK's son",
                        "location":None,
                        "created_time":"2025-02-02",
                        "created_by":"Tom",
                        "modified_time":None,
                        "modified_by":None,
                        "revised_time":None

                        
                    }
                )

def testGet():
    requests.get("http://localhost:7990/get?87701")

def testDelete():
    requests.get("http://localhost:7990/get?87701")


def testUpdate():
    requests.post( "http://localhost:7990/update",
                json={
                    "id":87699,
                        "verified":"<b>Tester2 UPDATED by new API.</b>",
                        "verified_plaintext":"Tester2 inserted by new API.",
                        "alpha_order":"Tester1 inderted aplha_order.",
                        "category_id":4,
                        "verified_alternates":None,
                        "verification_source":None,
                        "description":"UPDATED method",
                        "description_plaintext":"The testing item UPDATE by REQUEST and POST method",
                        "comments":None,
                        "relationship":"Norm's son",
                        "location":None,
                        "created_time":"2025-02-02",
                        "created_by":"Tom",
                        "modified_time":None,
                        "modified_by":None,
                        "revised_time":None
                    }
        
        )
def processSearch():
    originalSearch = "?the searching string"
    if originalSearch[0]=="?":
        w = originalSearch[1:].split()
        print(w)

if __name__ == '__main__':
    processSearch()