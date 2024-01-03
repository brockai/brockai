from helpers.config import authorization_url

sidebar_links_footer = """
<div class="top-space">Docs & Jupyter Notebooks</div>
<div class="left-space top-left-space">☁️&nbsp;&nbsp;&nbsp;<a href="https://github.com/brockai/brockai/wiki/Cloud-Deployment" target="_blank">Cloud Deployment</a></div>
<div class="left-space top-left-space">🤗&nbsp;&nbsp;&nbsp;<a href="https://github.com/brockai/brockai/wiki/🤗-Huggingface" target="_blank">Huggingface</a></div>
<div class="left-space top-left-space"><img src="app/static/openai.png" alt="openai" width="18">&nbsp;&nbsp;&nbsp;<a href="https://github.com/brockai/brockai/wiki/OpenAI" target="_blank">OpenAI</a></div>
<div class="left-space top-left-space">👑&nbsp;&nbsp;&nbsp;<a href="https://github.com/brockai/brockai/wiki/deepset-(Haystack)" target="_blank">deepset (Haystack)</a></div>
<div><br></div>
<div class="footer">
<a href="https://github.com/brockai" target="_blank">
<img src="app/static/github-mark-white.png" alt="GitHub Icon" width="32" height="32">
</a>&nbsp;&nbsp;&nbsp;
<a href="https://discord.gg/c3py8dTG" target="_blank">
<img src="app/static/discordlogo.png" alt="Discord" height="32">
</a>
</div>
"""

sidebar_app_header = """
<div class="header logo-label">
<img src="app/static/platform_logo_darkmode.png" alt="Platform" height="18">
</div>
"""

powered_by_openai = """
<div class="rounded-box">
Powered by&nbsp;&nbsp;<img src="app/static/openai-white-lockup.png" alt="OpenAI" height="18"></div>
</div>
<br>
"""

platform_link = """
<div class="rounded-box red-text">
✨&nbsp;&nbsp;<a href="""+authorization_url+""" target="_blank" style="text-decoration: none;">Platform Sign In</a>
</div>
"""

platform_intro = """
<div>
<p>
Platform's purpose is to assist integrating AI functionality into new or existing systems.
</p>
<p>
Our approach is to build prototypes, with your data, that can be taken to production. Prototypes typically run 30 - 90 days.
</p>
<p>
brockai is an open source project that can be hosted anywhere or you can run it here for free.
</p>
</div>
"""
