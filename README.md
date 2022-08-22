**WHAT IS THIS PROJECT FOR:**

This initiative attempts to digitize all of the carnatic lesson notations which are handwritten by HS Venugopal Sir.

This aim of this project is to achieve the following:
1. Connect with a custom simple web interface UI which can be used to submit carnatic notation requests to this backend.
2. The backend should then parse the notations and then save all of the content in google drive by programmatically creating a recursive hierarchy of lesson notes in the form of google docs
3. Additionally, this backend will also support any quick querying and searching of lesson notes by systematically saving all of the notes in a google sheet

**TODO**

1. Enable hosting of the backend on heroku
2. Write the following apis:
   1. Creating a notation submission request:
      1. This should create a google doc(with view all permissions) in the required google drive path mentioned (while keeping track of the google doc Id and url)
      2. This should create a unique guid and store it as a row in google sheets (or any other free-to-use database)
      3. Return the metadata back to the requestor
   2. Updating a notation metadata:
      1. If required changes the path on the drive programmatically while also updating the metadata google sheet
   3. Updating a notation file:
      1. Should be able to write into a notation file given text and id
   4. Deleting a notation:
      1. Should remove file from folder ( no need to remove the entire path)
      2. Should delete from meta data google sheet
   5. Search API:
      1. Should be able to search given query filters on the metadata (raga, tala, composer, etc)

**FUTURE WORK**

Implement an approval workflow where notations on submissions are put into a specific google drive folder (for e.g. "notes to be reviewed").
Use the Web UI to showcase all the notes which have to be reviewed and on corrections, an approval should move it to the correct folder.






   