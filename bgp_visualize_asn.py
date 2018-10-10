__author__ = "Bassim Aly"
__EMAIL__ = "basim.alyy@gmail.com"
import json
import requests
from matplotlib import pyplot as plt
import networkx as nx
import os

# TODO Add support for the proxy
class asn_visualize(object):
    def __init__(self, asn, ):
        self.asn = int(asn)

    def get_ipv4_neighbors(self):
        HOST = "api.bgpview.io"
        RESOURCE = "asn"
        url = 'https://{0}/{1}/{2}/peers'.format(HOST,
                                                 RESOURCE,
                                                 self.asn
                                                 )
        headers = {'content-type': 'application/json'}
        neighbors_resp = requests.get(url,
                                      headers=headers,
                                      )

        ipv4_peers = json.loads(neighbors_resp.content)['data']['ipv4_peers']

        asn_peers = []
        for peer in ipv4_peers:
            asn_peers.append(peer['asn'])
        asn_peers.insert(0, self.asn)
        return asn_peers

    def get_asn_ups_and_downs(self, direction='upstreams'):
        ipv4_data = ["NO_IPv4_{0}_FOUND".format(direction)]
        ipv6_data = ["NO_IPv6_{0}_FOUND".format(direction)]
        HOST = "api.bgpview.io"
        RESOURCE = direction
        url = "https://{0}/asn/{2}/{1}".format(HOST, RESOURCE, self.asn)
        headers = {'content-type': 'application/json'}
        direction_resp = requests.get(url,
                                      headers=headers)

        try:
            ipv4_data = json.loads(direction_resp.content)['data']['ipv4_' + direction]
        except:
            pass
        try:
            ipv6_data = json.loads(direction_resp.content)['data']['ipv6_' + direction]
        except:
            pass

        try:
            for index, x in enumerate(ipv4_data):
                del ipv4_data[index]['bgp_paths']
                del ipv4_data[index]['description']
                del ipv4_data[index]['country_code']
                del ipv4_data[index]['name']
        except:
            pass

        ipv4_data = [x.values()[0] for x in ipv4_data]
        try:
            for index, x in enumerate(ipv6_data):
                del ipv6_data[index]['bgp_paths']
                del ipv6_data[index]['description']
                del ipv6_data[index]['country_code']
                del ipv6_data[index]['name']
        except:
            pass
        # TODO Support IPv6 Peers
        return ipv4_data


