# X5DB Language Detection API

#####  Language detection API detects the languages in the  request text and return results with their confidence values  ###
## HOW TO ##
1. Create conda virtual environment 
     
      ``` conda create --name lang_detect python=3.7 ```
      
2. Activate conda environment

    ``` conda activate lang_detect ```
     
2. Run ```init.sh``` file this way 

      ``` . init.sh```
      
3. Set environment variables for <b>FASTTEXT_MODEL_DIR</b> and <b> LANGUAGE_API_URL </b>
3. Then run the gunicorn server to deploy the language detection server using wsgi

      ``` gunicorn --bind localhost:5000 wsgi:app ```

4. Run ``` lang_detect.py ``` file to update the existing database with the new column <b> oer_materials.language_detected </b>
    
      ``` python lang_detect.py --host host_name --database db_name --user db_user --password db_password```
## API INFO ##

``` python

GET - /docs
    Documentation for the API


POST - /language_detection
    Detects language of the text sent
    Args : JSON [ex:- {"value":"text to be sent for the language detection")]
    Returns : JSON 
    
```
