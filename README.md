**WHAT IS THIS PROJECT FOR:**

This initiative attempts to digitize all of the carnatic lesson notations which are handwritten by HS Venugopal Sir.

This aim of this project is to achieve the following:
1. Connect with a custom simple web interface UI which can be used to submit carnatic notation requests to this backend.
2. The backend should then parse the notations and then save all of the content in google drive by programmatically creating a recursive hierarchy of lesson notes in the form of google docs
3. Additionally, this backend will also support any quick querying and searching of lesson notes by systematically saving all of the notes in a google sheet

**TODO**

1. Finish implementing relevant google sheets apis
2. Finish implementing relevant google docs apis
3. Figure out how to have each google doc created be publically shareable to everyone with a link
4. Figure out how to implement templating in google docs for the initial meta data
5. Finish implementing the core logic:
   1. try to implement the approval workflow as well
   2. ensure models are well defined