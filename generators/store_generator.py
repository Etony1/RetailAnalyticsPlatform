import pandas as pd

def generate_stores():

    stores = [

        {
            "store_id":1,
            "store_name":"Chicago Downtown",
            "city":"Chicago",
            "state":"Illinois",
            "region":"Midwest"
        },

        {
            "store_id":2,
            "store_name":"Chicago North",
            "city":"Chicago",
            "state":"Illinois",
            "region":"Midwest"
        },

        {
            "store_id":3,
            "store_name":"Dallas Central",
            "city":"Dallas",
            "state":"Texas",
            "region":"South"
        },

        {
            "store_id":4,
            "store_name":"Houston West",
            "city":"Houston",
            "state":"Texas",
            "region":"South"
        },

        {
            "store_id":5,
            "store_name":"Seattle Central",
            "city":"Seattle",
            "state":"Washington",
            "region":"West"
        },

        {
            "store_id":6,
            "store_name":"Phoenix East",
            "city":"Phoenix",
            "state":"Arizona",
            "region":"West"
        },

        {
            "store_id":7,
            "store_name":"New York Manhattan",
            "city":"New York",
            "state":"New York",
            "region":"East"
        },

        {
            "store_id":8,
            "store_name":"Boston Downtown",
            "city":"Boston",
            "state":"Massachusetts",
            "region":"East"
        },

        {
            "store_id":9,
            "store_name":"Atlanta Central",
            "city":"Atlanta",
            "state":"Georgia",
            "region":"South"
        },

        {
            "store_id":10,
            "store_name":"Denver West",
            "city":"Denver",
            "state":"Colorado",
            "region":"Mountain"
        }

    ]

    return pd.DataFrame(stores)