Greetings!

I hope to make this as simple to follow as possilbe.

Progress status: We have completed all 7 parts of the facebook network analysis project.

Steps for setup(assuming all files are downloaded):
1. Go into "app.py" and change the "psword" value for all places where accessing mysql. Enter your own password (or non-password).
2. *THIS STEP ASSUMES ATTRIBUTES AND EDGES TABLES DO NOT ALREADY EXIST* Run the "createtables.py" script to create the attributes and edges tables in mysql using the "friend_attributes.json" and "friend_edges.json" files I have provided (my facebook friend data).
3. Run "app.py" and explore!
4. To upload a set of files, first make sure to rename them to "edges.json" and "attributes.json" before uploading. Once you have renamed the files, go to "127.0.0.1:5000/upload" or whatever your local host address is, and:
	1. Notice how it says "No files chosen" next to the "Choose File" button. Use the "Choose File" buttons to upload your "attributes.json" and "edges.json" files. Notice how your filenames have replaced "No files chosen".
	2. Once files are selected, click "Upload Files". You will know files have been uploaded when the page refreshes and changes back to "No files chosen"
	3. Finally, click "Create Tables" and wait to be redirected to a new page.
	4. Once you get to the "Congratulations!..." page, click "View Your Friend List" to be redirected to the full friends lists.
5. You can now explore the new data files!



Known bugs and workarounds: 
1. Some(VERY FEW) names may lead to an error page. The problem lies in the way we created the "fetchuid" function (see app.py). The "fetchuid" function takes the ascii-encoded name of a person and feeds it through mysql. Sometimes, the ascii-encoded name of the person does not match the name in the database, so "fetchuid" does not return the desired userid. When that happens, the "fetchuid" function returns an empty tuple, which breaks the app. To work around this problem, we've made it so that the userid is automatically assigned as "100", making the url "127.0.0.1:5000/100". We've created an error page, "error.html" which the aforementioned url takes you to.

2. On the profile page(s), there is a link for the website, that many times doesn't lead anywhere. We made it into a link so that the entire web url wouldn't show (it looks bad).