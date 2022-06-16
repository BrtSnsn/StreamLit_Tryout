# To make this work in docker
1. In `streamlit_app\database_files\crud.py` : 
    ```python
    db_host = 'db'
    ```

2. In `streamlit_app\config.ini` --> *_docker*
3. In ``streamlit_app\helpers.py``
    ```python
    docker = True
    ```

Finally, open terminal and type:
    ```
    docker compose up --build
    ```