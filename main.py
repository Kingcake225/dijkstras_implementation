import networkx as nx
import osmnx as ox
import folium
import config # Import later
# Contains API key for Position Stack - converts an address to long and lat coords.
# config.PS_apiKey to call

class Map:
    def __init__(self, start_coords, end_coords): # Start coords must be given at tuple
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.network = ox.graph_from_point(start_coords, dist=1000, network_type='drive') # dist is buffer distance

    def findNearestNode(self):
        orig_node = ox.distance.nearest_nodes(self.network, self.start_coords[1], self.start_coords[0])
        dest_node = ox.distance.nearest_nodes(self.network, self.end_coords[1], self.end_coords[0])
        return orig_node, dest_node

    def generate_shortest_map(self, orig_node, dest_node):

        shortest_path = nx.shortest_path(self.network, orig_node, dest_node, weight='length') # Replace nx.shortest_path with own implementation of Dijkstra

        m = folium.Map(location=self.start_coords, zoom_start=15)

        route_coords = [(self.network.nodes[node]['y'], self.network.nodes[node]['x']) for node in shortest_path]

        folium.PolyLine(route_coords, color='blue', weight=5).add_to(m)

        folium.Marker(
            location=self.start_coords,
            popup='Start',
            icon=folium.Icon(color='green')
        ).add_to(m)

        folium.Marker(
            location=self.end_coords,
            popup='End',
            icon=folium.Icon(color='red')
        ).add_to(m)

        m.save("shortest_path_map.html")


# Origin location and destination
start_coords = (51.45898602638651, -2.6188274814116506) # CHS
end_coords = (51.45481197860214, -2.609414437680666) # QEH

Map1 = Map(start_coords, end_coords)
orig_node, dest_node = Map1.findNearestNode()
Map1.generate_shortest_map(orig_node, dest_node)