from plp_library.main_library import Document_Library
import demo_file_path as fp

#Initialize the Library
myLibrary = Document_Library()
print("===================================================================================")
print("-- Created a Library Object. --")

#Set how I want the results to be returned
print("")
print("===================================================================================")
print("-- Toggle how the search results should be returned. --")
myLibrary.toggle_result_format_toDict(True)
myLibrary.toggle_result_format_toString(True)
print("")
print("===================================================================================")

#Add files to the library
print("-- Add any file to the in memory library. --")
myLibrary.add_new_document(fp.JSONL_STR_PATH)
myLibrary.add_new_document(fp.SUBNAUTICA_WIKI)
print("")
print("===================================================================================")

#Take a look at the layout of the file
print("-- Take a look at the layout the file. --")
print("== All files ==")
schema = myLibrary.view_all_files_format()
for entry in schema.keys():
     print(schema[entry])
     
print("")
print("== One file ==")
schema = myLibrary.view_file_format("jsonl_test_file.jsonl")
print(schema)
     
print("")
print("===================================================================================")

#Take a look at some of the content
print("-- Take a look at all file in library. --")
peek = myLibrary.peek_all_files_content()
for entry in peek.keys():
     print(peek[entry])
     
#Take a look at some of the content
print("")
print("-- Take a look at a file in the library. --")
peek = myLibrary.peek_file_content("jsonl_test_file.jsonl")
for entry in peek:
     print(entry)
     
print("")
print("===================================================================================")

#Apply filters to file and remove it
myLibrary.apply_filter_for_file("jsonl_test_file.jsonl", "categories")

#Search Through the Library
myLibrary.search_library("Do you have information on coral?")

#Get the results
results = myLibrary.retrieve_results()
for entry in results:
     print(results[entry])
     
print("")
print("===================================================================================")
     
print("-- Now remove filter and search again --")
myLibrary.reset_filter_for_file("jsonl_test_file.jsonl")
#Search Through the Library
myLibrary.search_library("Do you have information on coral?")

#Get the results
results = myLibrary.retrieve_results()
for entry in results:
     print(results[entry])
     
print("")
print("===================================================================================")
print("Demo Complete")