import os
import shutil


mainFolderPath = ""
McGillClassPrefixes = ["FACC", "COMP", "MATH", "ECSE", "CCOM", "MGCR"]
McGillGrades = ["[A]", "[A-]", "[B+]", "[B]", "[B-]", "[C+]", "[C]", "[D]", "[F]"]

for mainFolderPath, subfolders, files in os.walk(mainFolderPath):
    for folder in subfolders:

        if folder.endswith(tuple(McGillGrades)):
            beginningOfFolderString = folder[0:15]

            if folder.startswith(beginningOfFolderString) and not folder.endswith(tuple(McGillGrades)):
                pathToDelete = os.path.abspath(os.path.join(mainFolderPath, folder))
                # joins path initially searched in with folder to delete (MAKE SURE FILEPATH ENDS UP BEING CORRECT)
                print(pathToDelete)
                shutil.rmtree(pathToDelete)  # deletes folder and all of its contents in specified path


