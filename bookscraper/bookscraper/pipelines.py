# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        #replace space by underscore in name
        adapter =ItemAdapter(item)
        value=adapter.get('name')
        adapter['name']=value.replace(' ','_')

        #convert values to lowercase
        tolower=['Genre','Product_Type']
        for lower in tolower:
            value=adapter.get(lower)
            adapter[lower]=value.lower()
        
        #remove currency sign
        value=adapter.get('Price')
        adapter['Price']= float(value.replace('£',''))
        
        #availability to integer
        value=adapter.get('Availability')
        value=value.split('(')
        if len(value)<2:
            adapter['Availability']=0
        else:
            value=value[1].split(' ')
            adapter['Availability']=int(value[0])
        
        #reviews to int
        value=adapter.get('Rating')
        value=value.split(' ')
        value=value[1].lower()
        if value=='zero':
            adapter['Rating']=0
        elif value=='one':
            adapter['Rating']=1
        elif value=='two':
            adapter['Rating']=2
        elif value=='three':
            adapter['Rating']=3
        elif value=='four':
            adapter['Rating']=4
        else:
            adapter['Rating']=5
 
        return item
