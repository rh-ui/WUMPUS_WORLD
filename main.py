import random
import tkinter as tk
from tkinter import messagebox


class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.wumpus_position = None
        self.treasure_position = None
        self.pits = []
        self.setup_world()

    def setup_world(self):
        self.wumpus_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

        self.treasure_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        while self.treasure_position == self.wumpus_position:
            self.treasure_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))


        for _ in range(3): 
            pit_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            while pit_position == self.wumpus_position or pit_position == self.treasure_position:
                pit_position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            self.pits.append(pit_position)

    def perceive(self):
        x, y = self.agent_position
        surroundings = []

        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if (nx, ny) == self.wumpus_position:
                    surroundings.append('Stench')
                if (nx, ny) in self.pits:
                    surroundings.append('Breeze')
                if (nx, ny) == self.treasure_position:
                    surroundings.append('Glitter')

        return surroundings

    def move_agent(self, direction):
        x, y = self.agent_position
        if direction == 'up' and x > 0:
            self.agent_position = (x - 1, y)
        elif direction == 'down' and x < self.size - 1:
            self.agent_position = (x + 1, y)
        elif direction == 'left' and y > 0:
            self.agent_position = (x, y - 1)
        elif direction == 'right' and y < self.size - 1:
            self.agent_position = (x, y + 1)
        else:
            print("Mouvement invalide.")

    def check_game_over(self):
        if self.agent_position == self.wumpus_position:
            return "L'agent a rencontré le Wumpus ! Jeu terminé."
        if self.agent_position in self.pits:
            return "L'agent est tombé dans un trou ! Jeu terminé."
        if self.agent_position == self.treasure_position:
            return "L'agent a trouvé le trésor ! Félicitations."
        return None


class WumpusWorldGUI:
    def __init__(self, master, world):
        self.master = master
        self.master.title("Wumpus World")
        self.world = world

        self.buttons = []
        self.create_buttons()
        self.status_label = tk.Label(self.master, text="Commandes : Deplacez l'agent.")
        self.status_label.grid(row=self.world.size, column=0, columnspan=self.world.size, sticky="w")

    def create_buttons(self):
        for i in range(self.world.size):
            row = []
            for j in range(self.world.size):
                btn = tk.Button(self.master, text=f'{i},{j}', width=5, height=2,
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    def on_click(self, i, j):
        direction = None
        if i < self.world.agent_position[0]:
            direction = 'up'
        elif i > self.world.agent_position[0]:
            direction = 'down'
        elif j < self.world.agent_position[1]:
            direction = 'left'
        elif j > self.world.agent_position[1]:
            direction = 'right'

        if direction:
            self.world.move_agent(direction)
            self.update_grid()
            self.update_status()

    def update_grid(self):
        for i in range(self.world.size):
            for j in range(self.world.size):
                self.buttons[i][j].config(text=f'{i},{j}', relief="raised")

        # Mettre à jour la position de l'agent
        x, y = self.world.agent_position
        self.buttons[x][y].config(text="A", relief="solid", bg="yellow")

        # Vérifier la fin du jeu
        game_over_message = self.world.check_game_over()
        if game_over_message:
            messagebox.showinfo("Jeu terminé", game_over_message)
            self.master.quit()

    def update_status(self):
        perceptions = self.world.perceive()
        status = f"Perception : {', '.join(perceptions)}"
        self.status_label.config(text=status)


def main():
    world = WumpusWorld(size=4)
    root = tk.Tk()
    app = WumpusWorldGUI(root, world)
    app.update_grid()
    root.mainloop()


if __name__ == "__main__":
    main()
