HEADER_INFO = """""".strip()
SIDEBAR_INFO = """
<div class="contributors font-body text-bold">
<a class="contributor comma" >Aditya Nautiyal</a>
<a class="contributor comma" >Sanuj Singhal</a>
<a class="contributor comma" >Garvit</a>
<a class="contributor comma" >Akshat Gupta</a>

</div>
"""
CHEF_INFO = """
<h2 class="font-title">Welcome to our restaurant! </h2>
<p class="strong font-body">
<span class="d-block extra-info">(We are at your service with two of the best chefs in the world: Chef Vault, 
Chef Rush. Vault is known for being more creative whereas Rush is more meticulous.)</span>
</p>
""".strip()
PROMPT_BOX = "Add custom ingredients here (separated by `,`): "
STORY = """

<pre>[Inputs]
    {food items*: separated by comma}
     
[Targets]
    title: {TITLE} &lt;section>
    ingredients: {INGREDIENTS: separated by &lt;sep>} &lt;section>
    directions: {DIRECTIONS: separated by &lt;sep>}.

""".strip()