RAG Application Setup Instructions
Version: 3/16/26

    1. Install necessary libraries
        These can be found in the requirements.txt
        Use comand: pip install -r requirements.txt (This should only install missing libraries)

    2. Install MySQL Server
        This can be done in multiple ways either is fine but you must be able to create and run a sql file
        I recommend downloading MySQL Workbench (https://www.mysql.com/products/workbench/)

    3. Set up the SQL Server
        Connect to your local SQL server (defualts are fine for setting, "root" user but set your own password)
        Open the database/rag_app.sql file ive provided and run it on your machine
        This will create rag_app, users, files and rag_logs 
        (if sql server not on) 
        Windows Key + R 
        type: services.msc 
        search for your sql server Example: "MySQL80"
        right clicj and press start

    4. Update .env
        Rememeber the file that doesnt get pushed to github with your API KEY? 
        You will update this file with your SQL information as shown in the example.
        Again NEVER COMMIT .env 

    5. Running the application (To better understand flow. Skip to #7 for windows shortcut)
        Open a terminal in your IDE
        Navigate(cd) to the backend directory with the app.py file in it and run command "python app.py"
        Flask will start a local dev server 
        Flask will tell you what IP its running on
        It is now ready for request from react. 

    6. Running interface
        Open another terminal in your IDE keeping open the one running the application server
        Navigate(cd) to the frontend directory with the react-app in it and run command "npm start"
        This will start the React dev server
        A web page with the current interface will open

    7. Shortcut Server Startup (FAST)
        Run command: .\start_rag.bat in the RAG-App directory
        Windows will automatically start both Flask and React
        Close terminal windows and web page to end process
    

    8. Login using our shared credentials for either Admin or User 
        As an admin you can upload documents from your local computer using file paths
        To safely ensure this works please remove quotes from file path.
        As a user you can ask the API questions regarding the RAGGED documents

    9. Closing the flask server and react interface
        CTR + C in both terminals will shut them down. 
        You can check you Ragged documents in SQL workbench to verify by using "SELECT * FROM files;"
        Highlight and run this command alone, it should show files processed by the system.

Sharing a central set of data one will need to export both the MySQL data and ChromaDB data

    1. Export 
        Go to the MySql server 
        click data export 
        select the rag_app database
        export to a self contained file

        Zip the chroma _storage folder 
        Share both the SQL and Chrom_Storage files with team 
        They need both for a proper schema handoff.

    2. Import 
        Go to MySql server 
        Open and run the exported file
        OR type "mysql -u root -p rag_app < rag_app_data.sql" in the command line
        Replace current backend/chroma_storage in directoy with shared version.

    All set storage shared.

    Testing the RAG System Accuracy
    Version: 4/1/2026

    1. Change the top k, top p, and temperature values to desired testing values. 
    2. Navigate to the backend directory
    3. run: 
        python eval_questions.py 
    4. Wait a minute or two. 
    5. Results of the entire test will appear at the top, the individual questions results will appear below. 
