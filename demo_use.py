from document_support.main_src.main_library import Document_Library
import demo_file_path as fp

#Initialize the Library
myLibrary = Document_Library()

#Add files to the library
myLibrary.add_new_document(fp.JSONL_STR_PATH)
myLibrary.add_new_document(fp.SUBNAUTICA_WIKI)

#Take a look at the layout of the file
print(myLibrary.view_all_file_format())

#Take a look at some of the content
print(myLibrary.peek_at_all_file_content())

#Apply filters to file and remove it
myLibrary.apply_filter_for_file("jsonl_test_file.jsonl", "categories")
myLibrary.reset_filter_for_file("jsonl_test_file.jsonl")

#Serch Through the Library
myLibrary.search_document_for("Coral")

#Get the results
print("===================================================================================")
results = myLibrary.retrieve_results()
for entry in results:
     print(results[entry])