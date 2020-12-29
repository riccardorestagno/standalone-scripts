import os

mainFolderPath = r""  # Folder path to search
McGillClassPrefixes = ["FACC", "COMP", "MATH", "ECSE", "CCOM", "MGCR", "MIME", "PHYS", "CIVE", "SOCI"]  # Possible course codes
FoldersNotToModify = ["ECSE427 - Basic Operating System Code"]  # Folders not to modify


def directory_modifier(main_folder_path, directory, branches_searched=50):
	i = 0
	for branch in directory:  # scans through all sub-folders or files in said folder and renames with prefix if necessary
		
		# Breaks after too many folders or files have been searched to prevent infinite loop
		if i == branches_searched: 
			break
		
		# If branch already has correct prefix or is part of the list of folders not to modify, skip to next loop iteration
		elif branch.startswith(tuple(McGillClassPrefixes)) or branch in FoldersNotToModify:
			i += 1
			continue
		
		# Renames folder with correct prefix
		else:
			print("Now modifying: " + branch)
			
			os.chdir(main_folder_path)  # Changes directory to current folder path
			current_branch = main_folder_path.rfind("\\")  # Finds last backslash (i.e. the name of the current folder it is in
			
			# Creates a string for the course code to be used to rename the folder (takes the form: "AAAA111 - ")
			# Note: 11 needs to be modified depending on the layout of the prefix you choose
			course_code = main_folder_path[current_branch + 1: current_branch + 11]
			
			# If the course code found is part of the prefix list above, and the current path is not part of the restricted modifiable folders list, rename the current branch
			if course_code[0:4] in McGillClassPrefixes and not any(folder in main_folder_path for folder in FoldersNotToModify):
				os.rename(branch, course_code + branch)  # renames current branch with its course code prefix
				print(branch + " has been renamed to " + course_code + branch + "\n")
				
			else:
				print("The branch above was not modified due to directory restrictions set above")


if __name__ == "__main__":
	""" Renames folders and files with the correct McGill course code prefix in the parent folder"""
	
	for mainFolderPath, subfolders, files in os.walk(mainFolderPath):
	
		if any(prefix in mainFolderPath for prefix in McGillClassPrefixes):  # finds main folder with class prefix
			
			directory_modifier(mainFolderPath, subfolders, branches_searched=10)  # Searches for sub-folders to rename

			directory_modifier(mainFolderPath, files, branches_searched=50)  # Searches for files to rename