from bs4 import BeautifulSoup
import requests
import random


scrap_url='https://azure.microsoft.com/en-in/updates'

## Get the user info and author id from LinkedIn API
def user_info(headers):
    
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
     
    user_info = response.json()
    return user_info['id']

## Post content to linkedIn
def postMessage(message,user_access_id):
    
    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    author = f'urn:li:person:{user_access_id}'
    
    post_data = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": str(random.randint(1,100))+message[:2900]+"\n #latestupdates"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    r=requests.post(api_url, headers=headers, json=post_data)
    
    return r.json()
    

## Get the scarpping data
def getScrapingData(scrap_url):
    source_data=requests.get(scrap_url).text
    html=BeautifulSoup(source_data,features="lxml")
    string='\nMicrosoft Azure Latset Updates:\n\n'
    
    
    for i in html.findAll(True,{'class':['row update-row row-size6','row update-row row-divided row-size2']}):

        date_published=i.find('div',class_='column medium-1')
        if(date_published):
            #print(date_published.text.strip())
            string+=(date_published.text.strip()+'\n')


        heading=i.find('div',class_='column medium-11')
        if(heading):
            #print(heading.h3.a.text)
            string+=(heading.h3.a.text+'\n')


        avail=i.find('span',class_='status-indicator__label')
        if(avail):
            #print(avail.text)
            string+=(avail.text+'\n')


        paras=i.find('div',class_='column medium-11').find_all('p')
        for j in paras:
            l1=[]
            #print(j.text.strip())
            l1.append(j.text.strip())
        string+=('\n'.join(l1))
        string+=('\n')

        tags=i.find('div',class_='column medium-11').find("ul")
        if(tags):
            string+=('Tags: '+', '.join(list(tags.descendants)[2::3]))


        string+=('\n\n')
        #data.append(l)

    
    return string
    


# access token for LinkedIn API
    
access_token='AQUV0RIWd9Bhf4E040vKUmUy7B43oiB7peWeVdncah0reFiOv4OENqkkkjx3GPt2GJcv2KuUErl3ufhV-eHrTLF0D9-MRvQJCmM6nQHEldZc_sOIct65wqvmSB_DUWt2GRUaILQQzurICO0niNpG34j1UaTlrWKj4mCI6l2CMS6g3fddJ0gAPCNbM25s2yRkwBpKhn7oed0j-jdOYbDGjbebZKV1v7hkJ1cPxpade3xgaBu9kh6zJ2gebv7JCyIi60WK4UdfCY99i82q2rS4lVcjF2NoyMwWY0dEy4KVN5L7mjRprE54qz_d6ciMxyaQLQhnJdHkNyL4PtcNuIajSE2lmiaHPg'

headers = {'Content-Type': 'application/json',
           'Authorization':'Bearer {}'.format(access_token),
           'X-Restli-Protocol-Version':'2.0.0'
          }
s
user_access_id = user_info(headers)
scrap_data=getScrapingData(scrap_url)
result=postMessage(scrap_data,user_access_id)
print(result)







