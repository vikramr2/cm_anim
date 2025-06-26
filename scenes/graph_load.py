from manimlib import *
import pandas as pd
import networkx as nx
import numpy as np

class TSVToGraphAnimation(Scene):
    def construct(self):
        # Load your TSV file (replace with your actual file path)
        tsv_file = "data/interactome/interactome.tsv"  # Use the instance variable
        

        df = pd.read_csv(tsv_file, sep='\t', header=None)
        edges = df.values.tolist()
        
        # Create text representation of the TSV data
        tsv_lines = []
        for i, edge in enumerate(edges[:10]):  # Show first 10 edges
            line_text = f"{edge[0]}\t{edge[1]}"
            text_obj = Text(line_text, font_size=24)
            text_obj.shift(UP * (4 - i * 0.8))
            tsv_lines.append(text_obj)
        
        # Add "..." if there are more edges
        if len(edges) > 10:
            dots = Text("...", font_size=24)
            dots.shift(UP * (4 - 10 * 0.8))
            tsv_lines.append(dots)
        
        # Group all TSV lines
        tsv_group = VGroup(*tsv_lines)
        
        # Animation 1: Scroll through the TSV data
        self.play(Write(tsv_group), run_time=3)
        self.wait(1)
        
        # Animation 2: Scrunch up the data
        scrunched_rect = Rectangle(width=1, height=0.5, color=BLUE)
        scrunched_rect.shift(DOWN * 2)
        
        self.play(
            Transform(tsv_group, scrunched_rect),
            run_time=2
        )
        self.wait(0.5)
        
        # Animation 3: Create the graph visualization
        # Build NetworkX graph from edges
        G = nx.Graph()
        for edge in edges:
            G.add_edge(str(edge[0]), str(edge[1]))
        
        # Position nodes using spring layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Scale positions for manim
        scale_factor = 3
        node_positions = {}
        for node, (x, y) in pos.items():
            node_positions[node] = np.array([x * scale_factor, y * scale_factor, 0])
        
        # Create graph elements
        graph_nodes = {}
        graph_edges = []
        
        # Create nodes
        for node, position in node_positions.items():
            circle = Circle(radius=0.3, color=YELLOW, fill_opacity=0.7)
            circle.move_to(position)
            label = Text(str(node), font_size=20)
            label.move_to(position)
            node_group = VGroup(circle, label)
            graph_nodes[node] = node_group
        
        # Create edges
        for edge in G.edges():
            start_pos = node_positions[str(edge[0])]
            end_pos = node_positions[str(edge[1])]
            line = Line(start_pos, end_pos, color=WHITE, stroke_width=2)
            graph_edges.append(line)
        
        # Group all graph elements
        all_edges = VGroup(*graph_edges)
        all_nodes = VGroup(*graph_nodes.values())
        graph_group = VGroup(all_edges, all_nodes)
        
        # Animation 4: Transform scrunched data into graph
        self.play(
            Transform(tsv_group, graph_group),
            run_time=3
        )
        
        # Animation 5: Add the "Loaded the graph" text
        title_text = Text("Loaded the graph", font_size=36, color=GREEN)
        title_text.to_edge(UP)
        
        self.play(Write(title_text), run_time=1)
        self.wait(2)
        
        # Optional: Add some final graph animations
        self.play(
            all_nodes.animate.set_color(BLUE),
            all_edges.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(2)
