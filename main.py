import webview
import json
import sys
import gzip
import base64
import tempfile
import os
import threading
import subprocess
import urllib.request
import urllib.error
import hashlib
import platform
import uuid
import concurrent.futures
from pathlib import Path

CURRENT_VERSION = "1.2.5"
GITHUB_REPO = "kaleam21/heejae__"
RELEASES_API = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest"

# ─────────────────────────────────────────────────────────────
# 🔐 라이선스 설정
# ─────────────────────────────────────────────────────────────
GIST_ID = "63f641fed064d6bc7788f0246ed32a1f"
_OBF_TOKEN = "VnVGR2gwMU9yNDFEcVVqYVZOVzVVOWFzempFb2Y2NEEzU2Z4X3BoZw=="
# ─────────────────────────────────────────────────────────────

_HTML_DATA = "H4sIADkN5WkC/+29bXMbx9Eo+l2/YrWuGEAIgAD4IgkQ6CvL8rErju2y5MdPSla5lsCSRIS3CywpMhRvyTLlq1hyLCVSTNuUIj+R45er1KEl2pHv45wP5/yTfCTAOvkJp7vnZWd2Z4EFSSk+t65lksDuTE9PT09Pd09Pz/HDL7x28syvXj9lLXiN+syh4/jHqjvN+bJ9vmXjA9epwp+G6zlWZcHpdF2vbL955sXMUXtcPG86DbdsL9XcC+1Wx7OtSqvpuU0od6FW9RbKVXepVnEz9CVda9a8mlPPdCtO3S3nszkC49W8ujvTu7xt7Wxd2nm03vv+0vFx9vDQ8Xqted5a6LhzZXvB89rd4vj4HLTQzc63WvN112nXutlKqzFe6XYLz805jVp9pfxqy2uNnXaa3bFfvFG8ML/g/R8TuVxpEn6m4Gcafo7kcs9Wa9123Vkpdy84bdvquPWy3fVW6m53wXU9Qqxb6dTantXtVPzGK9Xmr6HFemuxOld3Oi417vzaWR6v12a748v17vJ4Lps/mp2iz9m5xXo926g1s7/u2jPHxxlIhI1NzRz6efrnxeKsO9fquPjJmfPczupsaznTrf2m1pwvzrY6VbeTgSelhtOZrzWLuVLbqVbxXW7tULHTanmrhywrk5mdLz6Tm8N/JfxSKD6Td/AffZsoPlOYxH/0bRK+ufivxGpSG8XO/KyTLExNpcVPLps7miqJ9wVTgfxUisHw3GWv+Aw1nyuxr4DBsWPH+BdAYGpqirdXX3SLz0w8f7Tw4nSJfUXsCfzUsXR+IpcuTE4j9AKH3nGrxWdOvTgJ/5XomyxfmDiWnj6K/yvF5zuu24Q+Fk5OTZ0q8e+yysRkOn/sSPrYpFplxa3XWxeKz7w4dexU7vmSeOC3MzmVzk8dTefzaq32Yqddh76cODo19eKRkngga+UBr6NAq8kjWm+cam2xW8wX2ssl8S3TbRSPwvdDa4dmW9WVVeTxDGPnoo38bCE/W794w0534UOm63Zqc6VZp3J+vtNabFaLS04niWObKlVa9VaHf0fSp0rAfpkFtwYToZjP5ZYWSq0ltzOH/V2oVatuc+1Q1mm3V/mEKM7V3eUS/spUax234tVazSIAXWw0SyoUqOW12rMO8GsYDeirZF3PazWK+fay1W3Va1WLF6G3KQFxComhIeDUa/PNTM1zG91iBQSK2/EZ38pnpzpuozTvtAGXNse2u9ABYYHTgiOWISHCaAnzyS3mp7Asfr3AmgU5wOdVpkMPnEWvNRQPbBYGC9oBOnaBPJlZpzqvNYRICXSha9Y0fA+TiXG+PmT4UBKPs8pkAG0QYdB4A54sZJrO0mochKcJYVnHml2EcWmukmAuFhA/PhT0mcsE86gVgvgFeud1gEXbIBybXqmy2OlC39qtGmESZk6FaJMxeODXi12vNreS4csMf2zoWXEBudzEmxMpWbzuzLp1ddwmwpSm6cPINI3DimhnCDO/8VmvKQeh1oQ1y80MGosphTuAdhaJAp2kDFkpHFLDRySC/gGCFzSKFwLdxfUxMGIErEZCwKnXLRD53ZIqnWrNBZBFHiPCIKKHx57VybQ7NZiDK6vG+SGqPTM3NydIxJ4ovdQBhZF4pjA1PXHqeQUUr9FdrFTcbjfcNC0Zo7TNIRnazk+fmJg8EW67CoqWiVawvI3SMANjaPeFk4XpwrShz41VwXsw4ayjggUYR+SZmHBqzfB6UMwbVo5ureriIsBmSP5YzijplAWBCdqo9UCT5KUYS5LoC60IVk5imFkhYQ4YgkygKRhLTB5TpmZ2imDms3lcbALTZohgg/4aZo6CzchTRVTMOtD/JXd1hOVE1AahGVwN+bAdjRBsWK1aW4Ix7qyKxd84wHz4uJKanaTB4AC6bMSC62Owk9BvfTAZ4a1sQZJfkcp11wMUMzAZKlQjNwWFqAtEd9CoG8XFdtvtVJyuC4jwBWM1wMicTWTL+WwB28YKTqc6ULWJ5OFoSZ5S2iGm4soHV5KyR5S2M2h9Adk1rg0uf9h9GHTXuwDyysTTgQaOKfBD2lHesPgZBimKyOEhmabGuosNFMsgU2tV2Rv8UsJfALUBTzw3wyZ0t9hx267jJSfS+TkgJk7K7PTUAGIB/MyTHSxBNmwppDJEsHIA2YkgD0+RDocQlxwVXiFn0FEDlM1kcwWJEFTPwpqxquKAa8iafIsyYDUsFOR7Wuy0Amz54w10F2fj9xc07yJNWOKy+qiDfsQf9IFyRh81wim8NGH7OIkihKwYXRCDsG6EpF8p0OfhM0NpEgjXNIyI/9rxVk1iGgtUwPSM4GUVZdSWFctu2rAoKSuQD08sRKKpgYqyLJVteaDnrbaQA70V4GcFAphbVWfFou9VGNT4mhwfv6ncz/hCRNwvDJHcnu2BwNhxXAm3AaM65VuDfNoiTUmbV1DiwNzltgLrqGFSCFVbga7CymcnOahaszIAFKNdaPkLQaq2motQpOO0Yyk6eTZHWa12q7sKP4xVOi7MTNAwQlY1K8tg+MWdWRCri55bwqmPI1l35zz64K8R9AnnezIDL9L4K2XUN9QmAoIxZKwcyQWRCoiqY0ZJBXXq7rzbrApVIIaSKYy2hrMsiT6tCh1f22Sw4yuc0yb9mwOptjyuVx/xp8WRkK2ItA6OFYeA3lnRz8GmYE5tWFJe4biosu2KLsr4eqAPA59WxBp5Poe8+EQ66oPgM/OIBLIPImF1RqGAEkQE4wXQkUSzip4W4q5JEz4ykxJXNJT8h4YaisSmPllZLqthpjS8Ycqa76k4MqUr9GR0McfYVHyyHwmRnbm9CApgen6QND1i1h65wTHhA1J5NNDBwJrOeiQfwtJTa3dr3dKFBUCdtCO32GzhYAnYlaYXQ3cxuA+n/HFXfD97GvtI8INZwbyIiuojcUPQb0XcEEbLma27rMtSrC1zsUbvhI2fg6nkeyXqTrvrFsWHgJkMNRekuwHYyTqmY4ICwTQi8ZzHweXVxAdeVbZ/lLcfDziQwKvh8swwbQAH1sGQ9DrFutOFFWehVq9aAF2H1mw1WSHSquh9hAeS+YwDXsPZeqtyPuw5Dmu7g5VTAT6LqsVojgJWD7Ubk2cqVI30WlFrrrYcriV3UvSK7HFKCsYDJEY8n0oB23Zomc+g/1a0A3PPOjKyC3xygAt80OLIRJKutpvdqz6qI7uO/KrZqhup8EcNr+6B1IYdN4W5zhlWH4WidJSpC6gIxjYHwQq04GeA9T/NrX8OtrUYawML4U2q6EA92qNdJTxYKfSqNK2CKBSy+POxlH1RvdZsL3ohGWgevNF4LrRHMHB3RarPOmeVfKGuYVyca1UWu6utRQ/nIsk1EyMIsUEVu24dyP2/RV9LTrvtOjBLK7xv+hzUezQiLRpgDtdJTQFu9CcGSEe3Wqo1u65XzKlEob3iXBr/AVunSr+BEaiCOoRL2h7tX4Re7bTamblaHb4XAbVOEhhforcXZ1khrmsTvb8qrdFsYl+nyKhXzKijU8p+tG9FMRKGPJST0fu3YjVnftV9OU1l+5V6q6t5M5SRZ58V3I4M3xRQnE45a5JvyMqGuFw2CXBWaq7V8oIOYaGmB/tI4g/MM9Uvx2iDNrOzkvGWDXbAyO5lVbUasPbqbBM2K6b0RZwUR4ElqohxRbtW0bfsNKHM34LWMdwywOI4i34DY71qZOhJYmjOEqiiVJ3ugruneVMQux603IX9kUM2ZgtdFVvGTGn/QZYt+hFSKzo4QQANbB5NFEKDyNdpMVSkvYnaxo12wxoagMgdyQQi4IbORw3YYrvecqqZboW82jEYJ75U9cNffsZ8aHKzCLWHQizFJjupqjZHBm1sENDZOFALI8GcGEEDG6KFCbBsmSGjNiSews4bjiINByqPRfxlFsQcsK5ETceRNk9Xs/CN7Tx3EquYj6hAdBfn512wMWdbywYG9inGtdkgdeW+GINCYl61oo7uKxjJZHEFRFNoAPSwBRUxYYxEE8PpgsIk95ADqz3rqVZkb/uaYdlDLMrJJh+SZhPLfyDR6rQuHNAiO00bVQFmHBkZxX1h9F3wkrR6mm1mem9wEcO7WnMJR/bg+vwkFIt2pzVX8wzbc6CFdY3bcsz9KLuEhDpca2DAs0McTYs1edVWDU7X5mKDkQqA1qBCBh6A0KgUPWd2se508HtXmRdt0Nug7wNdKREyjntVhok4ubF9ZPDGuoZPeGIVhkwsgc1w+XTgsyRqWoSjeUMRceQKnR/sjMobnVFHw5JR3fgQjoeWWCoHxkmRxj44arYwOVrUrIyZlauv4v7leCH/xlGMj4/zEPbj4/yYAAYuw59qbcmqgIzplm2wsW39CQvMhYeWFX7MGIxeWtY///T7LUs7FECPj5NvhlfTwm9tq1YNPppZApsnmwNcoRY1Og6tBluXoaO86eMsgtRqNSv1WuV82a4sYJDdL7FYMpNP2TP/uPTD8XFWaiaMlhJbypBSH8xkfGyGNMVa+n/Vlnz8eUXe5KzXtH0g3YXWhTdJDf4lGo5JgPPPP/3hstX/+Gb/yiX4c6X3+WbvD5sa5BBAS4mpDAA/UeWQE/0vL/W/30xAC2MW+xwDKA+WjAZ6daN/9woHSp99oJwCGldhuGKIp3hgohhT5Y0Sk2bP9L5f76/fkXQNl8TJZLGYOzaaFBMHVt5sy+lU1T643uvOvJtMyJfYA40zRBQejccHnBF61y/1r232Hm3TiAzEw0cAT9A0q9A9Q/vi3eDmr4jmrz3o3fsidsPzoHgumFqlF4ObvMqb7H92q/do3dr52+Pe3Y3dW+sDGufBh3h2JrKMHMud7Uu9vzyI3RXSSplvvGvqkfp+cMeu8Y7tfLsFPQKp1f/4r7HRIL+gqX16MbDhW78XDT+61793W0zAmA1XF72KcSjpxcCGP/z7/3z8kWCgD2/1f9jY/d1G/862hVhc3jqoAe3fvTEYmt4h0kyNQ8neDOzSR38R3EmN7m6s737ydeymmeJrapq9Gcw/v+VN7159AK0PbToODXX0ABsPlAAjbcS7ASj+49NP/PHur9+HUfZXIi6QdRS42sYwEF/CmGrOGlZYf8Sq8EqkcZRtXzuZBAUICfh7lUeiCpsiK+3gucOhUCI8VwDo2yu77z7ov3ej96cHIMn5Ytu/s+6vt7u3N1BCXN6ApfLd/r2bFqxsIHvhcX/9cf/TW+HmOZmkF4+RSPkqh7PaqoBV0fSy8653qu7ix+dXXq6iFKm7zAuRSGWpMOoDvJGA5iI9fUxhUDUVI0pcpeF6xe716/07P2KPoa8gB0G++z3efXe795e/7t7e7q8Dbdbv7b53R+uuAXp3cdZA1tvfWv94//cgaNb7D7d7X9/q/XabHsBA4hp6eXvn8RYrwQbg3qX+3S90ympfiDSWt9LGYQZaMRL7VLNh8a+4ba9sZ/FEZxp/24IvVIsQz4wO5JyCUZWGLm7c6H0QGPz9amNBBgOiBDTWgOjATrdBHmTkzOVtM9tXkTX8g0kR820bpo6pvKXYF2zK6tq9FVLVIytfjFOof2+zf/dm0ToPypDTKOQPCjDjDvag6ngOMMlcC8bwwy1Y/nbXt4Dt3u/fuS4gBYl1OJOxmJZg9b+/Bb0f3/3d4/6XN63eN1+BJmZlMrrBpO0lWnwsCAdvOUMvFWaozSXdJZQBHlidrlcul72FWjdFu0tnlqUtEDJ/EEpYNit7cGJhUNsVb7Te8G4H2FfZ5FKwDaL1Pz6WHBqxrskQAtskJP0dfUCXJJP2hsuqne8egMp/fJy+qmKQdnq1GuyRpDaKCEKfTLSy3WqeWT4Dz07Sd02oArxWG1UYsNvri1CWTUyclkxDY29ngqXI1oFS3ObhpXwkxxlKZkE2Mil6l+/1v9wUpNAEIYZK21odLgs5Lej9+EwMBCyMrhiEBUyb3l/Wxxkb9R9uGPFhUy8aH/RW2haI4oq70KqDbgTE3LhatPof3N9971Lv4RX4EA/fgbzz+Gr/9udWsv/ZjZQRzeZiYxb0sgGIOo3WIgpXDdVcTNQEEIyYGops/4ft3SvXwTAgk2h0dodGKGPBqBw3dMBxzf7mqz0Nc8NttILDTKpE//KD3dt/1ckYIUTUvXR7ZqAfJSih+n/7qv/+dV9KxV6knSUAQxC4NhKUc6Zlgk1PrjiNvj7gPnfMBSJSd5QwSHWEBl+pdb2sU4VXrKnEvpcT2YR4lRllDdkf5gNWHB21OlSOtLaGMdRgze3FTqvxgrOSZM4ukIWX71mBJTUOs0gbY3RG4QbXfnlFBfNE2GUm7L48AEaJi/Zw7STKSCuMZqUVFDNNGBHhXU9fA4ptv0VZb2bDlVtzJlPNbKiBhdH/fNuSinD/4xucg2HBvH+z9+g7sEZu9D76BEy3TeDwVISoHmaPFUY2yKIn62Brix2t16cE0Hau1mkkEzjN/nDP727vC6DV5b9C33Zv39v54TqY888lUqB7u07nRJ2WD8VG2L4K5Nr95JZukw1x6++bh3vX/p9oO9BoqShuRRy2/u2ro8sXsc+3XwGjwRlZwvhTaVmeisih9yiO5Pnnn259qBODbRtYOw+3dh79eCCCKHb3BkiieD6HUKwDEyi9L+/jwMIMhXm/e3vTYupuf/NHELdWb2sDpnDvxkbvg1t8gSKW3/pv/dsb/T9uA79nNRJRpT982/v8DkwIC7Sz3jdfkzeMBIr0eWVNK6+gxQjr7r4mUGzaBzTAUb01XHqcZs2RQkjU4OQJsBgRb4TZqmr8oEr8uLO9bvUeXdr9ZGP0STu7WD9PdsZ+Z60O6AkpBpEdP5CZGb8LT2xq+nNSmMn9OxvagONkhAK9h1dx4WW9R2+rYYYdpDdFoCP1hBENTaJtw+2gU2Vv9uZAU/PRpZ2Hf0f5sy9rmJBsuheG2sQmWUaV2x0XUyTaI7MB5VOYIiZ48mIwPqPvUw467XZ95Xlo7aTDpKA+Z+PrJ7ThC2rl6ALOqWLI5n6lmwLlIDSSyRgaiar3o2LyZYAK0i4yD8qIsi9mBxXBZ5wIMewYdfNQpqeJsID4jEAT5dq3FmgaO397HBYV/jDXW/MSkjFp4khJYo6qOaJ4KLMh2pRHCDdazRYFr4n8FzwvJY/hmsgZ8ghoJ1lBdlDMbyDnwzSIN+o4Wlj9jx/gttfuzU0MJbnxde/a1d61+9lsdoBwekJjsrHev/vAYkPTu7Fpse1031AaNE4stJR2VH4yw8UTlSpnlgr7GLLMqA7KOAKdiPeGO9dxuwss2OsW6NnvXUX+AI3yh69GMjMJ2slWe+WV1jwPHbvG5xhI6O/6lx/sARyawRweB4Va7qdbIXv0YKxxboofiAUesYbtV2SObIyj34vh/wFQ7/b13l9+3IuzD7duMs0WBdf6Onac5WlyFIP5/dsmhIU+PlQ5jnc+iIkcxun9T7et3sN1jAvAOKTvmSS8wUzTwxEtBuRCnCDz8HGWsMyMu/cfOu/EO/QdIH+P9yZOTMrRIbk3KI5dYwARJ+sHpQ5vJa6mGmA0tytaGaIp8yrtTmu+Q+Ghw1HgeTqNx4s0V+BT0J4NU2vg/L+80b9/E4y1USWQQqpqKxNE7k16Q0r1l5d2Hl/VZuGeVOvdy/d5HMletezz7soBadoS0gFo2xOFUfx/N1U1m1aw/p3HB+JeGKFnsUMkaLfYrKYdmdLEVbRprzJAwGTWnPRtqHqhhaHQERu3fgf5Q20DV2uHXIp6UBySEOpWWxeaCtfAE2CZxCk84pBIVRbcyvkT2MwvXNxKGz9gBesgxm6/rsNAF2d2P7lNHLgvYzmsWPSuPKY/e1Qs9r+L6IN5Ms5CUmcNXT6g3cR46I/kKJyIs7qXzNN8KZ8tZKesZCFXmM7mJlN7dkvqlsxROW/+sXnFYhHBFmjTva+3ad9PJS9jVNRmdj/4kW8JDjJIR+i5poHwPls5K6v0ffJJ953vaWo9fu8S7uRvfWjtbG321+89vd5O/At62799FUYfBv/pdbPwhLvJNG/uTrH6G7AubdBJpHu3n14n8/+CsXza/Jp70n28s91/uG2xEznWzsNLu+/fs8Ds7n3whZXsf/IYA4/7739OejLfddva6G+8mzo+29EYInzGha+ngYLq4RHkGKIwj4LYff+7/t0vxuEltJd6WkTOP3kiv3dn95PN3g/r4zvf3ehvfg6fAnuRLJApQKnLD/qffo3qCFIelg9DFT5UwcGg3TBL2XuK3v/Ta+rxDIz/+U5+b+sjHuEwqE7vKgiGd3kcKBMPweLKETBr9/Y6OpuMvdA55eMtxCUZisW5+6D3YJsVCvKkelgogsSBc3bYzM4WyLXbX+88IvH2lJfjnM+LE0+IF7/b7G9f5e6fIN+YA538eLJAceVcZtpixyTT2vimNeZI+4TeT/zpqO7GuCpnwF6INBXEFWVAcuvfTr1x+uXXXrXKls0USbtEz0+8eeal197Ax+J4BbygNy+cevHEm6+ceefkiTOn4f1Zu3/tDsgDO22DbAAByD73HjwGfUHKDXjSv7MBa6z/+c/XRa0HvY+uwFes9Wh79+MN9hll6bV7vPyff8RRYeUf/r3/+RbIFv7qHozM7Z1HP7LJgk+URqW4ws+Pt0Bts8+xDgL675x87ZXX3jj9zi9PvA4dwUvWRF+KNr+MTOsVPGVbBYb+wbujz0+dpHd+T+Hpi8eOTOThKUGX3YYX+cnnj56Y1giAxel6Mo0U8JRtKGlEgae56eenX5jkoCWF4AW7rSxIK+zUycmjx44ZqIb45J4/djSv0Q87NXnypEDfJyYiOnmk8Py0T1Z4NP38kcLRnH1oLcApJvpKpultbcHEU5/s3oaZfUd9gmfOAk/+eDP45H7wCYp9/cnu9a/wuMAHj3dvPoYpr76CaQ4d0QDCkvO7jXGQpsGW/vP+7q0fx/t3rrPR8WEQJUIVOOlg6OChNkdA/Ny/aXyFAe/XNgMP4QkqNKC5fnA/8ApDM7e+CgK5/dedR0HIbE0MFabB2fiqh6f7Hvf/7x93b9/EAmxscQQeYwTk+t8Mr9aRVwAlxsfqq52HW7Dgjve//xp0beUFNoZjcWVjXMJTxUPvb1u717bGe//1MegPgXe7H99Hh/973wWfE7zAQ/ZZf+jPlnE2m/C1Il/kw7AA0ksiICYGxnFzdgvnQFjs9T4C5WPT+Grn4fX+3XXjK1BQ4Yn51ccPdv/42/H+1U96W7dNJXxJM77z7fYOFVIFbu/Rzf5nNwIP+7f/vvPdX/WH/pwf3739Sf8Dzkq+QCXpMg7mRO/Bj/hOl8xMgiGGilRXxZrynHAmmYQohEU6PRmXwipcIvoVgSbq4Ft1ZL68CqIg8BDP6t0BK/BG4DkqhJvf6VPiEoyD9uSHbSZV5BPgYJBCjAX5QykdnXr9zDIuoOfSFuUBwCWdf68sdr1W46TjdfkD2jZ/wfEcFKROpYJHjLpFfFN1Z/kndgwd1Qb8vsaWuRpoF4tV9wUo9XLzVRcbmHPqXZe9Xey6Hd6Kuqxnu6CRuMkUK1RZ7PzKhb9lq+lesF6gvQfUUV5crNfxRTKFCHcoo0moEMtzkhrLS1h4JB31Cj/BBnvlVmt4SP3lKhIlk4eeOSt0LgeBYQU7bfE8RTy6khGH1eZvztCFFG5HfUW5Dl53ViR92WNv+UXK34YURTd3ERuoOB79xdNm9AE1LzzAIb+cacFHHMO5xSblMLCgl0DDk6jFJqF+ylq1Oq632GkGdIyz8PKcdfGiJVfKkrXmg5lreMmmUvmXjreQdWa7SfpAW5bwPpX1Wq+0MP/Haa8DHQbS2jibg6BOL7Q6HB52dqkcAa4kmluaKedz7L/nkkvj4jO29yJyZzKPLT3c7H0JU1cUliX9YjkoxsqEMNVwpBtlkgK/atlnG4lSVeeyMTtjj3FYVY23Utm2Uz3tOdDjQtrO2eGiDHKonIYRHjWgckspUlZqc1YSGaM1B+Qry6N/BpSTS5nC1NT0sdTPj05P5nI/R5IEuvHmmZMDegJvR+gMlB7QH0u0y6ssXbxo26lsd3G2yx7k0nnA7pDS847bbdWXXAzVw0Q7aSirMKKixp2FN+cuXlSfYAV4JMSbRlHA9Y3WhW5yJd1Q4JHg48kTk6JsspNapXlc7mRxmmW77XrNS0LXUyVer43XU7/c9JLts7lzKRiRlWefVZ7l6VmjtJYK4nCC0Z2hEgeRYIMhlAQCvDFl5tXqdSDjaQofTXbd+svVtMWCSd0qYyvsJTwBsRNl8FE1AFybSx6GzymGDl4tDN+ytWbT7bx05pevkEzEp0KKY0LrU05lwe9LJcV4tVWWbVU6LvSFN5e02QFk5JxWlp1RruBHtMNP8nu+K4RJBforO9LKio9lr7PolggxzLfdrJ7EtIPJFtKFmOyQ011pVixJIQw6cqpJf4pdqDWrrQvZ9soFdxYjaK1nn7WCzwB2jdVg9KuyldC54NQ8Y2Ek6TtYKklXMltytcVnWTXtDwpkXBKwkLoMU0F6oJbQFmYqojxRyqnrNRXzH0ApbQWXC3ho/UZAgcWLYGnPlEaRmodlQ9mG01x06icoL07KMj/n66Go7XcmW3eb895CKlJFqLSasJ6pNYITqSInklaRMp+/BgyVOp6D+cPHx6CnUF9Dz6G/XIGxSNiNjwtffu/b9/pfXtK83Xy6Uaq4ARMuoeWUSxBKSA76mmLV1SkBoLjfBDk8xOCnnSV3Hww+gKvxmPE7Kvcmia8Fjw+pSNyclEwesxYbYWWgFW00HRq3mECJhZMqI6fEgDJv14vkPUsyESJpq7+T4nSgNA2n8pDjC7IV6gZG1u5v37HsMbY4sFkwZoMhZYHiNsZ1YVBxrqyzr7Ruow52y9ZxpdXj30GnSGLLPrIXZqGRf3/l9L9nQRJX6WVaaKBOp+Os2GuEIJXFadcEvYHT/C3xvXSIsz6Liuxf2wRu731zhQJXfrgCL2F+wqLuZuut+aQNslv6QqkoVPy69/mdIii1F2azpxdc13sVVN5u9tetWjMJT22cmAAGlhQrSYZEOQfrwHG9NCMPPB8bU8VzE7DUCp6tcSEDKGvuc4aNlD9NKR1sVsxOzZRzFy8qz1lFei6atBidRIvds03eWoAKhpat3tbmzsMHSIcmZ901gajqmRfFM8AeymPbYpl9LLv37ZX+ezfE092PHuze/gpdyl9ZNtsN2r1zo/eXdZt2ID7xe6x2WYMc7rjaQujtRJbV5oQBEaO81DAAsesTzueqodQzkcNMvTXOnMYa3/wnHijc/LH39TaRRqHX7u2N3o0NS8XWJ5e/uL3VFfiPzJzD2DPEhQq5h9A0+NpA7GHkjk3wZKG/9VVKJTv+Nwvy5Lz4uqaPBlHvAhBuT/O5IyTWolerd7NdrPCO13rn111Y5v2eBGl6Lr3Kbjgu5kHLmQP1Ek3nlK9udHiDMwWkEszi8gBgJd5Bv1OEmttdrHtSjYlwA/CFuKt1yrkwsFvdQdgHyQjAovkNyQcFAlx2uANWxMWLte6rzqvJV8m2TOKjVCqFfODVmotuSYFCoXjcpuucLZxjZh18b6ADBs0w/+1E4C2Ybf7LSe2l2gR6PfxyUwEgTsMrSzyn4WUOH1Yqnl/laKAKrtZlaVdT7zQSYIMXLyLgMsoz6gRY2syR1ruO0a12mBrCMKeitP1PRnlw7LPtxe5CchVxKOKvNDl18Fea5egpSp8IYJBKY1eK+AuNOtkmn0mBVlkapxRnv1BLbDXnpYa1Sz4nUVYikcZMOArHWaCpdF0dC5ZyahgWrFQcLEx+gGiMIkU9OxnEJ50U2aQPkdVB81q+KPkeC9YPgxqlVBOTeJ9TGKvPdVz3BLfEuJ8VlFNgocBDZpgFHpLZJsULOXQJSZbYFPVIikonJSqsixlEOz/qhps8d2+mLdRCd//4W+ALlPO+fGFqGW3Rnj596sw7p0+dVDbY0Nd990Z/8x4wE4w6Rb1QFIJdtLG70pfeX//Wf8N6Lb3o2jue9jTNgV+7t/veu0rN87U21qPFMPQYT2rcvcFc58GXDF7v+0u4G6VWCn5njiWgy/3egx9DTbA9hHDLH2+FEUJ+ldSrNV+mngmHOA7zKy2n6TvITUrM+g/9Kxt8jHB4MDsCHstLsuP94/333t39/VVQxMdFBMnH93sf3sKiqUO+74J8dtBSrnQo9lpiWkmI7XK+/M0ZRDuVyftl8oYy0E+b9cDGzRLeB/jMemEr3bB2tm6ASJFrODQPokhUBiUI2kLZJIH4a6Ha85o1ZuWH65nKcS5J8yLzxDNQUjoq2o8UTAplZYV/EYWpzER4he64FCqfHE+Pz6dNlWanolZkpcwRv8yRYYDFgKvBReO4Ff39ZoDLv4TZeyUw0FNZtR6tu2ImcVcgm0ZlNok0oYghLigSQ4urD346q2LCwRM8AZy3tTfwk1kmL0zYc4gjom+ipr8AsrZFE7pWWHtV07YKkVpZ7fVFTJ7Qdcu0Fr5Yb8H6HNLmguOtgzi52MGreYwQpoZBoD4gtji9DzOFVSJFtqb8NkN2kJM7jDKBLSYkCPr/cQV3Qf2XsLztPFq3VeNIkwKssmJgEgJpCze7QCjRE9EoPN396Lc7W5foKe+qYhj5rk/FxQrzPGl8cfHi2XOpkDNzWTozDyeXs6Qol8uE07PPLmfnOq0G6Sip0tqwhrmaRuoY71Sbd6SodKnCulEU/QFLwX8p2yvitPCbXPMFqqIx+1yqTfMQlyLj6zxaj8uj9RONfTBXPcBcCI34Cj+oLMXwH5mZWLUkKBv9b9dTClPVGf2pPX/YyKW4XGMbzKTnZbuthuszQ1UyQ1WwAkHSBp8MHAYmxaEoI89bZio6w89GE4s0c8Qn/qBC75meM96/usnP4mOY0+XvAtJPFrTB5mJPRAV8kg+VyetlVEvMd5Kx9tiSEdANNA31rJM7Z8FoWYtN0MVrTbEfJieKrzqH6oW6zFplHFy0cMktS40DtGVYXstMdfFJkCd+URpCziEd3fSCFEbTC1oD9FkC9hMgrXC/M6GbuYyrHc7UDvJ0JK+KZAqSR1UE4FueDPEAn2nLFCBJqn5KM3BU5mNAiNUcldMUGzMIkZsIqYCFtE+o3LhIBUysOFDXgqKNJrfCElMBljgiWMJKCvYhpRaNrI9vAOt+QpH/d6/271xPSbaZncIhmz2ij3j1RHDIoYRhyKtCkFVPDBx0jrw/6LNTaaqzT6k0OzWCSMI2uTwidHx5VD1hojynvr5sMyOWJc2zMlbAGMWuaUzJtPC05VulWCTAY7KQNE9poddZRhZiyJORQD1UzWZ/QQ7Y/urXklYw5BHQH+iFQ54C/YFeWHgQ6G/pUGj/VtEZUpE6DLofVHeJ03TqK79xeYSUW2VBOb7LBEeatqx+6bTRZ0DbzMMCITrZgMsJuCocbADlpUVy3l1BQ4r4cMy+aI91soyXfKOlwePFRHCFEp9yRLFtqs6KmGnmUIzCOcWjfFjt31nA4lzKCj3CfhPHM/wkmwsc0wy3bhEDfE67HgW4oXssC78pLu0k271fXeO79KEmsgwCRejTx1RUQQntLHxC1JLDyqDjVVjPvjOrq8fEWdZrs78GQcuCOroaUMPYLfGxQxouCeTxiIY1U7YKgeWujhuXK8RZOHXEfnJAHM1J9pkT4miJPjz77BwnND3ifLGmy0+1EVVs4gbiFmbYtnpf/g4Fdu8P38I3SpxH0caU0ZacMprknAXavECslNdFasNZPtmUvhj2Hycd0L4L1JDUN9CtmlpVrgSozanFz1bPWTMcfmqVfyjrBUoCsbLk8GrK9zmLAWb/iSFWhfaSzsJLQRbWBpOx8ZJk4yJvHJ7j2XO3ajQn1iSfSQS6GFwoieCkZ+VYz/L2Mg7/wAeWv/YhUIRpLl3IBbb4MWk2l148KzuNfjjyM0LSSUEaqCEDWlaBgV1An0fCc50V81ipR31IF/j4fZ721JbRfGxskHEWvEZdhmAFGwsxSjdd46xC9cbKVkK7yi5wU6Y9k+BjMJbQUjHQQM22lmXi3UxirDaWsMUIBlJC0AWlmNDGHlchspQQgKQGQhzPqrvLxXzgxl88xzSTGOsyiZ44Pj47wxNT81qma28SYxjU2uU8mRpLWP/9bxYCYawxlsDDqJ/d4kMgMwexRBQKujx5o38xR4DcZ6kD55CvKfkAE3p2MAXQhLjS8wDulJ4yHFxLDco6xq+RVgZWhu01nLYpaioRuDskMVaBUUqMsVA87OxzCRlbmCgmEkDgGSok7xVJ4ELNQjrslE9Pkd6SnQhL+AtJZAyNlq43pcUgIj/HqssyOKjn1zpuo7XkJsUFRAFJEEylK3UYGE5aeXIjzjwKQJ8dFCqEk8EeqykKBZQH9b0ym+Xzy1+L/HVPEcddXRx3pThGadtF0X/xYp6J4S4Tw2xTjckiNg+ULT/q6dhYKSCHRYjZHsmOSolCc4sLRNYYhjqh8DMnevbTbflRVDymn+xOuugQNyTBxg9Fb6Fo5ylBVdFOqzDPD9t9QjoprQiykbNM8QPdMPSIFFIYmIByNTjCTE9xmzJF6qoqhWw0xRbSlC4BGgMkQAMkwAz9sZIsD2MRBKrfi8a5sUTKPP1pq0kLT9az3qYtEcNNRVmoHQ7X6yyz7RB2C6STjj/NDQ2F2GIE4jPZLwauQnWH8xJXUAWYZ581shffMxpKBpELOBUILRTgx2xxAYg9VsGvfM6xE+1+cs9ARKGeU/fgiAQcABCHVheMYiRxTpmzhkmIqnEcKsOQ0CrOUCohccZKa6OIvQF8GCH3/BHQ8wxgdoKEPcZQGbMTIk0+HyRdEJolHl7a8GKtDlYR/FLiFigogZ+Vwvdv0IMkh4Sfs60mVkb7SpDR1fYpWxTz6AeZIqg3QVU7egJjSJMuT8eUZTEVKdVGxrqcl8np7vsWHN2boijLauwk5fjf+m8YbN375j93/3g1QktWfFawQvPuoj3N+EQTeupkRHnAnQZh/4GMGA9pAhYRJXoN0D0TAxs5FPSXAf7ZBaebhNopRhXsAS38Hei1LIMshmVKcukWRhTHWuXhAVysX5E6kIkHQNFuexwskeNgE2NGcYnUxdH29Qmeg+KwvCbGHksqTJihkilelAI+U7bPrwPYExsCU8p+u6nl2rDHIutAI1to6a33/+M6z8nRu/GVLQ6JIK8DUGW2hKLK+MSZsRR3Lmo2osQbJPu5gsM1N+YBV9mwG8uQFUh0Q0as5tMVSXIDxaivKNW0BCe7n61jxosvfuTuZn/+AhVZQkmWSMK/5cYGng/b5WEvgSoGKdZGSjP8c6JLoun5xbk5XIZRIpK0PKtexZrW7gE6F57NNeZyieJVeI1ceQoz0iGLuqCCJW1mN9ppRZauYt46ISSxzS5GJ0qBHX5Fjgz8OavcA5VWL4GKxpYcmb8pD0Ca1rTfGFCvdpx5zManI+9mUceAgi+4cw7Id6A41A5MTKomdqQjgdddEEgK9NSqBkmIijjAWu3RsAzAphHBQB0xlYzjYi4gR0cxN/j11ygF2YwRlgo+0ZSI/3PR7awwrbhFmaTtrLxh22BVuHXoW93QETyVA8QUZGIO96XIcaf7t+0xQpBZU0l4gh7rpeBYSsgBXcO3lonF2SlStFLlkeyxcpUd4OPfZ/KF1Kr4UiY/Dx1pQT1LKXY8r5YqiGKZDBSTCGhnH8VTa9D8tMn1wzOQpvRzhuJsTVYedxUIhA+6Gg4KSc+xf3CHbHffPPWPnAsJuocFeMS1M3IN1tdOyz/kuXboYBSDg1EL6FBupRwTGOfiCJq3K75NXGbs8oJ4zUaQ7xSrAPAEebPqdMz1T/K3NNOjQKgn5sxgzqhn6qLACO+Gob6yZhsqznec9oK54n/BV5EVSY2JQJkd4IysKrfWDVVZOFpkVYCLymxEu6f528jqdKovYrTp2N8QLqk1a94LreaiZyooSImFJO3CUkhhK9/qAo2zLI6kc2GTlhJG8jqsWGUp+Mrl/HOBKpl8GiRoMQpQJi9B1ZqVci7tLrfhN4I9hZ9IgEfZKWQlBw8ZAJixsjRNiOAAU3nErWNoIQZQbmdzfEJQmD/AK0OjGWglXa3NzZXhQ4ZXkFa/V2Z+OtaX/bvpKt5ZMv3PlZPyI+50jhkQRK+ZWwWrvMzdaiB7OjUXBsNLDdqbOps/l3HgF+IgNqCOSqi4Qed4/+bUyxK+OJ+Ue04+AmUDIBTzklgVIES66RwwOZoV4ZEsJ/3PRJB8qekoLx3tpYFaXqs9FSRUszIyoaY0QsF6jXB9AuG3IG1gDJ93Ol2FnprN33ZqaswA+n3wEUBJL8Eo0Of8uTRts5SDWVbSbWBBJZcJ1BiXI4gZOPjCLF2p2k03bKfNngk+rbY80700iTFCAp2vbM9Eu5MVK9L15Lj74ni0wUI7WQHgsyA88M4Y2/RGNstS1yfGoH9jiZ+VBmJhxgXj0ZqLDbH/BpRJ+TipWz6ab1iwykteo87GNjRY2k4KOfPEeFWanhyvwMDAq3HGMUNGBdsUw6J2iZ7D+nweO5SsjeWV3oTKsWviKR04+svZbiVWFPuWEfUqeDddgryxid1PrxtGkIqZh1C8ihjDAcNFNQPjBTOa7U7EGDQTHbuLDcwsyS/+Y9uNY8ESGbztSe8FPhU3y9/Z7j28iunhmZjimAcKA2MBAlUVd1gpCG1TcbpDGI8EfXYLA5ExhyyMJy4wM+Xcc/aYXYROERR85oNhnd9nN2gtje4GJlhX+wHL3+B+JMbiS3q2jvsbCGOJnW+399+5q5vDegXkhbWcqEvXqACFO6jBjiVEX+V7hfrwaFjfkT4g8/ki1vvinmWPKVMeuGAcStB8H7N/ZovjjRRRcee6HTW2kcRAVi6YeTlMI+UeM+3eUEyUq7IzCWtcnwa1PBp4TIS4+VWYdFVUZw2Cgz1vt7rwuOI0l5wuu1icHrMHtkXCpGznJ3K2xXLisi9APVbEALLi8qCNiDfIHrbalv9U3BQUWZXN4+07umxQfys16+48KORqU/zJTLjecD4YPBp8T2330z8Bu1lnWm1rSoy0WNgkcN1oUEyOEc0F1O73oPP5C64Hmg4AAdu7ulhxVX3Mh+Aoal0657ddjzbLQ8PK8kmFM56UCQWYzDJpHD1IFe0c5ZXT9H1E9GCU971r7r5yibw/lAJsEvFsWuybklCLdW25zF4gDCLLspe0C1WsBS+zdL/cG7hjnkvn0jD18MfHY7k8PZWurODvTqs8Bb9r5YkpbroeZtRcRTiz7nyt+bqDad5K+N3pVJKVZagK9QAwCdDXX/55gb3FvfrTTJ14puDiP1s+5wAGAKwNBph38J8GcI1b85SGzWnOQ7kMhzBeKLFRCw8+0+FpXKXGPk59/rls3qDBc73R3A10Qp1psZ4YKEW4sd9j3Xqwb9SW2i9WsNytI+88EarRASh3fhgrcsHHWRG+CT7EyoqrhEUUcoIL6+tIahDtUeUW81hZh/XxwNW4mCtpjY2VE2FpbbCN+ItI88g0thHWEgclDCZe2qya87K0LJFixiQU71dqYCWgCcEnFTygSK8ZnUa6L3HEhaDi1F9uVsp70Qr3IPqhtVN7W3n20hpmYnXamofDsAiwpJhDIvWR9Rm4s9VzKfmpvApLSzGXBq0RfmMTlALP6LqSlbK6G4w8Y/5L3W3mPyf8xc69v5xgGGM5rGxEXLE2zS/sVm41EJcRYvhsad5pF/PssseSft2BosUOC58V+pXC4uoNCvyKhulcTt7LplgwjEP8KRKzVXHJVN2d8+Ttm9zMGIqH6UZKI2Yvc/NKxyxChYTywpbFwTqL6eAxxcNntzDzxCf4GzDEXBDffM0yNVMW73um/dgqujBwqMeCY13PYKoQNG0wF81zMPCLYC/hl2n84njMQCJfQtVXI5VsIrVO1/Nzwob9wul8Kg2tUbR/ZDGYdX6+2nQXt7xeaF0oE3D2YiXpa49q2lxyMb/iDMFBBc+TT8jcE7Xjor0SZUWIoFPFrdetlrcQtC/wHU55MhAFMhkBciw/VgvafSoC1XK+VD1e5gQqVQEB39dU657BdMFlL5ASGEaH9/HZZz09JzB7RV/FO9ZreFFVjhc1ylI0lGR8fkSvkTsYJsASlMBYMIV/iwfGSbzAM1cniVUoED4RRSmFl3jMSbLaIKd9tYECbiaXisAIXoKxxuYUK5vyYbH6ZKZH1YeX9syYrK+6PBKlNY0Wiv9JhrBRsqbkkUxSjjAfu9TPjsD/OnPlgbnKrM6+eatm4KIwonxFY9Hp4bVe3/AbYa3HXA/szp/+vXf7n34tZz8uwmDXRC3JYnBF2nFa1nB/mn06XC5rb1KiAzLZqV4bLCxWGT6odSkB+eCqTX7Ynn2SKeu095S3bjAYkRmdgcJvx0Pv4sA40/IhzATemOrzJ5QPRA/SZoalGImo+MLVTrGTrlWXiyxQQHS/k1qj3Y4BJ5u4RlOnpOYnWw1Qddykwx8zXWKwMhHp08iwNFXDXBs8dSWIFdlJ4VEc5w5JxcOYMvhRonSVaU0xMd9Y1G0ExJwey697w/glXfyOLnElkWmpN9GEdY9c6oriwk4B6UX4fbP+0SBtFimngUoiPMVX6UDNYY76o3RNcCDYnvmqH27LaPrAe67AS+0oohRTWqUuJ0qJIzh77Z1+1GlQ5/K5iN5po6V3lWO15xNKGpqwEO/hoJJyTEnSSD0Ih+qqbSaXfvmwvENu5+Gl/nu/tX1kNYnHFnGCoJCZNrlMdB43Y0VrlBmrcLNCSnL9ITjE4vWw9kMKuX8AzWRV/F9BtXtf+J9pDcD+TGsY7jEkjYBYZjmS3068naBkhfSBDl3RJ3lRh/x2pkWf1/yGZ/rbV/GMyye3IiSSSRZ5zmzdFb57+gJ/UF7Dnw5+nOldvtf/EuY2fMSveA/S9+v+V8GA8ok688RD2RqMEju1CUKf0lXIar2vb/W++Up+ZR/GEYdxgc9sq7rC1J8ofx26dhTFulPGB1laENlH+JCudcmVEfJVaDohdb6KG2Hc0CdP1RTpkF6V3mluGZaEnVRogP6cjepn0UYllltVrD1l0xOh+4cWvWr4gvf8FMi2EoaPztVbF4osbq1ENJQPQaOstbu1bunCAnQwA7ArbrHZYgOaEOH/iXBz4Y116gKrpO3zhzENjSZtuA02m33SqAZ0kX+DxT4lKCXK4aZdhu/adfxTttGUM9j7isSgdQKgd7J4KJHyNg0CZqJnYEIzBTujX7WOF/2cWQYlBliNrCN27a6cklYkEKvqqjePwzcXprkG6vJf+/c2lSsQcRhxjiiHXKWtwKYL/GWTOmhTDLEggpk12FaOfyp0D362g1cb1cB/UhsFdk9TT9SPDdgz//zTrQ/1u1nD4njgpZnmZk5UxdEJMGvFdakDNU+xRxMki+4i4rSguezUa/PNIttWK4lz5QX08pmWWnFmdkBqAbyRlP3EvCU0HkH5WTWWCCNwI2hCbvVYqyGPR6QzE/touoBeUoF/HXS4XhyeP+pzkeC4mYgLYnMRWgylDVCIqrgNw0COhm+1NTkm2VadyToJzgvVSeosei17ZPTZNb39jav9994dFXcNIq0LUZ35eb4Q3R/V62RwxwzXe+TNj71vrgxUbmZkapZB6g4Mqa7xmAqp1zPvTTNST+6HtzFQEZLnBTGtmNJeUdxLjXFFf1m3xuQ91fS6f+exuNziy+t4A3P/8paaNqdSWWws1kFVqkYeSfbkCuGJw7IdnjPHC+6D4COZRkfZZzcsPJ6y8HjBhSdCp1O0opF1IazQ+/I+zlGmHq6MJdjg+6rEnjQlwdxRyk48oKHpw6EqIxQF+ID0KKlhjqTpsNUtrrLjnzkdqPBIr+7ILlQefu+fQ6ekLmWWfUq4fhvlfKlxHA8QNTSPvtHR2lDOkNaezmbqvqJ4Rm+MJ2NiGUMaxQZteMIPnhIows9aSnWykwxHU4xXCzfXUJojF76mT1J93CeOWR8QCNd/1eWxBYBIRkCUnk5iJRxE0UYwlYUfLwxwCMUMa0iPA5aSp5FtgLD47NbIRlV475FPa39rYx8QVTnh77XsCaASdclgU2xm2NIzyL5B4ZoBS0cJEz4UFQU/MLTxs1sUMMkCN8ct34gQ5/QSvSvrKcN27YLTkbGOSlAjndwR8VhK7OIQV3AElsMsH65gwSq882g9so2nre3uUdflyuL2nVDAbxjI9BB9MXJbXszxAYHX+0B8uJI+vR9F95Qadx45zgemthtCr0fpEHrIuWgdLgaCfdarKoJAPB85ujqGpk/yOFpz58QYUIKP/yAYmyoYk/Y+JhebManMyP54eM0fImxSHZH0xqlq06ojpARTXfe6zmgTaGRQ6gKjsfQIkEbjq9i8JFYW+EVE9jnK6DkLBlYH9cRhgbvaQhEVuMsDdllsPP+C+7FNASvbmpvDC4awQGYiVxI1eAR9/mguTvzv/6/aPiHVtuEs40lLClaFz1nKbZWkqy4jFEn1WnSowdS6NNPFKCsQMgoHWy7nUvyjPIz4VlnlmfRLZY0h0rCwv4LB2/D3jXKe/p7hf58vF6Yks7xVfiuDZfHXG+nKS+WX8NMZ/PU8MWYoYPyt9Esp8abrdVrnXR5P3JmfdZIFaFP85LK56RQLL67Xmi7xLuuAHqZVnqQgGoq4xMyx1TNjlZcylZd+XhufHBRRjXineUg1NsAfjVXeEk8ZfslQ6LMB1QmOKcrZso1LptV1mt1M1+3U5vwY6TM4mWTkLhsUxDOVLqRXxib9COrZC+XKW+P5ws8B9AT2mfNByEfT0I4hLpd5F7BqDf8WJrWp9hKzOsZ505WXWFC/Gtc98fzRwovTPs40dMuZ2QtpQVuEk4bv+FefXAgezzsNAH/qxUn4LwhewkYgCBv/ctgxqD+lkf/YIOqjScXCJbFP44X0S5nplL8fEosab2WO5dJH03lKzj0cvakRmEPeffdW5sh0Oj9lRMpIw7cyk1N7Qcpvmd+N91ZmIs9aDrs5RJ4FuX4FUsdH5JSX93JTaFIwiXxkfnmtWiidfGSmea2aSCwfTDWvFaIVnvoWSH8vbvbWEdtT3Di1gVdDyxsL9gAE7FuBZugy8OfUbmSU9orKC+mraDjnRS/fYOnzJB6Y11bkhOHo4CN9EXKUwBdFfSYys6TNmpeUPRfnHJxs9AlkVhJPbCp2jaP6OAOnF7QzwGsDws4O4iwwnvSj7Grxj8/6xD+QY7yAAbvVIfY5ZMkJB9L+1U1x4ww7+qox4XM2v1iIXWKMijZ/IFLZRZ6m9c/oEq0GHdTlnh6dpgNsXK/VLmYn2CEFlu3b5Oug7Uw67tMVm5ro/pgSlusgaziUINwYUOTnKzeSjmdV5mHUShxRsCgLJOLFSzKLohJTJO8pwttcxG0wNCQio/hAe1hYL/zWx6sbuJnKNpH54Esp0lzkzK0LWe2FJmvZmzPIk5gFVik3qkBUxN1YWYWLLw9GUmLv33sXby7vf3qrf/vvFruNFy/CxLSJdDfRRn/jXb5lYJUHZh/4lwucf7G8+f+UuPlJSZt9ChvrKUkbTbyEZQ2lrDNciUSJeY33INEbTYboSUGNJysku+0jmOXbK7vvPui/d6P3pwckDz6+2b9yiXIBf3yl9/kmPNu9vdH7ettSc7GyO7UwMkWEpLCcqx/9uNfglzcpA54fdE5o+DgEgl2GRTkM217Qt739/YV//un338lVgt+BxyOOmK4WMzbqRLX6S38sjaFLA53MhQhP9e773/XvfpG2+M3MeEsOjtSX7/bv3eQNwGj11x/jMIQppW398ou+DNQTeTlKhwYQV4RZGbjceBaPacNddkucPjbaK7nVY7zwmsLdQIpprY6w2qYokT7LHhEwHDSYgTNT0E/jrD2Yngau7hZ9DLR4QL0MGIChfhovYDuQfgavIbf+8f7v9Rt2mRQR/Q9gckD916EG+h+MlogzAbT76CKF9ajE4otPMqyIpAzCj+GgmbXV/Zi11dhm7bBNj2pcezfqWKIhjFFVT/azf1vS9JhfL3a92tyKyHpapBDozKzrXUBdaujBDJPILqRsX6XYh9oXfdQ77sakph2OtDEZ0hkNp7sjDmsaZpNihPHllcyQn4IR9kTViCelPyREguShqqNWQHeASc+7OaJkRE9YBHtGGADq5j2FoScRFDsykpISQ+G5IXEeEdYIRWvsxTunNRo9eoE7yUAYWEfDBlBILuGk41R5Zm5uLhQbqDIBHZE2xQeG1DwhWROJVCkqFFyVoaoIVZ5weYkPzNenpUYQoIaBsWdGl6Wq6BD7++ElKirW1Bw1I+K/fEliztE4JLh+qPrur1KUQcTK7UWf33tgp0gPLXc89CtnzVfRarI26iDLyGFcqtIXcNjt7YSI6NswOZk8rHQuWmc7iLMhrI/ApH/tffO1fjgkgqfk3srrndZcDZM1+6gOXsuSnWxlsYNhEplOtr2I9zB18ei63MWPFgAHEQe3Bz1qT5rU9h1r96Pf4kWx79/o3/kuIKH3qBkpFFeUI9KGitqRvcigLaVyMNaGvQqvJsHsIMpIDzm8wJKZE3+YBj1NScP87zO555JJVn5cYQ3KGpb1Wiz2vIAJxAJnBpSZy7DT7y8dFjtYCJCcR7r6BxD2EHeIZw/uXrHEWQHZGfNRmKCWoExmHpsWVVJBZSLeESM5EoE9nIGw8wYSCdiUakdyFfsIrFVvdbsyyKttZLu24Dg0HVmWtJQBpfCTwWcWDKGWLI1UUGPhkjjyOIMBC/VYw55WNv/uApKke4iKVpMm7GxfokNOUVtxQyWVMcQYFj262FG7iw5veZTZGJgxnLbsgRuBoaBmlL96g3lqLkZ6hVanIdIAYCg3vwnQmG+h/95VK5AIBA9L2eHD2wVKTDEec0VX+AeWnpOwdLQadA8iDMqgo557GBgUITuPt3qPHms96X1wy2I8unv7HhptygXRXJfA5Vyr8uV1XgVvLe998MXubSoeb/uWswNG3PPeBjNxoD0mmVhd08Tg15oY55UZZPBMAgXUG5KPDrkhWSznvuT2pRTDvsjS3FGCDz6mcuzYFTP+8HFbxZBUstlquuJSZvo8dFMolGnvf3ysKHdsWVWdSRF7wKNngb79rdW/d7v3aHs/soAGigUjFpVc172H6/1760WLrt/+t1NvnH75tVfZ/du4cyJKoRPo7k1e6sSbZ1567Q1DIVCL1ERCvLh6YRJPTa7XU8/Z8jrGg+RYb/jkC/vkjJIKv1BMepFnaoiUEiElv1Fr/sJdUU9Hf8llNejZMY6aq0tVRJDy2wl2+xS7E/HthOEWpbcTLB3F2wnC4Q/XaI/qwy2Qh7sfPLZ6Vx7DnxEPviuYMSP0JG5RvkmoJHHPknV3XW+KXecXq+Phach4dMWt11sXQAykNNZlj6VkMLxSMG613ebrzkqbjco/Nm7jVYT9z26A3aoeUh9CiSru2HYUsHg/EL//8O1E75uven+4Z/G+r2/hNYdSZvPbDGFAUhShixe9obYoClvD0sMYQ9z11UixmTGTUPTNb9oSyqPc6UsgOzUdA6YXLI1O1gNWkDcjHaZkbav8klbDuktegrtXevdo6fnzj8xDYONeNrXC93KkbiHSoRFcUBl92ADuv8KC+Pk26Ca40YurodIeHmUPAlbWLQoLJ6AlSzamPFSv99VukVS6TpmR11SdTl9L0Poh+tOJAc4TdsJW1s+zUObcmJ3QV2kDk9gpZRwkwpjMFozrELUCDaTS7BIopf+8JmbXyUf2NnhZOjp3SYqhToZ3yHv8IkNMoQLr9cvV5XImP/CuN2+ZiSi+Vuk37vHkWFx5sYcBQizE7c9l/HLxojwxMKQq5ZUSVfHLxYuUP3PIZc5Qk7zGKYUBBhdnXtkRKuAR7UDxwC3pUIjuR7f71+70flhnm1Ct5pnlM0CCkxRBMrwbcW5Fx1vjvTO1httaVHIQplZjkGcOiuCNbGtpdsfOWoiRMDcWJY+NBgfjMfSOX40tZfx0lSc8fYElQvQb57l+hF+CpZwihYMmChN7HWWqKZwNBQ6AtSm30Giszc7DjMTSLAfWSLzMPBwj8rN6Q3VsrvbzEAzgbpY69EmxtsISQfByweziSfXYg6ScVhqCHy6zqMy0oS7pN1mucJapyedsu2ijgaEvLl2QzsC5Ej0yi+Ni5ydO9wZXUplIW/HjspGiDlCSEZYQhJKwv1hvwaIYn7mU5PJeOXAi7LkhBBYwimquONp1BVYox+XUgG7D1glSceAPQ/biRfb3uKKasPx7aa7xpGU6luGaDw3scnkVWyrirzTlGKTlllIL4q80a7HI/lDuQfhJI+JF/JV2KhWvaNtrHG9fhKH+xDK9nPUfnit7yyXmzVdukfeWA1pBpd7qAgOKu7bNl/7KDGgkYDW1BzcSuLE3UL1hOOjqSSjgURXpOmKro0kGfTEx6Ds8g9eqOhfasHS1UQVV8g0Vhc5M6qOuMocngYSAWaOIO6wkWB4pgMLBhLlLh4nZx+XVBgKcTGtkJfOZibwCDopfvAi/jufpzwy8DFw649DN2eWAU28cuyUvQxRYq2p90h7jdcdsaDBt2Zhv8qMrvT9fZzqEb5qzo5hRfAxoAcuvCH6G5QFtn/cu2YyzgZ8H6KkBDmSjZmDCSLbzsRzOeiEmEZt4Ri7h22k8R1MS7JIisD9M/28xye3dG6kBnCN2Cky8wzcVzOwjKl68KD6FWYh7/k2wuceX7VmZW+C1L17kH46r4ImDTduyKfNuLT/JbHwXYhvRo6LcOuIoFPnfERiFj9wonGJGclSukSn5geVTo93sUu0MO0A9+M4TvHDAWeE3Raiasn/jeWb4jedqIeyD6Ub04Zq9UVeWaPSurFtoLfOL40lc2mOYvovu3BAEwZNx5RhtYTmcbHSSLni/EUnJjtxZD5SJubuej9pdV92cxi11umS9MzDdO5OTGUdJrWa69ka5pGJA1ly9f4F9UyQZLJfha5f4C9xFM74QIVWG3VK9IKpoaq62wE0rwSwSA/LQIoVpizu03RknMW0gAmktJtsOtS70ya4dEYjWUBapWJwW1g6Nj1v/uHUJ/vc9yRY5Gzf583/V/4eQ9U688MuXX33nF6d+ZZUt+zcLc/Xq+UIuf+QwMB8pROgSf6U1j9E7KPlV5yV7k2x055VUtrWGC0X9u2WyXusVuvUAvRNcCNHQSchs1bDP2mNYecw+B4IDYfp3FeIZ4KiRIDCZemveTokwRbypcDVwVyEGH8kGmcL0Ng4PFutWOi1QZVttKCS/vkTcWbLWkEVgCGG56bbqeIXDPG3Ifb7Z/3Yd1B6iUqtTmwfIUF8pVjqk1lFODPvUcjpE2BOdjrOShRXda6EEYPmwYb7V60kosciWY5Vm+Fh0w8J1Hm1vhgNPh8GbTlsqgLVSSCHSNjwIryGUPu+uCM8zs7yQbwYb0n7FJ+LKCuPlu7Qs4dNSjBDc9xAdV8YCAAzns1DvNbvTShKQctmfVSI+dk/E0U0egoM7IYS8sO6CAV7csPVFze7l+3gQdffapd69x3zPWUDb81ivaSQNIkWoEIg33LmO210Y4glirY0qrvUGlN2TuZbEk76MwTcclOBpH5g7Y1bSnITh4sWz58Sly1DKxmTXOLIgNBDuwFqhpd5JrfqYWCDeeByzbRXpC1vlpKQUUhK1qBvYIF/sJIi3m9QdeaQn2BH9+E38rpjqPaXO+Od2gp3Rz9LE74yp3lPqjDhXE+gJHaCJ3wGlePgyuiDeVRXv6r4GgZ+TMo8DLSWjDoJSKdSTpWBPlkRPmNVcxCfCfDR0yGIGMBXjRqWhlNLnuCoFi91H1HTNIqRXEPYXL1q2shvMLis3yKuTrfYKLuCKxgTAorQT3mwT5uW847VAB6/X2rMtp1MV64rhVfZCB8wBylJDGnfWW3Cb6koq1gjQYXb+9pgWh3e3e3/5e+8RHpOhU8mPvutfftC7cYOtF4dRUVpLGYOJdVJWOi5ofZyaSTK/HHgk1hugnVhH8FXJr4gZ+VB1ASP85EKtXkVSyzrsMh/0D8jy7rJbOdlqNJwmDFgFiBpa0ggi3+fVIe6l+6E1j40mxgL4wxlUlvehv4a4TEG3//EDUDyt3Zub/WubvRtf965d7V27n81mAwwXjvOY9ZoMU/iAWxmYgw9Tiosb0fCx3myCRYBY/fs3oYEE89ZccGeXau4FGK8aO+n+DgtpSQZ5DZZmwaiBFpVb2QyNRgWiyIsOLQSddZacWh0hikYsbsMhMq+2MEKcyi25nS6gk7bwS7PluV3OCRo3C8ZI/GPziiUCKb8DGt+zWCQVbgkQqQ9byQTIPR5SBZ8SKXEKZo1l0AVbWRVy7pOggsD2znVTIat/7f7u9a+KFmLqypxdYXtXoZWkE6PRYHOARzHxOjwDRSrItUu4ivAypRjgqOUIYPSOJK0dExQeEdibFwAhvN5pzQPHdHULd/B05m23eVWDUartIyKJZuutynm7FJ7y0GxJZj3EIKbh7VZbdGOObJUmvHGyq12utrh88HvJhyxGkwMYAChNAb5JYIM0P4JrIK+tsS/ItP5dFDZ+Ly7UmtXWhawUPJjHIvgMhZGYZaZ32WpLSCmOccpsyIg4Mx4NFLftqOdZhPnOYqc+EDlRCJjS89rd4vj4hQtQhlDJVlqN8WalPQ5fkfrjrxZ+9e9v/aJw8vkzv5p41Q4vy7wFhLkHeGn7ndm60zyvLHrkwrp946fzPyLEpOOd7f7DbYvfbrnz8NLu+/fIuXbtwU8PaU3E0C2yc27nDReZQDWcWdbYqjNIziQ8Xj3TofpMyiVSqp99lOpYntXWvc0AA1Uy0KIFvoE4ci9t1QLZ7yLO9QaPr2an6XyiCAAV5wrMh0Dj3vkzYT4S5GlObvPFPDHuP0RAKEHGEtZ//5uF33D/Ps6tP7GPDwcPmkUdNo0+OiTSSkWeMoYHIydamtQD9ikO3ZjDbUBiJTz+4XUyFLZvWzxD0gy/HYDy+/DDGCwJUvAYm+b7184eE++H13ceRJ0I+v/YvqE+//jUC/F6yFxV+Z12ZmcHTzPsbsrXWqE4rBOVWZEgKqXonjKgg8WUMFZLExmLCUalRJo2rIuMn9M8XKEoxjqNe//FBNuMh7IUXcKYNE3hNACHBGZiTVNXS4auSxNmVBEU8F8qo6Bs9NIJKj9SlxKdspvJ6Jhw06mv/Mbld5W5IrJDqAOiZCAFAdGXbwoHiowldrY2+3c2tHu/MIYcbb4vfrR6W5s7Dx/s/vEq94++3YQi6CJkurS/t5xIpazwNWpyofxprpMf/v1/Pv7I6n14q//Dxu7vNmhTE4hweesnvEQy7nhhEc0of1mEtcRjSmwV34Cqxu7iCmyv+2lpqllepeQ7fxabI4M5bIJDh2/fVIBJwIaT1FX1JLXwz2Wq2cbK6QWnI89RK4fgg9kR1UPvg85X23tJ4oJnPyLZJJiOZW/H5/lYDr1g0U9u59NzlDR1IyVR+cdHj2Dyf4YBf72PruJx1mCj4p7LmMfAJ2PdoTIzpqRckixkzAghuuvjpWdgUvKqUFyK69Rfri4HWVucNqjKe9soZsntvA6insw8So5P53aSkj+tjOVzqDUOX9puq113JRBN4wvpd1N7UvAGqk7x03/QIbAuRrkYDpTv4VQ21ySrRk1yZF2ypBxl40ceq4pqicftQqmt8AUYOri70Lu2Ld+L8dk3TvYMLHX9z25YiAsb6LFE75sr2G4eXvWu/cAblXxjbnQgGqZ7YY15WzQABzLbDGJ3jyl4hqXcYWmvzEl32DRm0jAxxucrnWInQXTdfIp93ygNywJkQmjosfpR8gKpmWWEIvfExfvmFb6GWf1P1nt/vo4SfoB8N8hds9Tdm8wdKC5HkZb7y4lUakGBmrcCInrfyTYOSB7GEoBxMnAcqHiZCODKp3VId2K8dQCS5CBn5R7m42GNf59ObmBfpdI0T1P8JU/5qyhhoyT/1VVQXc016aNmz8OgRCF6KwN3TxJEaYPJHPZdDAWCEzAhzjYlEjFq4DyTNWIcpuTVSFsdrSWmRvh1ClSJ+eGJTiedeiV4fjX02t8r5ykYZdT0KBinLl6UF3cxvEaApHcEQBXkMSWmSugqNDU8rmjLFCXoLTDHCutGRlSNQcfGShdLJoJbYhzCTO45yi7HtZpiIhNncBg+IZjsMYBMcL2JPeBQNYZ3ltygiY7cOMglFubZwDk0HPvhAFQWLv1EuYNEKjuCRk3huQ5LRF8kWJx5/+FG/5NLhnNnPCFfgg5F0GkG/wK0WBynyfLgwQz/1JpwIWL1NKteZH/SvJ0i/5vmqlCRdq3TLNSjesIrasG+L59+TYTdMFcJ3oQurZbe9+uU2Eb6fOWFECH/p3+mTjo/Jf5jiaQqwFMJ0Q2BKvlB2aHrBDtkl0iww0mhZYZjllgLeShHFt4hf2fE+XzFAuDOZHWwztbOZX2nkgjNiChxwgtGWysDEO1y1XZ/FU2jJrIgWP4Bm0TwgA06Qf0DRBqfibM1wUwFwcZ/mo7SiLz844wAP/ENxWA638H6B4sN4kFu+1RDGs5IOggUZ7N1hAooB/ziLKOpYTEKEyDOkhTA33guOtZiEOqZDIAYT4/Pp0EFV1cZ7NMQtNRuB1YU/7Spv6Swg4s7j36Mv54QRHMO7FREbuzQCUAt6/Pgk6PyjPQI0nYIq8YUuuFcx3uQdRF9jiv1lIPQIofQKq17SFJ5rBW/+Olf8JsqYvG7RKO86vD45uLZc2kKGMYPStQtflVxhe9rJXFyuPzCqRdPvPnKmXdOnjhzmp06AUwNQS/PPmsMtzGGslDf3sGzK6nS6Oen9CMPw+p3K3QH0cDgrkgYbWfeFT6TATgwa+TFVssTp0N5t6HYqSWoi3XcJry0JSFANaqu2Gmnu9KsKOd+KEb0glPzLAwCduSWZlLNo8buZsU2uyzdie56Uu/epcQheLaQbVw932oB7ZspdjSRBpLAaIDrlEOne1Z9k8kjx9FJTv+kel09i5o7Rxnz6HBnRJE8FFnbw4DFHPHI0TKcuNOmHfzggdEgryoHisID+cJrv+T2EA6TW7XTyiD6B4WxrePj0Kda25s5dOj44UxmUESSlcnMHFIdKOysK2DfwVBA3gEeJ2HYW9czl7lLFOrudIBS5TJdO5Vid0+ZRaM9A3QJtW5IrjlVQE/UDDlBwthyzyq5zGYiY7DMVxEwCJQFIkaivFEDDAJJG9Fn4/dhj3lVWZpTtBLwArv/uG7tbIkOUxazh9u77z6wMEsILhobO4/upa3etfu9Lx5bGEF+93r/4xs7D69bGGdwGZ69/zmuzHcu8ZpyWc4G8TUxAR2KVseLp3ycwAErIRvNYaa9laKz6LXsEAm0QZgjeWYbMiuyLnMX2J4yHI4+cP2/fdV/39/5iGw8wr0XEdIDcNfv7b53h+dHN0Qaqe1JcvEP/A+b1QZ34eiTWjEbn9JUnsyNMJVN+/8D7iUbcTLHspnjTGHNw0+7vNVah91rVIT5vNhokt+fJwgNXkHhc7YEPkBGDN685TJiEkksvTm9b64oiBNsFg7ncwAdvZcJkmntFvmQOQps9PK53M+CKZIpJckH9/Hgx+ebaWv30+v9a3dsa1x2S237gPvIkiUN6x3lpeLBf+xz3J4+lU5QJltKvsONpGH9Ic+Y6FBzsTGLYnNPg5fDecKSe9ohH/fT6j7b4scU1Mne5Q1+8WRqGBGYR3CvVOAZEgu21ag16e/e6BCZYzbiyojATROj3CBhpHhoe0spFzk2kTcN+KEcSR6QyJyhwcFQNAJtM8Ae6RYK9da0THC4xyOZ7GC7LCOthnWRbTnspYc85GNgF9WVJYaStD9lKObCt08VSNmKCWW1H67emLyeo+s3YUfNU1JzJo6OoOaMdPnqiErOKK6q/311nf5/XOl9sRGcYOyQLmcEltIy7gKhCYJWG7vHb606Ps6/mkrQfVaDSvTvvTusxMbVISVYMH24BPALdfjpLNro141eo7kDez86JdjsoFZa4q4wDH/fusmvDHtKqskwdUx61w9KGRv/l6wHo8mIA1gWApc8jrQ4jOMpevyO0S4zh/4XWyBpnxaAAQA="


