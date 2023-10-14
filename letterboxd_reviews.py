from bs4 import BeautifulSoup
import requests 
import csv

def scrape_reviews():
    with open('burning_reviews.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Rating', 'User', 'Review'])
        
        for i in range(9):
            if i == 0:
                html_text = requests.get('https://letterboxd.com/film/burning-2018/reviews/by/activity/').text
            else:
                html_text = requests.get(f"https://letterboxd.com/film/burning-2018/reviews/by/activity/page/{i+1}/").text 
                print(i+1)
                
            soup = BeautifulSoup(html_text, 'lxml')
            reviews = soup.find_all('li', class_='film-detail')
            next_page = soup.find('a', class_="next")['href']
                
            for idx, review in enumerate(reviews):
                metadata = review.div.find('div', class_='attribution-block').text.strip().split(' ')
                rating = metadata[0]
                if len(metadata) > 9:
                    if metadata[8] != '':
                        username = metadata[7] + ' ' + metadata[8]
                        date = conc_list(metadata[10:13])
                    else:
                        username = metadata[7]
                        date = conc_list(metadata[9:12])
                
                review_content = review.div.find('div', class_='body-text -prose collapsible-text').p.text  
                # print(f"{idx}. {review_content}\n")
                # print(rating, username, date)
                writer.writerow([date, rating, username, review_content])
                print(f"row {idx} written")

def conc_list(list):
    output = ""
    for element in list:
        output += " " + element 
    return output 

if __name__ == '__main__':
    scrape_reviews()
