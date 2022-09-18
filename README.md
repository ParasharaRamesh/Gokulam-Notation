**WHAT IS THIS PROJECT FOR:**

This initiative attempts to digitize all of the carnatic lesson notations which are handwritten by HS Venugopal Sir.

This aim of this project is to achieve the following:
1. Connect with a custom simple web interface UI which can be used to submit carnatic notation requests to this backend.
2. The backend should then parse the notations and then save all of the content in google drive by programmatically creating a recursive hierarchy of lesson notes in the form of google docs
3. Additionally, this backend will also support any quick querying and searching of lesson notes by systematically saving all of the notes in a google sheet

**TODO**

Implement style parsing of the notations. Use the following syntax when sending a style

_**Syntax**_:

<style:category1,category2-value1|value2>content inside for which the style has to be applied</style:category1,category2-value1|value2>

**_Examples_**:

1. <style:bold,italic,underline> </style:bold,italic,underline>
2. <style:bgColor-0.0|0.9|0.8,fgColor-0.4|0.4|0.9> </style:bgColor-0.0|0.9|0.8,fgColor-0.4|0.4|0.9>
3. <style:fontSize-14> </style:fontSize-14>
4. <style:baselineOffset-SUPERSCRIPT> </style:baselineOffset-SUPERSCRIPT>
5. <style:baselineOffset-SUBSCRIPT> </style:baselineOffset-SUBSCRIPT>