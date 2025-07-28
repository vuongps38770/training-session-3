import networkx as nx
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

class Node:
    """
    Represents a node in the map
    """
    def __init__(self, node_id: int, x: float, y: float, node_type: str = "NORMAL"):
        self.id = node_id
        self.x = x
        self.y = y
        self.type = node_type
    
    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def get_color(self) -> str:
        """Get node color based on type"""
        return 'lightblue' if self.type == 'NORMAL' else 'lightgreen'

class Edge:
    """
    Represents an edge in the map
    """
    def __init__(self, edge_id: str, source: int, target: int, label: str):
        self.id = edge_id
        self.source = source
        self.target = target
        self.label = label
        self.weight = float(1.0)

class Map:
    """
    Represents a map with nodes and edges
    """
    def __init__(self, map_data: Dict):
        self.id = map_data['id']
        self.name = map_data['name']
        self.map_type = map_data['mapType']
        self.dimensions = map_data['dimensions']
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Edge] = []
        
        self._load_nodes(map_data.get('nodes', []))
        self._load_edges(map_data.get('edges', []))
    
    def _load_nodes(self, nodes_data: List[Dict]):
        """Load nodes from raw data"""
        for node_data in nodes_data:
            node = Node(
                node_id=node_data['id'],
                x=node_data['x'],
                y=node_data['y'],
                node_type=node_data['type']
            )
            self.nodes[node.id] = node
    
    def _load_edges(self, edges_data: List[Dict]):
        """Load edges from raw data"""
        for edge_data in edges_data:
            edge = Edge(
                edge_id=edge_data['id'],
                source=edge_data['source'],
                target=edge_data['target'],
                label=edge_data['label']
            )
            self.edges.append(edge)
    
    def to_networkx_graph(self) -> nx.DiGraph:
        """Convert map to NetworkX directed graph"""
        G = nx.DiGraph()
        
        # Add nodes
        for node_id, node in self.nodes.items():
            G.add_node(node_id, x=node.x, y=node.y, type=node.type)
        
        # Add edges
        for edge in self.edges:
            G.add_edge(edge.source, edge.target, weight=edge.weight, label=edge.label)
        
        return G
    
    def get_node_positions(self) -> Dict[int, Tuple[float, float]]:
        """Get positions of all nodes"""
        return {node_id: node.position for node_id, node in self.nodes.items()}
    
    def get_metadata_text(self) -> str:
        """Get formatted metadata text"""
        return (f"Map ID: {self.id[:8]}...\n"
                f"Nodes: {len(self.nodes)}\n"
                f"Edges: {len(self.edges)}\n"
                f"Dimensions: {self.dimensions['width']}x{self.dimensions['height']}")
    
    def print_graph_info(self, console: Console):
        """Print graph information using Rich"""
        # Create main panel
        panel = Panel(
            f"[bold cyan]{self.name}[/bold cyan]\n"
            f"Type: {self.map_type}\n"
            f"ID: {self.id[:16]}...",
            title="[bold magenta]Map Information[/bold magenta]",
            expand=False
        )
        console.print(panel)
        
        # Create statistics table
        stats_table = Table(title="Graph Statistics", show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Nodes", str(len(self.nodes)))
        stats_table.add_row("Total Edges", str(len(self.edges)))
        stats_table.add_row("Map Width", str(self.dimensions['width']))
        stats_table.add_row("Map Height", str(self.dimensions['height']))
        
        # Count node types
        node_types = {}
        for node in self.nodes.values():
            node_types[node.type] = node_types.get(node.type, 0) + 1
        
        for node_type, count in node_types.items():
            stats_table.add_row(f"{node_type} Nodes", str(count))
        
        console.print(stats_table)
        
        # Create edges tree
        if self.edges:
            tree = Tree("[bold yellow]Graph Edges[/bold yellow]")
            
            # Group edges by source node
            edges_by_source = {}
            for edge in self.edges:
                if edge.source not in edges_by_source:
                    edges_by_source[edge.source] = []
                edges_by_source[edge.source].append(edge)
            
            # Add to tree
            for source, edges in sorted(edges_by_source.items()):
                source_branch = tree.add(f"[cyan]Node {source}[/cyan]")
                for edge in edges:
                    source_branch.add(
                        f"→ [green]Node {edge.target}[/green] "
                        f"(weight: [yellow]{edge.weight}[/yellow])"
                    )
            
            console.print(tree)
