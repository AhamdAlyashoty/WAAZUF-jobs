import requests
from bs4 import BeautifulSoup
import csv

job_details = []
page_num = 0
while True :
    page = requests.get(f"https://wuzzuf.net/search/jobs?q=&start={page_num}")
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    all_jobs = (soup.find_all("div" , {'class' : 'css-1gatmva e1v1l3u10'}))

    #print(all_jobs[0].h2.text)
    #print(len(all_jobs))

    for i in range(len(all_jobs)) :

        # job title
        job_title = all_jobs[i].find("h2" , {'class' : 'css-m604qf'}).text.strip()

        #links for each job
        link = all_jobs[i].find("h2" , {'class' : 'css-m604qf'}).a.attrs['href']
        page1 = requests.get(link)
        src1 = page1.content
        soup1 = BeautifulSoup(src1 , 'lxml')
        #salary
        #salary = soup1.find("section" , {'class' : 'css-3kx5e2'}).h2.contents[1].text.strip()
        #*******the is a problem that always display the content of the link is empty*********#
        salary = soup1.find("section" , {'class' : 'css-3kx5e2'})

        #company name
        company_name = all_jobs[i].find("a" , {'class' : 'css-17s97q8'}).text.strip()

        #location
        location = all_jobs[i].find("span" , {'class' : 'css-5wys0k'}).text.strip()

        #job skills
        job_skills = ""
        skills = all_jobs[i].find_all("div" , {'class' : 'css-y4udm8'})
        for j in range(len(skills)) :
            job_skills += skills[j].text.strip() + " "
        
        #add information
        job_details.append({'Job Title' : job_title , 'Company Name' : company_name , 'Location' : location , 'Job Skills' : job_skills , 'Salary' : salary})
    
    page_limit = int(soup.find("strong").text)
    if(page_num > page_limit // 15) :
        break

    page_num += 1
    
    print("page switched")

keys = job_details[0].keys()
with open ("job_details.csv" , 'w') as file :
    wr = csv.DictWriter(file , keys)
    wr.writeheader()
    wr.writerows(job_details)
    print("file created")
    #**********************************************************************************************#
