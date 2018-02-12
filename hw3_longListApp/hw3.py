import csv

infile = open("movienews.txt", 'r')
data = infile.read().split('\n')

month = {
    'January' : '1',
    'February' : '2',
    'March' : '3',
    'April' : '4',
    'May' : '5',
    'June' : '6',
    'July' : '7',
    'August' : '8',
    'September' : '9',
    'October' : '10',
    'November' : '11',
    'December' : '12'
}

csvfile = open("moviecalendar.csv", 'w', newline = '')
fieldnames = ['Subject', 'Start Date', 'All Day Event', 'Start Time', 'End Time', 'Location', 'Description']
writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
writer.writeheader()

for i in range(0, len(data)-3, 3):
    date = data[i+2].split(' ')
    date[0] = month[date[0]]
    date[1] = date[1].replace(',', '')

    writer.writerow({
        'Subject': data[i],
        'Start Date': date[0]+'/'+date[1]+'/'+date[2],
        'All Day Event' : "FALSE",
        'Start Time' : date[3] + " " + date[4].upper(), 
        'Description': data[i+1],
    })

print(date[0]+'/'+date[1]+'/'+date[2])