class bgp_visualize(object):
    def __init__(self, country="", asns=[], adjacency_num=14,
                 u_color='#009999',
                 d_color='#ED9236',
                 default_color='#999999',
                 operator_node_size=800,
                 save_asn="",
                 dark = False,
                 ):
        self.country = country
        self.asns = asns
        self.adjacency_num = int(adjacency_num)
        self.u_color = str(u_color)
        self.d_color = str(d_color)
        self.default_color = str(default_color)
        self.operator_node_size = int(operator_node_size)
        self.save_asn = save_asn
        self.dark = dark


    def get_country_data(self):
        HOST_RIPE = "stat.ripe.net/"
        RESOURCE = "/data/country-resource-list/data.json"
        PARAMS = {'resource': self.country}
        url = 'https://{0}/{1}/'.format(HOST_RIPE, RESOURCE, )
        headers = {'content-type': 'application/json'}
        asns_in_country = requests.get(url,
                                       headers=headers,
                                       params=PARAMS
                                       )

        return json.loads(asns_in_country.content)['data']['resources']['asn']

    def Draw(self):
        country_codes = {
            'EGYPT': 'eg',
            'KSA': 'sa',
            'UAE': 'ae',
            'TURKEY': 'tr',
            'LEBNON': 'lb',
            'JORDON': 'jo',
            'SWEDEN': 'se',
            'QATER': 'qa',
            'IRELAND': 'ie',
            'Singapore': 'sg',
            'South Africa': 'za',
            'GERMANY': 'de'
        }

        # http://www.worldstandards.eu/other/tlds/

        G = nx.Graph()

        if self.country != "":
            self.txt = self.country
            # TODO Add Threading for faster processing
            country_data = self.get_country_data()
            Total_ASN_Nums = len(country_data)
            print "Total ASNs in {0} are {1}".format(self.country.upper(), Total_ASN_Nums)
            print "================================================"
            for asn in country_data:
                print "adding peers for AS #{0} in {1}".format(asn, self.country.upper())
                asn_neig_object = asn_visualize(asn=asn)
                asn_neig_object_neighbors = asn_neig_object.get_ipv4_neighbors()
                G.add_star(asn_neig_object_neighbors)

            print "================================================"
            print "Getting The Operators ASN in {0}".format(self.country.upper())

        elif self.asns:
            Total_ASN_Nums = len(self.asns)
            self.txt = "_".join([str(x) for x in self.asns])
            for asn in self.asns:
                asn_neig_object = asn_visualize(asn=asn)
                asn_neig_object_neighbors = asn_neig_object.get_ipv4_neighbors()
                G.add_star(asn_neig_object_neighbors)
        candidates = []
        operators = []
        for x, v in G.edges():
            candidates.append(x)
            candidates.append(v)

        for x in candidates:
            if candidates.count(x) > self.adjacency_num:
                operators.append(x)
        operators_asn = set(operators)

        val_color_map = {}
        val_size_map = {}

        for asn in operators_asn:
            asn_upstream = asn_visualize(asn=asn).get_asn_ups_and_downs(direction='upstreams')
            asn_downstream = asn_visualize(asn=asn).get_asn_ups_and_downs(direction='downstreams')
            for upstream in asn_upstream:
                val_color_map[upstream] = self.u_color.upper()

            for downstream in asn_downstream:
                val_color_map[downstream] = self.d_color.upper()

        operators_colors = ['#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#996633',
                            '#004D99',
                            '#00CC99',
                            '#E6E600',
                            '#669999',
                            '#996633',
                            '#FF0000',
                            '#00CC99',
                            '#EE5D9A',
                            '#009933',
                            '#FF0000',
                            '#996633',
                            '#E6E600',
                            '#004D99',
                            '#A525D6',
                            '#009933',
                            '#FF0000',
                            '#3729DC',
                            '#EE5D9A',
                            '#009933',
                            ]

        for index, operator in enumerate(operators_asn):
            val_color_map[operator] = operators_colors[index]
            val_size_map[operator] = self.operator_node_size

        print "================================================"
        print "Visualizing {0} Connections Between {1} ASNs....".format(len(G.edges()), Total_ASN_Nums)

        fig1 = plt.figure(1)
        color = '#000000'
        edge_cmap = plt.cm.ocean
        if self.dark:
            fig1.patch.set_facecolor('black')
            color = '#CCCCCC'
            edge_cmap = plt.cm.ocean
            self.default_color = '#EEEEEE'

        size_values = [val_size_map.get(node, (self.operator_node_size - 300)) for node in G.nodes()]
        color_values = [val_color_map.get(node, self.default_color.upper()) for node in G.nodes()]
        edge_colors = range(len(G.edges()))
        layout = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos=layout, node_size=size_values, node_color=color_values, )
        nx.draw_networkx_edges(G, pos=layout, alpha=0.2, width=2, edge_color=edge_colors, edge_cmap=edge_cmap)
        nx.draw_networkx_labels(G, pos=layout, font_size=6)
        plt.axis("off")
        fig1.subplots_adjust(left=0, right=1.0, bottom=0, top=0.94)
        # fig1.style.use('dark_background')

        plt.title("Visualize AS Connections for {0}".format(self.txt) , color=color)

        if self.save_asn != "":
            print "================================================"
            print "Writing Data to {0} ".format(self.save_asn)

            # TODO savefig doesnt read the facecolor of the plot when saving
            plt.savefig(os.path.join(self.save_asn, '{0}_asns.png' ) .format(self.txt))
            with open(os.path.join(self.save_asn, "{0}_asns.txt").format(self.txt), 'w') as asns:
                if self.country != "":
                    asns.write("\n".join(country_data))

        plt.show()