def get_html_path():
    html_bytes = gzip.decompress(base64.b64decode(_HTML_DATA))
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".html", delete=False, prefix="budget_")
    tmp.write(html_bytes)
    tmp.close()
    return tmp.name


if getattr(sys, "frozen", False):
    EXE_PATH = Path(sys.executable)
    EXE_DIR = EXE_PATH.parent
    UPDATER_PATH = EXE_DIR / "updater.exe"
    DATA_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "MyBudget"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
else:
    EXE_PATH = None
    EXE_DIR = Path(__file__).parent
    UPDATER_PATH = EXE_DIR / "updater.py"
    DATA_DIR = Path(__file__).parent

DATA_FILE = DATA_DIR / "budget_data.json"
LICENSE_FILE = DATA_DIR / "license.json"


# ═══════════════════════════════════════════════
# 🔐 라이선스 모듈
# ═══════════════════════════════════════════════

def _get_token():
    try:
        return base64.b64decode(_OBF_TOKEN.encode()).decode()[::-1]
    except Exception:
        return ""


def get_hwid():
    components = []
    system = platform.system()
    mac = uuid.getnode()
    if mac != 0:
        components.append(f"mac:{mac}")
    if system == "Windows":
        try:
            out = subprocess.check_output("vol C:", shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
            serial = "".join(c for c in out if c.isalnum())[-10:]
            components.append(f"vol:{serial}")
        except Exception:
            pass
        try:
            out = subprocess.check_output("wmic cpu get ProcessorId /value", shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
            cpu = "".join(c for c in out if c.isalnum())[:16]
            components.append(f"cpu:{cpu}")
        except Exception:
            pass
    elif system == "Darwin":
        # 방법 1: ioreg로 Hardware UUID (앱 샌드박스에서도 동작)
        try:
            out = subprocess.check_output(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                stderr=subprocess.DEVNULL
            ).decode(errors="ignore")
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    val = line.split('"')[-2].strip()
                    if val:
                        components.append(f"ioreg_uuid:{val}")
                        break
        except Exception:
            pass
        # 방법 2: system_profiler fallback
        if not any("ioreg_uuid" in c for c in components):
            try:
                out = subprocess.check_output(
                    ["system_profiler", "SPHardwareDataType"],
                    stderr=subprocess.DEVNULL
                ).decode(errors="ignore")
                for line in out.splitlines():
                    if "Hardware UUID" in line:
                        val = line.split(":")[-1].strip()
                        if val:
                            components.append(f"mac_uuid:{val}")
                            break
                for line in out.splitlines():
                    if "Serial Number" in line:
                        val = line.split(":")[-1].strip()
                        if val:
                            components.append(f"mac_serial:{val}")
                            break
            except Exception:
                pass
    elif system == "Linux":
        try:
            with open("/etc/machine-id") as f:
                components.append(f"mid:{f.read().strip()}")
        except Exception:
            pass
    if not components:
        components.append(f"platform:{platform.node()}:{platform.machine()}")
    raw = "|".join(sorted(components))
    return hashlib.sha256(raw.encode()).hexdigest()[:32].upper()


def _gist_request(method="GET", data=None):
    url = f"https://api.github.com/gists/{GIST_ID}"
    token = _get_token()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "budget-app-license",
        "Authorization": f"token {token}"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    # macOS PyInstaller 앱에서 SSL 인증서 문제 해결
    import ssl
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return json.loads(r.read().decode())
    except ssl.SSLError:
        # SSL 실패 시 certifi 시도
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return json.loads(r.read().decode())
        except Exception:
            # 마지막 수단: 인증서 검증 비활성화 (GitHub API라 안전)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return json.loads(r.read().decode())


def _read_db():
    resp = _gist_request("GET")
    content = resp["files"]["keys.json"]["content"]
    return json.loads(content)


def _write_db(db):
    _gist_request("PATCH", {
        "files": {"keys.json": {"content": json.dumps(db, ensure_ascii=False, indent=2)}}
    })


def _local_sig(key, hwid):
    return hashlib.sha256(f"{key}:{hwid}:budget".encode()).hexdigest()


def _load_local_license():
    if LICENSE_FILE.exists():
        try:
            with open(LICENSE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def _save_local_license(key, hwid):
    payload = {"key": key, "hwid": hwid, "sig": _local_sig(key, hwid)}
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def verify_license():
    hwid = get_hwid()
    local = _load_local_license()
    if local is None:
        return False, "no_license"
    if local.get("sig") != _local_sig(local.get("key", ""), local.get("hwid", "")):
        return False, "tampered"
    if local.get("hwid") != hwid:
        return False, "hwid_mismatch"
    key = local.get("key", "")
    try:
        db = _read_db()
        keys = db.get("keys", {})
        if key not in keys:
            return False, "key_deleted"
        entry = keys[key]
        if entry.get("revoked"):
            return False, "revoked"
        if entry.get("hwid") != hwid:
            return False, "hwid_changed"
        return True, "ok"
    except Exception:
        return True, "ok_offline"


def register_key(key):
    key = key.strip().upper()
    hwid = get_hwid()
    try:
        db = _read_db()
    except Exception as e:
        return "net_error", f"서버 연결 실패: {e}"
    keys = db.get("keys", {})
    if key not in keys:
        return "not_found", "유효하지 않은 키입니다."
    entry = keys[key]
    if entry.get("revoked"):
        return "revoked", "취소된 키입니다. 관리자에게 문의하세요."
    registered_hwid = entry.get("hwid")
    if registered_hwid is None:
        from datetime import datetime
        entry["hwid"] = hwid
        entry["activated_at"] = datetime.now().isoformat()
        try:
            _write_db(db)
        except Exception as e:
            return "net_error", f"등록 실패: {e}"
        _save_local_license(key, hwid)
        return "ok", "등록 완료!"
    elif registered_hwid == hwid:
        _save_local_license(key, hwid)
        return "ok", "인증됨."
    else:
        return "duplicate", "이 키는 다른 PC에 이미 등록되어 있습니다.\nPC를 변경하려면 관리자에게 문의하세요."


# ═══════════════════════════════════════════════
# 라이선스 UI HTML
# ═══════════════════════════════════════════════

LICENSE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>내 가계부 - 라이선스 등록</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0f0f0f;
    color: #e0e0e0;
    font-family: 'Malgun Gothic', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    user-select: none;
  }
  .card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 48px 56px;
    width: 480px;
    text-align: center;
  }
  .icon { font-size: 52px; margin-bottom: 20px; }
  h1 { font-size: 22px; font-weight: 700; margin-bottom: 8px; color: #fff; }
  .sub { font-size: 13px; color: #888; margin-bottom: 36px; line-height: 1.6; }
  input {
    width: 100%;
    background: #111;
    border: 1.5px solid #333;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 18px;
    color: #fff;
    text-align: center;
    letter-spacing: 3px;
    font-family: 'Courier New', monospace;
    transition: border-color 0.2s;
    outline: none;
    margin-bottom: 16px;
  }
  input:focus { border-color: #4ade80; }
  input.error { border-color: #f87171; }
  input.success { border-color: #4ade80; }
  button {
    width: 100%;
    background: #4ade80;
    color: #0f0f0f;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover { background: #22c55e; }
  button:disabled { background: #333; color: #666; cursor: not-allowed; }
  .msg { margin-top: 16px; font-size: 13px; min-height: 20px; line-height: 1.5; }
  .msg.err { color: #f87171; }
  .msg.ok { color: #4ade80; }
  .msg.info { color: #60a5fa; }
  .hint { font-size: 11px; color: #555; margin-top: 28px; }
</style>
</head>
<body>
<div class="card">
  <div class="icon">🔐</div>
  <h1>내 가계부 라이선스 등록</h1>
  <p class="sub">이 앱을 사용하려면 라이선스 키가 필요합니다.<br>관리자로부터 받은 키를 입력하세요.</p>
  <input type="text" id="key" placeholder="XXXX-XXXX-XXXX-XXXX"
    maxlength="19" autocomplete="off" spellcheck="false" />
  <button id="btn" onclick="submitKey()">키 등록하기</button>
  <div class="msg" id="msg"></div>
  <p class="hint">v""" + CURRENT_VERSION + """ | 1 PC에만 등록 가능합니다</p>
</div>
<script>
  const input = document.getElementById('key');
  const btn = document.getElementById('btn');
  const msg = document.getElementById('msg');

  input.addEventListener('input', function() {
    let v = this.value.replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 16);
    let parts = v.match(/.{1,4}/g) || [];
    this.value = parts.join('-');
    input.className = '';
    msg.textContent = '';
    msg.className = 'msg';
  });

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') submitKey();
  });

  function setMsg(text, type) {
    msg.textContent = text;
    msg.className = 'msg ' + type;
  }

  function submitKey() {
    const k = input.value.trim();
    if (k.length < 19) {
      setMsg('키를 올바르게 입력하세요 (XXXX-XXXX-XXXX-XXXX)', 'err');
      input.className = 'error';
      return;
    }
    btn.disabled = true;
    btn.textContent = '확인 중...';
    setMsg('서버에 연결 중입니다...', 'info');
    pywebview.api.submit_license_key(k);
  }

  function onLicenseResult(ok, message) {
    if (ok) {
      setMsg('✅ ' + message, 'ok');
      input.className = 'success';
      btn.textContent = '등록 완료!';
      setTimeout(function() { pywebview.api.license_accepted(); }, 1200);
    } else {
      setMsg('❌ ' + message, 'err');
      input.className = 'error';
      btn.disabled = false;
      btn.textContent = '키 등록하기';
    }
  }
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════
# 기존 유틸 함수들
# ═══════════════════════════════════════════════

def parse_version(v):
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split("."))
    except:
        return (0, 0, 0)


def check_update():
    try:
        token = _get_token()
        headers = {"User-Agent": "budget-app", "Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        req = urllib.request.Request(RELEASES_API, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        latest = data.get("tag_name", "0.0.0").lstrip("v")
        notes = data.get("body", "")
        download_url = ""
        installer_url = ""
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name == "updater.exe":
                continue
            if "installer" in name.lower() or "setup" in name.lower():
                installer_url = asset.get("browser_download_url", "")
            elif name == "가계부.exe":
                download_url = asset.get("browser_download_url", "")
        if parse_version(latest) > parse_version(CURRENT_VERSION):
            return latest, notes, download_url or installer_url
    except Exception as e:
        print("업데이트 확인 실패:", e)
    return None, None, None


def download_and_update(window, latest_version, download_url):
    try:
        if not download_url:
            window.evaluate_js("showUpdateProgress('다운로드 URL을 찾을 수 없어요.')")
            return
        window.evaluate_js("showUpdateProgress('다운로드 중...')")
        tmp_dir = tempfile.mkdtemp()
        is_installer = "installer" in download_url.lower() or "setup" in download_url.lower()
        tmp_exe = os.path.join(tmp_dir, "update.exe")

        def reporthook(count, block_size, total_size):
            if total_size > 0:
                pct = min(int(count * block_size * 100 / total_size), 100)
                window.evaluate_js(f"showUpdateProgress('다운로드 중... {pct}%')")

        urllib.request.urlretrieve(download_url, tmp_exe, reporthook)
        window.evaluate_js("showUpdateProgress('설치 중...')")
        if is_installer:
            subprocess.Popen([tmp_exe])
            window.evaluate_js("showUpdateProgress('설치 파일을 실행했어요. 설치 후 재시작하세요.')")
            import time; time.sleep(2)
            window.destroy()
        elif EXE_PATH and UPDATER_PATH.exists():
            subprocess.Popen([str(UPDATER_PATH), tmp_exe, str(EXE_PATH)])
            window.evaluate_js("showUpdateProgress('재시작합니다...')")
            import time; time.sleep(1)
            window.destroy()
        else:
            window.evaluate_js("showUpdateProgress('다운로드 완료! 수동으로 교체해주세요.')")
    except Exception as e:
        window.evaluate_js("showUpdateProgress('오류가 발생했어요.')")
        print("업데이트 오류:", e)


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "customCats" not in data: data["customCats"] = []
            if "assetData" not in data: data["assetData"] = {"accounts": [], "debts": [], "investments": []}
            if "fixed" not in data: data["fixed"] = []
            if "includeDebtInNet" not in data: data["includeDebtInNet"] = False
            if "dutchPayList" not in data: data["dutchPayList"] = []
            return data
    return {
        "transactions": [], "fixed": [], "customCats": [],
        "assetData": {"accounts": [], "debts": [], "investments": [], "manualAssets": []},
        "includeDebtInNet": False,
        "dutchPayList": []
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════
# API 클래스
# ═══════════════════════════════════════════════

class LicenseApi:
    def __init__(self, on_accept):
        self._on_accept = on_accept
        self._window = None

    def set_window(self, w):
        self._window = w

    def submit_license_key(self, key):
        """백그라운드 스레드에서 검증 후 JS 콜백으로 결과 전달"""
        def _do_verify():
            try:
                result, msg = register_key(key)
            except Exception as e:
                result, msg = "net_error", str(e)
            if self._window:
                ok = "true" if result == "ok" else "false"
                safe_msg = msg.replace("'", " ").replace('"', " ").replace("\n", " ")
                self._window.evaluate_js(
                    f"onLicenseResult({ok}, '{safe_msg}')"
                )
        t = threading.Thread(target=_do_verify, daemon=True)
        t.start()
        return {"ok": True, "started": True}

    def license_accepted(self):
        if self._window:
            self._window.destroy()
        self._on_accept()


class Api:
    def __init__(self):
        self._window = None
        self._update_url = None

    def set_window(self, window):
        self._window = window

    def get_data(self):
        return load_data()

    def get_version(self):
        return CURRENT_VERSION

    def check_update(self):
        latest, notes, url = check_update()
        if latest:
            self._update_url = url
            return {"available": True, "version": latest, "notes": notes}
        return {"available": False}

    def do_update(self, version):
        if self._window and self._update_url:
            t = threading.Thread(target=download_and_update, args=(self._window, version, self._update_url))
            t.daemon = True
            t.start()
        return {"ok": True}

    def save_transactions(self, transactions):
        data = load_data(); data["transactions"] = transactions; save_data(data)
        return {"ok": True}

    def save_fixed(self, fixed):
        data = load_data(); data["fixed"] = fixed; save_data(data)
        return {"ok": True}

    def save_custom(self, customCats, assetData, includeDebtInNet=False):
        data = load_data()
        data["customCats"] = customCats
        data["assetData"] = assetData
        data["includeDebtInNet"] = includeDebtInNet
        save_data(data)
        return {"ok": True}

    def save_dutch(self, dutchPayList):
        data = load_data()
        data["dutchPayList"] = dutchPayList
        save_data(data)
        return {"ok": True}

    def open_url(self, url):
        import webbrowser; webbrowser.open(url)
        return {"ok": True}

    def clear_all(self):
        save_data({
            "transactions": [], "fixed": [], "customCats": [],
            "assetData": {"accounts": [], "debts": [], "investments": []},
            "includeDebtInNet": False
        })
        return {"ok": True}


# ═══════════════════════════════════════════════
# 실행
# ═══════════════════════════════════════════════

def run_main_app():
    api = Api()
    html_path = get_html_path()
    try:
        window = webview.create_window(
            title="내 가계부 v" + CURRENT_VERSION,
            url=html_path,
            js_api=api,
            width=1280,
            height=820,
            min_size=(960, 640),
            background_color="#0f0f0f"
        )

        def on_loaded(w):
            api.set_window(w)

        def bg_update_check():
            import time; time.sleep(5)  # exe 완전 로드 대기
            try:
                latest, notes, url = check_update()
                if latest:
                    safe_notes = (notes or "").replace("'", " ").replace('"', " ")[:100]
                    window.evaluate_js(f"showUpdateNotify('{latest}', '{safe_notes}')")
            except Exception as e:
                print("업데이트 체크 오류:", e)

        t = threading.Thread(target=bg_update_check)
        t.daemon = True
        t.start()

        webview.start(on_loaded, window, debug=False)
    finally:
        try:
            os.unlink(html_path)
        except:
            pass


def run_license_window():
    accepted = threading.Event()

    def on_accept():
        accepted.set()

    lic_api = LicenseApi(on_accept=on_accept)
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, prefix="license_", encoding="utf-8")
    tmp.write(LICENSE_HTML)
    tmp.close()

    try:
        win = webview.create_window(
            title="내 가계부 - 라이선스 등록",
            url=tmp.name,
            js_api=lic_api,
            width=540,
            height=440,
            resizable=False,
            background_color="#0f0f0f"
        )
        webview.start(lambda w: lic_api.set_window(w), win, debug=False)
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass

    if accepted.is_set():
        run_main_app()


if __name__ == "__main__":
    valid, status = verify_license()
    if valid:
        run_main_app()
    else:
        reason_map = {
            "no_license":    "라이선스 없음",
            "tampered":      "license.json 변조 감지",
            "hwid_mismatch": "HWID 불일치",
            "key_deleted":   "키 삭제됨",
            "revoked":       "키 취소됨",
            "hwid_changed":  "HWID 변경됨",
        }
        print(reason_map.get(status, f"인증 실패: {status}"))
        run_license_window()
