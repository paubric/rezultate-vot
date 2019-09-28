import scrapy
from scrapy import Item, Field
from scrapy.loader import ItemLoader
import json
import re


class ElectionData(Item):
    year = Field()
    type = Field()
    partial = Field()
    url = Field()
    id = Field()
    general_election_data = Field()

class GeneralElectionData(Item):
    precincts = Field()
    mandates = Field()
    enrolled_citizens = Field()
    voting_citizens = Field()
    valid_votes = Field()
    null_votes = Field()


class ElectionDataSpider(scrapy.Spider):
    name = 'AEPSpider'
    start_urls = [
        'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_posts.php?qType=post']

    def parse(self, response):
        data = json.loads(response.body)

        for election in data:
            election_data_loader = ItemLoader(item=ElectionData())
            election_data_loader.add_value('year', election['alegeriDate'])
            election_data_loader.add_value('type', election['category'])
            election_data_loader.add_value('partial', election['isPartial'])
            election_data_loader.add_value('id', election['alegeriId'])
            election_data_loader.add_value('url', election['permalink'])
            election = election_data_loader.load_item()

            id = str(election['id'][0])
            type = election['type'][0]

            year = [e for e in re.split(r'[/-]', election['year'][0]) if len(e) == 4]
            election['year'] = year

            if type == 'europarlamentare':
                general_data_url = 'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_data.php?name=v1_euro_Tara_Sumar&parameter=' + id
            elif type == 'locale':
                general_data_url = 'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_data.php?name=v1_local_National_Sumar&parameter=' + id + '&parameter=3'
            elif type == 'referendum':
                general_data_url = 'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_data.php?name=v1_ref_National_Sumar&parameter=' + id
            elif type == 'prezidentiale':
                general_data_url = 'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_data.php?name=v1_prez_Tara_Sumar&parameter=' + id
            else:
                general_data_url = 'http://alegeri.roaep.ro/wp-content/plugins/aep/aep_data.php?name=v1_parl_Tara_Sumar&parameter=' + id + '&parameter=5'

            yield scrapy.Request(general_data_url, callback=self.parse_general_election_data, meta={'election': election})

    def parse_general_election_data(self, response):
        complete_general_election_data = []
        data = json.loads(response.body)

        for tour in data:
            general_election_data_loader = ItemLoader(
                item=GeneralElectionData())
            general_election_data_loader.add_value(
                'enrolled_citizens', tour['TotalInscrisi'])
            general_election_data_loader.add_value(
                'voting_citizens', tour['TotalPrezenti'])
            general_election_data_loader.add_value(
                'valid_votes', tour['TotalVoturiValabile'])
            general_election_data_loader.add_value(
                'null_votes', tour['TotalVoturiNule'])
            complete_general_election_data += [
                general_election_data_loader.load_item()]

        election = response.meta['election']
        election['general_election_data'] = complete_general_election_data

        print(election)

        yield {'election': election}
