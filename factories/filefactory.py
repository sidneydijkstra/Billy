import os
import discord
import random
from gtts import gTTS
from factories.uniqueidfactory import UniqueIdFactory

class FileFactory:
    # setup files factory can load
    publicFilesAccepted = [
        "mp3",
        "wav"
    ]

    # setup public folder factory can load
    publicFoldersPath = [
        "./audio/",
        "./audio/radio/"
    ]

    # setup jingle folder path
    publicJingleFolderPath = "./audio/radio/"
    # setup temp folder path
    publicTempFolderPath = "./audio/temp/"

    # create temp folder if not exists
    if not os.path.exists(publicTempFolderPath):
        os.makedirs(publicTempFolderPath)

    # load all files and setup file array
    files = []
    for folder in publicFoldersPath:
        for file in os.listdir(folder):
            fileSplit = file.split('.')

            if len(fileSplit) == 2 and fileSplit[1] in publicFilesAccepted:
                files.append({
                    "name": fileSplit[0],
                    "type": fileSplit[1],
                    "path": folder + file
                })

    # load all jingels and setup jingle array
    jingleFiles = []
    for file in os.listdir(publicJingleFolderPath):
        fileSplit = file.split('.')
        if len(fileSplit) == 2 and fileSplit[1] in publicFilesAccepted:
            jingleFiles.append({
                "name": fileSplit[0],
                "type": fileSplit[1],
                "path": folder + file
            })
    # shuffle jingle array
    jingles = random.sample(jingleFiles, len(jingleFiles))


    def getFilePath(name):
        # loop files in files array
        for file in FileFactory.files:
            # check file name with name variable
            if file['name'] == name:
                # return file path on match
                return file['path']
        # return None on no match
        return None

    def getRandomJingle():
        # check if more jingles in array
        if len(FileFactory.jingles) > 0:
            # return jingle
            return FileFactory.jingles.pop(0)
        else:
            # shuffle jingle array
            FileFactory.jingles = random.sample(FileFactory.jingleFiles, len(FileFactory.jingleFiles))
            # return jingle
            return FileFactory.jingles.pop(0)

    def generateTTSFile(value):
        tts = gTTS(text=value, lang='nl', slow=True)
        uuid = UniqueIdFactory.getUuid()
        fileName = uuid + ".mp3"
        tts.save(FileFactory.publicTempFolderPath + fileName)

        return {
            "name": uuid,
            "type": fileName,
            "path": FileFactory.publicTempFolderPath + fileName
        }

    def clearTempFolder():
        for file in os.listdir(FileFactory.publicTempFolderPath):
            os.remove(FileFactory.publicTempFolderPath + file)
