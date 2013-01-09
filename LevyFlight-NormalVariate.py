import c4d
from c4d import documents  # Unused. Find out why
from c4d import Vector
from random import seed
# Normal Variate distribution used for Rayleigh Flight.
# This is not a 'true' Levy Flight, but it produces nicer-looking results.
# For a longer tail, import the Pareto distribution (paretovariate), which is always positive.
from random import normalvariate as rand
from math import *

#########################################################################

#Constants
RANDOM_SEED = 8
SPHERE_RADIUS = 1
PIPE_RADIUS = 0.5
NUM_NODES = 40
RANGE = 800

#########################################################################

# Where to start randomizing
means = Vector(0, 1000, 0)
# Range?
ranges = Vector(RANGE, RANGE, RANGE)
SphereScale = Vector(SPHERE_RADIUS, SPHERE_RADIUS, SPHERE_RADIUS)


spheres = []
cylinders = []

# Init Random Funcs
seed(RANDOM_SEED)


def GetRandomVector(v=means):
    "Returns a random vector with magnitude v (a vector quantity)"
    return Vector(rand(v.x, ranges.x), rand(v.y, ranges.y), rand(v.z, ranges.z))


def AddSphere(i=0, position=Vector()):
    "Adds a new sphere to the document and to the list. Defaults to the origin."
    spheres.append(c4d.BaseObject(c4d.Osphere))      # Allocate a new Sphere object at (0, 0, 0)
    spheres[i].SetAbsPos(position)
    spheres[i].SetAbsScale(SphereScale)
    doc.InsertObject(spheres[i])


def main():
    AddSphere()  # Add first one. for every other sphere, add a connector as well.
    for i in xrange(1, NUM_NODES):                        # TODO change position
        # Create next point
        there = GetRandomVector(spheres[i - 1].GetAbsPos())
        AddSphere(i=i, position=there)
        myCylinder = c4d.BaseObject(c4d.Ocylinder)
        cylinders.append(myCylinder)
        delta = spheres[i].GetAbsPos() - spheres[i - 1].GetAbsPos()
        pipeScale = Vector(PIPE_RADIUS, delta.GetLength() / 200 - SPHERE_RADIUS, PIPE_RADIUS)
        cylinders[i - 1].SetAbsScale(pipeScale)
        cylinders[i - 1].SetAbsPos(spheres[i - 1].GetAbsPos() + delta / 2)
        cylinders[i - 1].SetRelRot(c4d.utils.VectorToHPB(- delta) + Vector(0, pi / 2, 0))
        doc.InsertObject(cylinders[i - 1])
        #For future use: returns a list of all the generated objects.
        # return cylinders + spheres


# Run this
main()
