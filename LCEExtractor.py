import os

# Based off of https://www.xpgamesaves.com/threads/advanced-minecraft-savegame-dat-structure-editing.49608/

# Dexrn: read the savegame (MUST BE DECOMPRESSED)
fileName = "savegame-decompressed.dat"
with open(fileName, "rb") as saveGame:
    fileOffset = int.from_bytes(saveGame.read(4), byteorder="big")
    fileCount = int.from_bytes(saveGame.read(4), byteorder="big")
    print(f"The index begins at offset {fileOffset}.\nThere are {fileCount} files mentioned in the index.")

# Dexrn: export index to file
with open(fileName, "rb") as saveGame:
    saveGame.seek(fileOffset)
    index = saveGame.read()
with open("index.dat", "wb") as f:
    f.write(index)

# Dexrn: extraction
with open("index.dat", "rb") as f:
    while True:
        line = f.read(144)
        if not line:
            break
        fileNameFromSaveGame = line[:80].decode("ascii").rstrip("\x00")
        # print(line[120:128])
        # print(line[128:136])
        length = int.from_bytes(line[128:132], byteorder="big")
        offset = int.from_bytes(line[132:136], byteorder="big")
        print(f"Filename: {fileNameFromSaveGame}, Length: {length}, Offset: {offset}")

                
        with open(fileName, "rb") as saveGame:
            # Dexrn: yes I am replacing / with the word Slash... IDK what else to replace it with LMAO
            with open(fileNameFromSaveGame.replace("\x00", "").replace("/", "Slash"), "wb") as saveGameFiles:
                saveGame.seek(offset)
                data = saveGame.read(length)
                saveGameFiles.write(data)

            print(f"Saved {fileNameFromSaveGame}")
