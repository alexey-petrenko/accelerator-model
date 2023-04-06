#!/usr/bin/env python3

import accmodel as am

Q1 = am.Quadrupole(L=0.2, K1=2.0, name="Q1")
Q2 = am.Quadrupole(L=0.2, K1=-2.0, name="Q2", s=1.0)

print(f"{Q1.type_name}: name={Q1.name}, K1={Q1.K1} 1/m^2, location={Q1.s} m")
print(f"Q1 matrix = \n{Q1.M()}\n")

Sol1 = am.Solenoid(L=0.5, K=1.4, name="Sol1", s=2.0)

print(f"{Sol1.type_name}: name={Sol1.name}, K={Sol1.K} 1/m, location={Sol1.s} m")
print(f"Sol1 matrix = \n{Sol1.M()}\n")

S_bend1 = am.SectorBend(L=0.6, alpha=0.31, name="S_bend1", s=2)
print(f"{S_bend1.type_name}: name={S_bend1.name}, alpha={S_bend1.alpha} rad, location={S_bend1.s} m")
print(f"S_bend1 matrix = \n{S_bend1.M()}\n")

# create beamline:

chan = am.Beamline([Q1,Q2], name="channel 1")

print(chan)

chan.append(Sol1)

print(chan)

#input("Press Enter to Exit.")

Q2.s = -1.0

chan.sort()

print(chan)
