import os
import sys
import zlib

# Based off of https://www.xpgamesaves.com/threads/advanced-minecraft-savegame-dat-structure-editing.49608/

if len(sys.argv) < 2:
    raise FileNotFoundError(
        "Please provide a filename.\n{} <filename>".format(os.path.basename(__file__))
    )

fileName = sys.argv[1]


def handleZLib(data, start_index):
    pData = data[start_index:]
    DCompOBJ = zlib.decompressobj()
    Flated = DCompOBJ.decompress(pData)
    return Flated


def checkSaveGame(fileName):
    with open(fileName, "rb") as saveGame:
        saveGame.seek(0)
        # Dexrn: Janky and possibly flawed WiiU/Switch level detection.
        if "789c" in saveGame.read(16).hex():
            print("Decompressing...")
            saveGame.seek(0)
            unZLibsG = handleZLib(saveGame.read(), 8)
            with open(fileName + "_ZFlate", "wb") as f:
                f.write(unZLibsG)

            return open(fileName + "_ZFlate", "rb")
        else:
            return open(fileName, "rb")


def start():
    saveGame = checkSaveGame(fileName)
    saveGame.seek(0)

    try:
        header = saveGame.read(3).decode("ascii")
        if header == "CON" or header == "PIRS":
            print(
                f"You must decompress this file manually, as it comes from Xbox 360 Edition.\nThere are multiple tools to do this, I recommend Horizon. (https://www.wemod.com/horizon)\nYou'll also need to get something to handle XMemcompress/LZX, as this tool will not decompress that."
            )
            sys.exit()
    except Exception as e:
        pass

    saveGame.seek(0)
    fileOffset = int.from_bytes(saveGame.read(4), byteorder="big")
    fileCount = int.from_bytes(saveGame.read(4), byteorder="big")
    saveGame.seek(0)
    print(
        f"The index begins at offset {fileOffset}.\nThere are {fileCount} files mentioned in the index."
    )

    # Dexrn: export index to file
    saveGame.seek(0)
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
            print(
                f"Filename: {fileNameFromSaveGame}, Length: {length}, Offset: {offset}"
            )

            if not os.path.exists("LCESaveGameExtractor"):
                os.mkdir("LCESaveGameExtractor")
            if "/" in fileNameFromSaveGame:
                if not os.path.exists(
                    "LCESaveGameExtractor\\"
                    + fileNameFromSaveGame[: fileNameFromSaveGame.index("/")]
                ):
                    # https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
                    os.mkdir(
                        "LCESaveGameExtractor\\"
                        + fileNameFromSaveGame[: fileNameFromSaveGame.index("/")]
                    )
            # Dexrn: replace / with \ so that Windows treats it as a directory.
            with open(
                "LCESaveGameExtractor\\" + fileNameFromSaveGame.replace("/", "\\"), "wb"
            ) as saveGameFiles:
                saveGame.seek(offset)
                data = saveGame.read(length)
                saveGameFiles.write(data)

            print(f"Saved {fileNameFromSaveGame}")


start()
