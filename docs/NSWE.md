# Minecraft: Nintendo Switch Edition

### Everything is in little endian, as opposed to other editions using big endian for their save formats.
### It seems that entities are stored seperate, inside entities.dat which looks to be a modified version of Infdev 627's entities.dat.
#### NSWE
![Dexrn_HxD_z8CdKmZYxa_01-31-2024_03_02_13_167_AM](https://github.com/DexrnZacAttack/LCESaveGameExtractor/assets/60078656/d6a97dad-5965-473c-af5d-512d2ab291bd)
#### Inf627
![Dexrn_HxD_m5EtN0Ccmp_01-31-2024_03_02_31_907_AM](https://github.com/DexrnZacAttack/LCESaveGameExtractor/assets/60078656/2c49e5c1-a73a-4f9a-b730-665b88c5101b)
### Chunks are stored outside of the main gamedata, instead in these GAMEDATA_ files.
![Dexrn_explorer_TXy7K5ZKR3_01-31-2024_02_57_44_298_AM](https://github.com/DexrnZacAttack/LCESaveGameExtractor/assets/60078656/eae294ea-457f-4953-b8ac-cbacb6ca2ce4)
### Each chunk is ZLib compressed.
### Like Wii U edition, world info is stored in .ext files.
