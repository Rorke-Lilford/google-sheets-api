from googleApi import GoogleApi
import pandas as pd

if __name__ == "__main__":

    list_of_dicts = [{}, {}, {}]
    df = pd.DataFrame(list_of_dicts)
    GoogleApi().clear_and_insert(df)
