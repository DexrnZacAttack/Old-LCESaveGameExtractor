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
        fileNameFromSaveGame = line[:80].decode("ascii").replace("\x00", "")
        # print(line[120:128])
        # print(line[128:136])
        length = int.from_bytes(line[128:132], byteorder="big")
        offset = int.from_bytes(line[132:136], byteorder="big")
        print(f"Filename: {fileNameFromSaveGame}, Length: {length}, Offset: {offset}")

                
        with open(fileName, "rb") as saveGame:
            if not os.path.exists("LCESaveGameExtractor"):
                os.mkdir("LCESaveGameExtractor")
            if "/" in fileNameFromSaveGame:
                if not os.path.exists("LCESaveGameExtractor\\" + fileNameFromSaveGame[:fileNameFromSaveGame.index("/")]):
                    # https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
                    os.mkdir("LCESaveGameExtractor\\" + fileNameFromSaveGame[:fileNameFromSaveGame.index("/")])
            # Dexrn: replace / with \ so that Windows treats it as a directory.
            with open("LCESaveGameExtractor\\" + fileNameFromSaveGame.replace("/", '\\'), "wb") as saveGameFiles:
                saveGame.seek(offset)
                data = saveGame.read(length)
                saveGameFiles.write(data)

            print(f"Saved {fileNameFromSaveGame}")
