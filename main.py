import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


config = dotenv_values(".env")
print(config)


config ={ 
    **dotenv_values(".env.shared"),
    **dotenv_values(".env.secret")

}
# print(os.getenv("MY_SECRET_KEY"))

# print(os.getenv("COMBINED"))

# print(os.getenv("MAIL"))


#crud main :
