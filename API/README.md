# X5DB Language Detection API

#####  Language detection API detects the languages in the  request text and return results with their confidence values  ###
## HOW TO ##
1. Change environment variables in the ```init.sh``` file in the <b>x5gon_rest</b> directory to match directory
2. Run ```init.sh``` file 

      ``` . init.sh```
3. Then run the gunicorn server to deploy the language detection server using wsgi

      ``` gunicorn --bind localhost:5000 wsgi:app ```

4. Run ``` lang_detect.py ``` file to update the existing database with the new column <b> oer_materials.language_detected </b>
    
      ``` python lang_detect.py --host host_name --database db_name --user db_user --password db_password```
## API INFO ##

``` python

GET - /ping
    Determine if the server is healthy if healthy returns 200 response

POST - /language_detection
    Detects language of the text sent
    Args : JSON [ex:- {"value":"text to be sent for the language detection")]
    Returns : JSON 
    
```
