# CRISIL

**Steps to run**
-  Create a virtual environment and actiavte using below steps.
```bash
pip install virtualenv 
virtualenv my_env
.\my_env\Scripts\activate.bat
```
- Install required packages from requirement.txt file using below steps.
```bash
pip install -r requirements.txt
```
- Now run the main file using below command.
```bash
python main.py
```

**Note:**
Added simple cache machanisim to make the program faster in second time run. If you want to disable it set cache False in config.ini


    cache: False
