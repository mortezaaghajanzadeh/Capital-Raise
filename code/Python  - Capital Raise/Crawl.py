#%%
import requests


#%%
link = "https://codal360.ir/fa/statement/387745"
r = requests.get(link)
# %%
html = r.text
import io

with io.open("text.txt", "w", encoding="utf-8") as f:
    f.write(html)
# %%
