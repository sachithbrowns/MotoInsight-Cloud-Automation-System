import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = 'https://ikman.lk/en/ads/sri-lanka/motorbikes-scooters'
response = requests.get(url)
print(response.text)  # Shows the HTML content of the page

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())  # Displays a formatted version of the HTML

# Extract the first 5 motorbike data
motorbikes_data = []

# Find all the motorbike listings (li elements with class 'normal--2QYVk')
motorbike_elements = soup.find_all('li', class_='normal--2QYVk')[:5]

for motorbike in motorbike_elements:
    title = motorbike.find('h2', class_='heading--2eONR').text if motorbike.find('h2', class_='heading--2eONR') else 'N/A'
    kilometers = motorbike.find_all('div')[1].text if len(motorbike.find_all('div')) > 1 else 'N/A'
    location_category = motorbike.find('div', class_='description--2-ez3').text if motorbike.find('div', class_='description--2-ez3') else 'N/A'
    price = motorbike.find('div', class_='price--3SnqI').span.text if motorbike.find('div', class_='price--3SnqI') else 'N/A'
    image_url = motorbike.find('img')['src'] if motorbike.find('img') else 'N/A'
    link = "https://ikman.lk" + motorbike.find('a', class_='card-link--3ssYv')['href'] if motorbike.find('a', class_='card-link--3ssYv') else 'N/A'

    motorbikes_data.append({
        'Title': title,
        'Kilometers': kilometers,
        'Location & Category': location_category,
        'Price': price,
        'Image URL': image_url,
        'Link': link
    })

# Convert the data into a DataFrame
df = pd.DataFrame(motorbikes_data)

# Save the data to an Excel file
df.to_excel('top_5_motorbikes.xlsx', index=False)

print("Data has been saved to 'top_5_motorbikes.xlsx'")
print(df)

