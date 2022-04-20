'''
What Danny did:
1. Write a subclass called Node to store position + direction together, 
reducing the need for both stack & coords
2. Combined several methods together
3. Linked with main game module
'''

import pygame

class Node:
	# Class of a node, containing x, y, and the direction it is moving to next
	def __init__(self, location, direction):
		self._x 	= location[0]
		self._y 	= location[1]
		self._dir 	= direction
	
	# Accessors and Modifiers
	def get_x(self):
		return self._x
		
	def set_x(self, new_x):
		self._x = new_x
		
	def get_y(self):
		return self._y
		
	def set_y(self, new_y):
		self._y = new_y
	
	def get_pos(self):
		return (self._x, self._y)
	
	def get_dir(self):
		return self._dir
		
	def set_dir(self, new_dir):
		self._dir = new_dir



class Snake:
	# spawn_pos takes in a tuple indicating snake's spawn point
    def __init__(self, spawn_pos):
        self._head = Node(spawn_pos, 'r')               # By default going rightward
        self._body = [self._head]                       # The body is a stack that stores all the nodes in the snake. body[0] is the head node
    
    # Accessors and Modifiers
    # Return head node's position
    def get_head_pos(self):
        return self._head.get_pos()
    
    # Return head node's direction
    def get_head_dir(self):
        return self._head.get_dir()

    # Update head node's direction    
    def set_head_dir(self, new_dir):                    # The player can only directly interact with the head's direction
        self._head.set_dir(new_dir)
        self._body[0].set_dir(new_dir)
    
    # Return the list of nodes that makes up the body
    def get_body(self):
        return self._body
    
    # Returns True if the snake is alive (body is not empty)
    def is_alive(self):
        return len(self._body) > 0
    
    # Return a list of eligible player moves based on current direction
    def get_eligible_moves(self):
        curr_dir = self._body[0].get_dir()
        if curr_dir == 'r' or curr_dir == 'l':
            return ['u','d']
        elif curr_dir == 'u' or curr_dir == 'd':
            return ['l','r']
    
    # Function to make the snake longer if they get the good fruit, by 
    # pushing the new_node to the back of the body stack
    def add_body(self):
        # First, the new node's direction is same as body[-1]'s direction
        new_dir = self._body[-1].get_dir()
        # Second, new node's position can be computed based on body[-1]'s position
        old_pos = self._body[-1].get_pos()
        if new_dir == 'r':
            new_pos = (old_pos[0] - 20, old_pos[1])
        elif new_dir == 'l':
            new_pos = (old_pos[0] + 20, old_pos[1])
        elif new_dir == 'u':
            new_pos = (old_pos[0], old_pos[1] + 20)
        elif new_dir == 'd':
            new_pos = (old_pos[0], old_pos[1] - 20)
        # Initialize and append the new node
        new_node = Node(new_pos, new_dir)
        self._body.append(new_node)

    # Function to make the snake shorter if they get the bad fruit 
    def rm_body(self):
        self._body.pop()

    # Function to update the positions & directions of all nodes in 
    # the snake's body
    def update_body(self, offset):
        next_dir = self._body[0].get_dir()
        for i in range(len(self._body)):
            # Update position
            curr_dir = self._body[i].get_dir()
            curr_x = self._body[i].get_x()
            curr_y = self._body[i].get_y()
            if curr_dir == 'r':
                self._body[i].set_x(curr_x + offset)
            elif curr_dir == 'l':
                self._body[i].set_x(curr_x - offset)
            elif curr_dir == 'u':
                self._body[i].set_y(curr_y - offset)
            elif curr_dir == 'd':
                self._body[i].set_y(curr_y + offset)
            # Update direction
            # Skip the direction update for head node
            if i == 0:
                continue
            self._body[i].set_dir(next_dir)
            next_dir = curr_dir
