import cv2
import numpy as np
import random


persons = []

class FaceIdentifier:
    def __init__(self, owner_id=0, owner_name="???"):
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.neural_network = None
        global persons
        persons.append(self)

    def is_it_that_person(self, frame):
        #some neural magic
        return random.randrange(100) < 50

    def train(self, face):
        pass


def load_all():
    pass

def save_one():
    pass

def save_all():
    for person in persons:
        save_one()

def identify(face, exclude=[]):
    for person in persons:
        if person not in exclude:
            if person.is_it_that_person(face):
                face.owner_id = person.owner_id
                face.owner_name = person.owner_name
                face.identified = True
                return

def identify_faces(faces):
    for face in faces:
        if not face.identified:
            identify(face)
            if not face.identified:
                new_person = FaceIdentifier()
                face.identified = True
                new_person.train(face)

FaceIdentifier(1, "Human #1")
FaceIdentifier(2, "Human #2")
FaceIdentifier(3, "Human #3")