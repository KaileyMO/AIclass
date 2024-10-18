import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

#scrapes website
def scrape_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #goes through content from the link and finds the links to the datasets
    data = []
    for section in soup.find_all('li', class_='dataset-item has-organization'):
        link = section.find('a')['href']
        data.append({'Link' : link})
    return data

#download csv files
def download(csvData1, csvData2):
    # Gets response/data from the data downloads
    response1 = requests.get(csvData1)
    response2 = requests.get(csvData2)

    # writes data to csv file. creates/rewrites it depending on if it exists
    with open('data1.csv', 'wb') as file1:
        file1.write(response1.content)
    with open('data2.csv', 'wb') as file2:
        file2.write(response2.content)

# plot data
def plotting(x, y, xlabel, ylabel, title, typePlot):
    if typePlot == 'scatter':
        # Create a scatter plot
        plt.scatter(x, y, color='blue', zorder=2)
    elif typePlot == 'bar':
        # Create a bar chart
        plt.bar(x, y, color='red', width=0.4, zorder=2)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(zorder=1)
    plt.show()

# Goes through 4 angles of data analysis. Total of 4 graphs
def angles():
    file1 = pd.read_csv('data1.csv', usecols=['Electric Range', 'Model Year', 'Base MSRP'])
    file2 = pd.read_csv('data2.csv', usecols=['Vict Age', 'Vict Sex', 'Vict Descent'])

    carx = file1['Model Year']
    car_xlabel = 'Model Year'
    cary = file1['Electric Range']
    car_ylabel = 'Electric Range'
    carTitle = 'Electronic Range for Model Year'

    # Plots based on electric vehicle population. Graphs on the electric range of model year.
    plotting(carx, cary, car_xlabel, car_ylabel, carTitle, 'scatter')
    

    msrpx = file1['Base MSRP']
    msrp_xlabel = 'Base MSRP'
    msrpy = file1['Electric Range']
    msrp_ylabel = 'Electric Range'
    msrpTitle = 'Base MSRP vs. Electric Range'

    # Create a scatter plot for Electric Range vs. Base MSRP
    plotting(msrpx, msrpy, msrp_xlabel, msrp_ylabel, msrpTitle, 'scatter')


    # Simplify data for bar graph
    sexNum = file2['Vict Sex'].value_counts()
    genders = ['Male', 'Female']
    genderNum = [sexNum.get("M"), sexNum.get("F")]

    genderx = genders
    gender_xlabel = 'Sex'
    gendery = genderNum
    gender_ylabel = 'Victim Count'
    genderTitle = 'Male and Female Crime Victims'

    # Plots crime statistics based on gender. Males are slightly higher but relatively equal.
    plotting(genderx, gendery, gender_xlabel, gender_ylabel, genderTitle, 'bar')

    
    ''' Descent Code: A - Other Asian B - Black C - Chinese D - Cambodian F - Filipino G - Guamanian H - Hispanic/Latin/Mexican
        I - American Indian/Alaskan Native J - Japanese K - Korean L - Laotian O - Other P - Pacific Islander S - Samoan U - Hawaiian
        V - Vietnamese W - White X - Unknown Z - Asian Indian '''
    age_desc_num = file2.groupby(['Vict Age', 'Vict Descent']).size().unstack(fill_value=0).drop(0) #take away the .drop(0) to get an extreme variable

    # Plots bar graph to organize crime stats based on age and descent of victim
    age_desc_num.plot(kind='bar', stacked=True, color=['blue', 'orange', 'green', 'red',
                                                             'yellow', 'indigo', 'pink', 'darkgoldenrod',
                                                             'darkgray', 'gold', 'magenta', 'purple',
                                                             'gray', 'darkolivegreen', 'cyan', 'brown', 'midnightblue',
                                                             'saddlebrown', 'violet', 'teal'])

    plt.xlabel('Victim Ages')
    plt.ylabel('Number of Victims')
    plt.title('Victims by Age and Descent')

    # Plots crime statistics based on age and descent. Top three in order seem to be: Hispanics, Whites, Blacks.
    plt.show()


#runs everything together
url = 'https://catalog.data.gov'
links_list = scrape_site(url)

# Goes through and finds the link of the downloadable csv data files (first two)
csvLinks = []
for i in range(2):
    scraped_url = f"{url}{links_list[i]['Link']}"
    response = requests.get(scraped_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Searches through buttons to find correct .csv downloadable links. Stops searching after 2 csvs have been found
    for section in soup.find_all('div', class_='btn-group'):
        a_point = section.find('a', class_='btn btn-primary', href=True)
        if a_point and 'csv' in a_point['href']:
            csv_link = a_point['href']
            csvLinks.append(csv_link)
            
# Calls functions to download and analyze the data
download(csvLinks[0], csvLinks[1])
angles()
