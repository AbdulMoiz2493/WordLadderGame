import tkinter as tk  # tkinter library for GUI
from tkinter import ttk, messagebox, font  # themed tkinter widgets
import heapq
from collections import deque, defaultdict
import random
import json
import time

from PIL import Image, ImageTk  # PIL library for image handling
import os

import networkx as nx   # nteworkx library for graph visualization
import matplotlib.pyplot as plt   # matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   # matplotlib canvas for tkinter

class ModernButton(ttk.Button):
    def __init__(self, 
                 master=None, 
                 **kwargs):
        style = ttk.Style()
        style.configure('Modern.TButton', 
                       padding=10, 
                       font=('Helvetica', 10, 'bold'),
                       background='#2196F3')
        super().__init__(master, style='Modern.TButton', **kwargs)

class WordLadderGame:
    def __init__(self): # Constructor
        self.dictionaries = self.load_dictionaries()
        self.word_graph = defaultdict(list)
        self.graph_visualization = None
        
        # Game state variables
        self.current_word = ""
        self.target_word = ""
        self.moves = []
        self.max_moves = 0
        self.score = 0
        self.game_mode = "Beginner"
        self.banned_words = set()  # For Challenge mode
        self.restricted_letters = set()  # For Challenge mode
        self.multiplayer_mode = False  # Multiplayer mode
        self.player_scores = {"Player 1": 0, "Player 2": 0}  # Multiplayer scores
        self.current_player = "Player 1"  # Multiplayer turn
        
        self.difficulty_levels = {
            "Beginner": 
                {"max_moves": 10, 
                 "word_length": 3, 
                 "obstacles": False},  # Beginner mode
                
            "Advanced": 
                {"max_moves": 15, 
                 "word_length": 5, 
                 "obstacles": False},  # Advanced mode
                
            "Challenge": 
                {"max_moves": 12, 
                 "word_length": 4, 
                 "obstacles": True}  # Challenge mode
        }
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Word Ladder Adventure")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')  # Dark theme
        
        self.setup_styles()
        self.setup_ui()
        self.create_menu()

    def setup_styles(self):
        """Configure custom styles for modern UI"""
        style = ttk.Style()
        
        # Dark theme colors
        style.configure('.',
                       background='#1e1e1e',
                       foreground='#ffffff',
                       fieldbackground='#2d2d2d')
        
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'), 
                       background='#1e1e1e',
                       foreground='#00bfff')
        
        style.configure('GameInfo.TLabel',
                       font=('Arial', 12),
                       background='#1e1e1e',
                       foreground='#ffffff',
                       padding=5)
        
        style.configure('Score.TLabel',
                       font=('Arial', 16, 'bold'),
                       foreground='#4CAF50',
                       background='#1e1e1e',
                       padding=10)
        
        style.configure('Word.TLabel',
                       font=('Arial', 20, 'bold'),
                       foreground='#ffffff',
                       background='#2d2d2d',
                       padding=10)
        
        style.configure('Modern.TFrame',
                       background='#1e1e1e')

    def create_menu(self):
        """Create menu bar with additional options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, 
                            tearoff=0)    # Create game menu
        
        menubar.add_cascade(label="Game", 
                            menu=game_menu)  # Add game menu
        
        game_menu.add_command(label="New Game", 
                              command=self.start_new_game)  # Add new game option
        
        game_menu.add_command(label="Toggle Multiplayer", 
                              command=self.toggle_multiplayer)  # Add multiplayer option
        
        game_menu.add_separator()  # Add separator
        
        game_menu.add_command(label="Custom Word Ladder", 
                              command=self.show_custom_ladder_dialog)  # Add custom ladder option
        
        
        
        # View menu
        view_menu = tk.Menu(menubar, 
                            tearoff=0)  # Create view menu
        
        menubar.add_cascade(label="View", 
                            menu=view_menu)  # Add view menu
        
        view_menu.add_command(label="Show Graph", 
                              command=self.show_word_graph)  # Add show graph option
        
        
        # Help menu
        help_menu = tk.Menu(menubar, 
                            tearoff=0)  # Create help menu
        
        menubar.add_cascade(label="Help", 
                            menu=help_menu)  # Add help menu
        
        help_menu.add_command(label="How to Play", 
                              command=self.show_help)  # Add how to play option
        
        help_menu.add_command(label="About", 
                              command=self.show_about)  # Add about option
        
        

    def setup_ui(self):
        """Create enhanced game user interface"""
        # Main container using grid layout
        self.main_container = ttk.Frame(self.root, 
                                        style='Modern.TFrame')  # Main container
        
        self.main_container.grid(row=0, 
                                 column=0, 
                                 sticky="nsew", 
                                 padx=20, 
                                 pady=20)  # Grid layout
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, 
                                    weight=1)  # Row weight
        
        self.root.grid_columnconfigure(0, 
                                       weight=1)  # Column weight
        
        # Title
        title_label = ttk.Label(self.main_container, 
                              text="Word Ladder Adventure",
                              style='Title.TLabel')
        
        title_label.grid(row=0, 
                         column=0, 
                         columnspan=2, 
                         pady=(0, 20))  # Grid layout
        
        # Left panel for game controls
        left_panel = ttk.Frame(self.main_container, 
                               style='Modern.TFrame')  # Left panel
        left_panel.grid(row=1, 
                        column=0, 
                        sticky="nsew", 
                        padx=(0, 10))  # Grid layout
        
        # Game mode selection
        mode_frame = ttk.LabelFrame(left_panel, 
                                    text="Game Mode", 
                                    style='Modern.TFrame')  # Game mode frame
        
        mode_frame.pack(fill=tk.X, 
                        pady=10)  # Pack layout
        
        self.mode_var = tk.StringVar(value="Beginner")  # Game mode variable
        for mode in ["Beginner", 
                     "Advanced", 
                     "Challenge"]:
            ttk.Radiobutton(mode_frame,
                          text=mode,
                          variable=self.mode_var,
                          value=mode,
                          command=self.change_game_mode).pack(side=tk.LEFT, 
                                                              padx=10)
        
        # Word display
        word_frame = ttk.Frame(left_panel, 
                               style='Modern.TFrame')
        
        word_frame.pack(fill=tk.X, 
                        pady=20)
        
        self.current_word_label = ttk.Label(word_frame, 
                                            text="", 
                                            style='Word.TLabel') # Current word label
        
        self.current_word_label.pack(side=tk.LEFT, 
                                     expand=True)
        
        ttk.Label(word_frame, text="→", 
                  font=('Helvetica', 24),
                 background='#1e1e1e', 
                 foreground='#ffffff').pack(side=tk.LEFT, padx=20) # Arrow label
        
        self.target_word_label = ttk.Label(word_frame, 
                                           text="", 
                                           style='Word.TLabel') # Target word label
        
        self.target_word_label.pack(side=tk.LEFT, 
                                    expand=True)
        
        # Input area
        input_frame = ttk.Frame(left_panel, 
                                style='Modern.TFrame') # Input frame
        
        
        input_frame.pack(fill=tk.X, 
                         pady=20)
        
        self.word_entry = ttk.Entry(input_frame, 
                                    font=('Arial', 14), 
                                    width=20) # Word entry
        
        
        self.word_entry.pack(pady=5)
        self.word_entry.bind('<Return>', lambda e: self.make_move())
        
        # Buttons
        button_frame = ttk.Frame(left_panel, 
                                 style='Modern.TFrame')  # Button frame
        
        
        button_frame.pack(pady=20)
        
        ModernButton(button_frame, 
                     text="Submit Move", 
                    command=self.make_move).pack(side=tk.LEFT, padx=5)  # Submit move button
        
        
        ModernButton(button_frame, text="Get Hint",
                    command=self.show_hint_options).pack(side=tk.LEFT, padx=5) # Get hint button
        
        ModernButton(button_frame, text="New Game",
                    command=self.start_new_game).pack(side=tk.LEFT, padx=5)  # New game button
        
        
        
        # Game info
        info_frame = ttk.Frame(left_panel, 
                               style='Modern.TFrame') # Info frame
        
        info_frame.pack(fill=tk.X, 
                        pady=20)
        
        self.moves_text = tk.Text(info_frame, height=3, 
                                  width=40,
                                font=('Arial', 12), 
                                wrap=tk.WORD,
                                bg='#2d2d2d', 
                                fg='#ffffff') # Moves text
        
        self.moves_text.pack(fill=tk.X, 
                             pady=5)
        
        # Statistics
        stats_frame = ttk.Frame(info_frame, 
                                style='Modern.TFrame')  # Stats frame
        
        stats_frame.pack(fill=tk.X, 
                         pady=10)
        
        self.score_label = ttk.Label(stats_frame, 
                                     text="Score: 0",
                                   style='Score.TLabel')  # Score label
        self.score_label.pack(side=tk.LEFT, 
                              padx=20)
        
        self.moves_count_label = ttk.Label(stats_frame, 
                                           text="Moves: 0/10",
                                         style='Score.TLabel')  # Moves count label
        
        self.moves_count_label.pack(side=tk.LEFT, 
                                    padx=20)
        
        # Right panel for graph visualization
        self.right_panel = ttk.Frame(self.main_container, 
                                     style='Modern.TFrame') # Right panel
        self.right_panel.grid(row=1, 
                              column=1, 
                              sticky="nsew")  # Grid layout
        
        
        
        # Create initial graph visualization
        self.create_graph_visualization()

    def load_dictionaries(self):
        """Load words from dictionary file into separate difficulty-based dictionaries"""
        
        dictionaries = {
            "Beginner": set(),
            "Challenge": set(),
            "Advanced": set()
        }
        
        # Add some default words
        default_words = {
            "Beginner": 
                {"cat", "bat", "hat", "hot", "dot", "dog", "bog", "big", "bag", "tag"},
            "Challenge": 
                {"word", "ward", "warm", "worm", "worn", "corn", "coin", "cold", "bold", "hold"},
            "Advanced": 
                {"stone", "store", "score", "scare", "spare", "spade", "shade", "shake", "shale", "scale"}
        }
        
        try:
            current_section = None
            with open('dictionary.txt', 'r') as file:
                for line in file:
                    
                    line = line.strip().lower()
                    if line.startswith('#'):
                        if '3-letter' in line:
                            current_section = "Beginner"
                        elif '4-letter' in line:
                            current_section = "Challenge"
                        elif '5-letter' in line:
                            current_section = "Advanced"
                    elif line and current_section:
                        dictionaries[current_section].add(line)
                        
        except FileNotFoundError:
            # Use default words 
            dictionaries = default_words
            
        return dictionaries
    
    

    def build_word_graph(self):
        """Build graph of words for current game mode"""
        self.word_graph.clear()
        current_dict = self.dictionaries[self.game_mode]
        
        # For Challenge mode, add obstacles
        if self.game_mode == "Challenge":
            self.banned_words = set(random.sample(list(current_dict), 5)) # Randomly select 5 words
            self.restricted_letters = set(random.sample('abcdefghijklmnopqrstuvwxyz', 3))  # Randomly select 3 letters
            current_dict = current_dict - self.banned_words  # Remove banned words
        
        for word in current_dict:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':  # Check all possible letter changes
                    if self.game_mode == "Challenge" and c in self.restricted_letters:  # Skip restricted letters
                        continue
                    new_word = word[:i] + c + word[i+1:]  # Create new word
                    if new_word in current_dict and new_word != word:
                        self.word_graph[word].append(new_word)



    def update_graph_visualization(self):
        """Update the graph visualization with current game state"""
        if not self.current_word or not self.target_word:
            return
        
        # Create NetworkX graph
        G = nx.Graph()
    
        # Add nodes and edges
        words_to_show = set([self.current_word, self.target_word] + self.moves)
        for word in words_to_show:
            G.add_node(word)
            for next_word in self.word_graph[word]:
                if next_word in words_to_show:
                    G.add_edge(word, next_word)
    
        # Clear previous plot
        plt.clf()
    
        # Set figure style with adjusted margins
        plt.margins(x=0.2, y=0.2)
        plt.title("Word Graph", 
                  color='white', 
                  pad=10, 
                  fontsize=12)
    
        # Create new plot with improved layout
        pos = nx.spring_layout(G, k=1.5, 
                               iterations=50)  # Adjusted k value and iterations
    
        # Draw edges
        nx.draw_networkx_edges(G, pos, 
                            edge_color='#4a4a4a',
                            width=1.5,
                            alpha=0.6)
    
    
        # Draw nodes with different colors and adjusted size
        node_colors = []
        for node in G.nodes():
            if node == self.current_word:
                node_colors.append('#00ff00')  # Green for current word
            elif node == self.target_word:
                node_colors.append('#ff0000')  # Red for target word
            else:
                node_colors.append('#00bfff')  # Blue for intermediate words
    
        nx.draw_networkx_nodes(G, pos,
                            node_color=node_colors,
                            node_size=1000,  # Adjusted node size
                            alpha=0.7)
    
        # Draw labels with improved visibility and size
        nx.draw_networkx_labels(G, pos,
                            font_size=8,  # Adjusted font size
                            font_weight='bold',
                            font_color='white')
    
        # Adjust layout to prevent cutoff
        plt.tight_layout()
    
        # Update canvas
        self.graph_canvas.draw()

    def create_graph_visualization(self):
        """Create and display the word graph visualization"""
        # Create figure with adjusted size
        fig, ax = plt.subplots(figsize=(4, 4), 
                               facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')
        plt.subplots_adjust(left=0.1, 
                            right=0.9, 
                            top=0.9, 
                            bottom=0.1)
    
        # Create graph canvas with proper sizing
        self.graph_canvas = FigureCanvasTkAgg(fig, 
                                              master=self.right_panel)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, 
                                               expand=True, 
                                               padx=10, 
                                               pady=10)  # Pack layout
    
        self.update_graph_visualization()

    def a_star_search(self):
        """Perform A* search to find optimal path to target"""
        start = self.current_word
        goal = self.target_word
        
        frontier = [(self.heuristic(start), 0, start, [start])]
        heapq.heapify(frontier)
        explored = set()
        
        while frontier:
            _, cost, current, path = heapq.heappop(frontier)
            
            if current == goal:
                return cost, path
                
            if current in explored:
                continue
                
            explored.add(current)
            
            for next_word in self.word_graph[current]:
                if next_word not in explored:
                    new_cost = cost + 1
                    new_path = path + [next_word]
                    priority = new_cost + self.heuristic(next_word)
                    heapq.heappush(frontier, (priority, new_cost, next_word, new_path))
        
        return None, None

    def uniform_cost_search(self):
        """Perform Uniform Cost Search to find optimal path to target"""
        start = self.current_word
        goal = self.target_word
        
        frontier = [(0, start, [start])]  # (cost, word, path)
        heapq.heapify(frontier)
        explored = set()
        
        while frontier:
            cost, current, path = heapq.heappop(frontier)
            
            if current == goal:
                return cost, path
                
            if current in explored:
                continue
                
            explored.add(current)
            
            for next_word in self.word_graph[current]:
                if next_word not in explored:
                    new_cost = cost + 1
                    new_path = path + [next_word]
                    heapq.heappush(frontier, (new_cost, next_word, new_path))
        
        return None, None

    def breadth_first_search(self):
        """Perform Breadth-First Search to find path to target"""
        start = self.current_word
        goal = self.target_word
        
        queue = deque([(start, [start])])  # (word, path)
        explored = set([start])
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return len(path) - 1, path
                
            for next_word in self.word_graph[current]:
                if next_word not in explored:
                    explored.add(next_word)
                    new_path = path + [next_word]
                    queue.append((next_word, new_path))
        
        return None, None

    def heuristic(self, word):
        """Calculate heuristic value (number of differing letters from target)"""
        return sum(1 for a, b in zip(word, self.target_word) if a != b)

    def start_new_game(self):
        """Initialize a new game with appropriate settings for the current mode"""
        current_dict = self.dictionaries[self.game_mode]
        mode_config = self.difficulty_levels[self.game_mode]
        
        # Reset game state
        self.moves = []
        self.max_moves = mode_config["max_moves"]
        self.score = 100
        
        # Select random start and end words
        valid_words = list(current_dict - self.banned_words)
        if len(valid_words) < 2:
            messagebox.showerror("Error", "Not enough valid words available!")
            return

        self.current_word = random.choice(valid_words)
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            self.target_word = random.choice(valid_words)
            if (self.target_word != self.current_word and 
                self.check_path_exists(self.current_word, self.target_word)):
                break
            attempts += 1
        
        if attempts >= max_attempts:
            messagebox.showerror("Error", "Could not find valid word pair!")
            return
        
        self.update_ui()
        
        # Show game mode specific information
        if self.game_mode == "Challenge":
            info_text = "Challenge Mode Rules:\n"
            info_text += f"Banned words: {', '.join(self.banned_words)}\n"
            info_text += f"Restricted letters: {', '.join(self.restricted_letters)}"
            messagebox.showinfo("Challenge Mode", info_text)

    def change_game_mode(self):
        """Handle game mode change"""
        self.game_mode = self.mode_var.get()
        self.build_word_graph()
        self.start_new_game()

    def make_move(self):
        """Process a player's move with multiplayer support"""
        new_word = self.word_entry.get().lower()
        
        # Validate move
        if not self.is_valid_move(new_word):
            messagebox.showerror("Invalid Move", 
                               "Invalid word or move! Check the rules and try again.")
            return
        
        # Update game state
        self.moves.append(new_word)
        self.current_word = new_word
        self.score -= 5
        
        self.update_ui()
        self.update_graph_visualization()
        
        # Check win/lose conditions
        if new_word == self.target_word:
            if self.multiplayer_mode:
                self.player_scores[self.current_player] += self.score   # Add score to current player
                
                win_text = f"{self.current_player} wins!\n"
                win_text += f"Scores:\nPlayer 1: {self.player_scores['Player 1']}\n"
                win_text += f"Player 2: {self.player_scores['Player 2']}"  # Show scores
                
                messagebox.showinfo("Game Over", win_text)
                self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"  # Switch player
                
            else:
                messagebox.showinfo("Congratulations!", 
                                  f"You won! Final score: {self.score}") # Show final score
                
            self.start_new_game()
        elif len(self.moves) >= self.max_moves:
            
            if self.multiplayer_mode:
                self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"  # Switch player
                messagebox.showinfo("Turn Over", f"{self.current_player}'s turn!")
                
            else:
                messagebox.showinfo("Game Over", "Maximum moves reached!")
            self.start_new_game()
            
            

    def is_valid_move(self, new_word):
        """Check if the move is valid according to game rules"""
        if not new_word:
            return False
            
        # Check if word exists in dictionary
        if new_word not in self.dictionaries[self.game_mode]:
            return False
            
        # Check if word is banned (Challenge mode)
        if new_word in self.banned_words:
            return False
            
        # Check if only one letter is changed
        diff_count = sum(1 for a, b in zip(self.current_word, new_word) if a != b)
        if diff_count != 1:
            return False
            
        # Check if new letters are not restricted (Challenge mode)
        if self.game_mode == "Challenge":
            changed_letter = next(b for a, b in zip(self.current_word, new_word) if a != b)
            if changed_letter in self.restricted_letters:
                return False
        
        return True

    def check_path_exists(self, start, target):
        """Check if a path exists between start and target words using BFS"""
        if start == target:
            return True
            
        visited = set([start])
        queue = deque([start])
        
        while queue:
            word = queue.popleft()
            for next_word in self.word_graph[word]:
                if next_word == target:
                    return True
                if next_word not in visited:
                    visited.add(next_word)
                    queue.append(next_word)
        
        return False

    def update_ui(self):
        """Update all UI elements with current game state"""
        self.current_word_label.config(text=self.current_word)  # Update labels
        self.target_word_label.config(text=self.target_word)  # Update labels
        self.moves_text.delete(1.0, tk.END)  # Clear moves text
        self.moves_text.insert(1.0, " → ".join(self.moves))  # Update moves text
        self.score_label.config(text=f"Score: {self.score}")  # Update score label
        self.moves_count_label.config(text=f"Moves: {len(self.moves)}/{self.max_moves}")  # Update moves count label
        self.word_entry.delete(0, tk.END)  # Clear word entry
        
        if self.multiplayer_mode:
            self.score_label.config(
                text=f"Scores - P1: {self.player_scores['Player 1']} | "
                     f"P2: {self.player_scores['Player 2']} | "
                     f"Current: {self.current_player}")

    def get_hint(self, algorithm="A*"):
        """Get next move suggestion using specified algorithm"""
        if algorithm == "A*":
            _, path = self.a_star_search()
        elif algorithm == "UCS":
            _, path = self.uniform_cost_search()
        elif algorithm == "BFS":
            _, path = self.breadth_first_search()
        
        if path and len(path) > 1:
            return path[1]
        return None

    def show_hint_options(self):
        """Show dialog for selecting hint algorithm"""
        hint_window = tk.Toplevel(self.root)
        hint_window.title("Get Hint")
        hint_window.geometry("400x350")
        hint_window.configure(bg='#1e1e1e')
        
        ttk.Label(hint_window, 
                 text="Select Search Algorithm",
                 style='Title.TLabel').pack(pady=10)
        
        algorithms = {
            "UCS": ("Uniform Cost Search", 
                   "Finds the optimal solution by exploring paths with lowest cost first"),
            "A*": ("A* Search",
                  "Uses heuristics to guide search towards the goal efficiently"),
            "BFS": ("Breadth-First Search",
                   "Explores all possible paths level by level")
        }
        
        algorithm_var = tk.StringVar(value="A*")
        
        for alg, (name, desc) in algorithms.items():
            frame = ttk.Frame(hint_window, 
                              style='Modern.TFrame') # Frame
            
            frame.pack(fill=tk.X, 
                       padx=10, 
                       pady=5)
            
            ttk.Radiobutton(frame,
                          text=name,
                          variable=algorithm_var,
                          value=alg).pack(side=tk.LEFT)
            
            ttk.Label(frame,
                     text=desc,
                     wraplength=300,
                     style='GameInfo.TLabel').pack(side=tk.LEFT, 
                                                   padx=5)
                     
        
        def get_hint():
            hint = self.get_hint(algorithm_var.get())
            if hint:
                messagebox.showinfo("Hint", f"Suggested next word: {hint}")
            hint_window.destroy()
        
        ModernButton(hint_window,
                    text="Get Hint",
                    command=get_hint).pack(pady=10)
        
        ModernButton(hint_window,
                    text="Compare Algorithms",
                    command=self.show_algorithm_comparison).pack(pady=10)

    def show_algorithm_comparison(self):
        """Compare and display results from different search algorithms"""
        algorithms = {
            "A*": self.a_star_search,
            "UCS": self.uniform_cost_search,
            "BFS": self.breadth_first_search
        }
        
        results = {}
        for name, func in algorithms.items():
            start_time = time.time()
            cost, path = func()
            end_time = time.time()
            
            if path:
                results[name] = {
                    "cost": cost,
                    "path_length": len(path),
                    "time": end_time - start_time,
                    "path": " → ".join(path)
                }
        
        # Create comparison window
        comp_window = tk.Toplevel(self.root)
        comp_window.title("Algorithm Comparison")
        comp_window.geometry("600x400")
        comp_window.configure(bg='#1e1e1e')
        
        # Add results to window
        ttk.Label(comp_window,
                 text="Search Algorithm Comparison",
                 style='Title.TLabel').pack(pady=10)
        
        for alg, data in results.items():
            frame = ttk.Frame(comp_window, 
                              style='Modern.TFrame')  # Frame
            
            frame.pack(fill=tk.X, 
                       padx=10, 
                       pady=5)
            
            
            info_text = f"{alg}:\n"
            info_text += f"Cost: {data['cost']}\n"
            info_text += f"Path Length: {data['path_length']}\n"
            info_text += f"Time: {data['time']:.6f} seconds\n"
            info_text += f"Path: {data['path']}"
            
            ttk.Label(frame,
                     text=info_text,
                     style='GameInfo.TLabel',
                     wraplength=550).pack(padx=5)

    def toggle_multiplayer(self):
        """Toggle between single player and multiplayer modes"""
        self.multiplayer_mode = not self.multiplayer_mode
        if self.multiplayer_mode:
            self.player_scores = {"Player 1": 0, 
                                  "Player 2": 0}  # Reset scores
            
            
            self.current_player = "Player 1"  # Set current
            
            messagebox.showinfo("Multiplayer Mode", 
                              "Multiplayer mode activated!\nPlayer 1's turn")
        else:
            messagebox.showinfo("Single Player Mode", 
                              "Switched to single player mode")
        self.start_new_game()

    def show_help(self):
        """Display help information"""
        help_text = """
        Word Ladder Adventure - How to Play
        
        1. Transform the starting word into the target word
        2. Change only one letter at a time
        3. Each new word must be valid
        4. Complete the challenge in as few moves as possible
        5. Use hints if you get stuck
        
        Game Modes:
        - Beginner: 3-letter words
        - Advanced: 5-letter words
        - Challenge: 4-letter words with obstacles
        
        Features:
        - Multiplayer mode available
        - Create custom word ladders
        - View word graph visualization
        - AI-powered hints using different algorithms
        """
        
        messagebox.showinfo("How to Play", help_text)

    def show_about(self):
        """Display about information"""
        about_text = """
        Word Ladder Adventure
        
        A game-based implementation of the classic word ladder puzzle featuring multiple game modes, AI-powered hints, and graph visualization.
        
        Created for educational and entertainment purposes.
        """
        
        messagebox.showinfo("About", about_text)

    def show_custom_ladder_dialog(self):
        """Show dialog for creating custom word ladder"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Custom Word Ladder")
        dialog.geometry("400x200")
        dialog.configure(bg='#1e1e1e')
        
        ttk.Label(dialog, text="Start Word:", 
                 style='GameInfo.TLabel').pack(pady=5)
        start_entry = ttk.Entry(dialog, font=('Helvetica', 12))
        start_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Target Word:",
                 style='GameInfo.TLabel').pack(pady=5)
        target_entry = ttk.Entry(dialog, font=('Helvetica', 12))
        target_entry.pack(pady=5)
        
        def create_custom_ladder():
            start = start_entry.get().lower()
            target = target_entry.get().lower()

            
            if len(start) != len(target):
                messagebox.showerror("Error", "Words must be the same length!")
                return
                
            if not (start in self.dictionaries[self.game_mode] and 
                   target in self.dictionaries[self.game_mode]):
                messagebox.showerror("Error", "Both words must be in dictionary!")
                return
                
            if not self.check_path_exists(start, target):
                messagebox.showerror("Error", "No valid path exists between words!")
                return
                
            self.current_word = start
            self.target_word = target
            self.moves = []
            self.update_ui()
            dialog.destroy()
        
        ModernButton(dialog, text="Create Ladder",
                    command=create_custom_ladder).pack(pady=20)

    
    
    def show_word_graph(self):
        """Display the full word graph in a new window"""
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Word Graph Visualization")
        graph_window.geometry("600x600")  # Adjusted window size
        graph_window.configure(bg='#1e1e1e')

        # Create figure with adjusted size
        fig, ax = plt.subplots(figsize=(8, 8), 
                               facecolor='#1e1e1e')
        
        ax.set_facecolor('#1e1e1e')
        plt.subplots_adjust(left=0.1, 
                            right=0.9, 
                            top=0.9, 
                            bottom=0.1)
        

        # Create NetworkX graph
        G = nx.Graph()

        # Add all words and connections
        for word in self.word_graph:
            G.add_node(word)
            for next_word in self.word_graph[word]:
                G.add_edge(word, next_word)

        # Set layout with adjusted parameters
        pos = nx.spring_layout(G, k=1, iterations=50)

        # Draw edges
        nx.draw_networkx_edges(G, pos,
                              edge_color='#4a4a4a',
                              width=0.5,
                              alpha=0.3)

        # Draw nodes with adjusted size
        node_colors = ['#00bfff' for _ in G.nodes()]
        nx.draw_networkx_nodes(G, pos,
                              node_color=node_colors,
                              node_size=300,  # Reduced node size
                              alpha=0.6)

        # Draw labels with adjusted font size
        nx.draw_networkx_labels(G, pos,
                               font_size=6,  # Reduced font size
                               font_weight='bold',
                               font_color='white')

        # Adjust layout to prevent cutoff
        plt.tight_layout()

        # Create canvas with proper sizing
        canvas = FigureCanvasTkAgg(fig, 
                                   master=graph_window) # Canvas
        
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, 
                                    expand=True, 
                                    padx=10, 
                                    pady=10)  # Pack layout
    
    
    def run(self):
        """Start the game"""
        self.build_word_graph()
        self.start_new_game()
        self.root.mainloop()
        





if __name__ == "__main__":
    game = WordLadderGame()
    game.run()