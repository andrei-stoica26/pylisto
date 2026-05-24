import pandas as pd
import pylisto as pyl

universe1 = ["apple", "apricot", "banana", "blackberry", "blueberry", "cherry","chestnut", "fig", "grape", "grapefruit", 
"hazelnut", "lemon", "lime", "orange", "melon", "nectarine", "peach", "peanut", "pineapple", "plum", "pomegranate", 
"raspberry", "sour cherry", "walnut", "watermelon"]
universe2 = {"banana", "coconut", "date", "lychee", "fig", "mango", "orange", "papaya", "passion fruit", "pomegranate"}


dict1 = {
    "set11": pd.DataFrame(
        {
            "fruit": ["apple", "apricot", "cherry", "orange", "melon"],
            "cost": [1.2, 0.8, 1.6, 1.9, 1.3],
        }
    ),
    "set12": pd.DataFrame(
        {
            "fruit": ["apricot", "banana", "fig", "plum"],
            "cost": [2.6, 2.2, 1.8, 1.3],
        }
    ),
}

dict2 = {
    "set21": pd.DataFrame(
        {
            "fruit": ["apple", "cherry", "lemon", "orange", "melon"],
            "cost": [1.2, 0.8, 1.6, 1.8, 1.4],
        }
    ),
    "set22": pd.DataFrame(
        {
            "fruit": ["apple", "banana", "fig", "orange"],
            "cost": [1.3, 3.2, 2.1, 1.8],
        }
    ),
}

dict3 = {
    "sig1": ["banana", "coconut", "mango"],
    "sig2": ["banana", "fig", "mango", "orange"]
}

dict4 = {
    "newsig1": ["banana", "fig", "orange"],
    "newsig2": ["apricot", "blackberry", "raspberry"]
}

res = pyl.run_listo(dict1, dict2, universe1=universe1, num_col='cost')
print(list(res["pvalAdj"]))

#res = pyl.run_listo(dict1, dict3, universe1=universe1, universe2=universe2, num_col='cost')
#print(res)


#res = pyl.run_listo(dict1, dict2, dict4, universe1=universe1, num_col='cost')
#print(res)
