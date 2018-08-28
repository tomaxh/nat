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
                        "id":87821,
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
    k = ["brand names","events & awards","people","--mlas & elected officials","--government & legislature & statutory officers employees","--fictional personal names & nicknames","--parliamentary officials & statutory officers","--first nations and indigenous peoples leaders & officials & councillors & elders","style","programs & initiatives","works","--reports & studies","--accords & charters & conventions & declarations","--legislation","places","--resource infrastructure","--cities & towns","--physical infrastructure","--parks","--fictional place names & nicknames","organizations","--first nations and indigenous peoples organizations","--post-secondary organizations","--federal & other jurisdictions","--health sector organizations","--k-12 organizations","--crown corporations & government agencies","--unions","--local governments & regional districts","--ministries","modes of transport","non-english words & phrases","--first nations and indigenous peoples words & phrases","miscellaneous","specialized terms and jargon"]
    print(sorted(k))

